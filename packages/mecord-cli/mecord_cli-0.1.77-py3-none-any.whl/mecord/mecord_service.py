import os
import sys
import time
import signal
import subprocess
import json
import platform
import psutil
from pathlib import Path
from urllib.parse import *

from mecord import store
from mecord import xy_pb
from mecord import xy_user 
from mecord import utils
from mecord import progress_monitor

def process_is_alive(pid: int) -> bool:
    try:
        # if platform.system() == 'Linux':
        #     print(f"======= touch!!!  ")
        #     dddd = os.stat(f"/proc/{pid}")
        #     print(f"======= touch!!!   {dddd}")
        #     status = os.stat(f"/proc/{pid}").st_state
        #     print(f"======= status {status}")
        #     if status == "R" or status == "S" or status == 'D':
        #         return True
        #     else:
        #         return False
        # else:
        process = psutil.Process(pid)
        pstatus = process.status()
        if pstatus == psutil.STATUS_RUNNING or pstatus == psutil.STATUS_SLEEPING:
            return True
        else:
            return False
    except (FileNotFoundError, psutil.NoSuchProcess):
        return False
    except Exception as e:
        return False

def stop_file():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "stop.now")

class BaseService:
    def __init__(self, name, pid_file=None):
        self.name = name
        self.pid_file = pid_file
        self.running = False

    def start(self):
        store.writeDeviceInfo(utils.deviceInfo())
        if self.pid_file:
            with open(self.pid_file, 'w') as f:
                f.write(str(os.getpid()))
        self.running = True
        signal.signal(signal.SIGTERM, self.stop)
        self.run()

    def run(self):
        while (os.path.exists(stop_file()) == False):
            self.run_internal()
            time.sleep(1)
        if self.pid_file and os.path.exists(self.pid_file):
            os.remove(self.pid_file)
        print("MecordService stoped!")
        if os.path.exists(stop_file()):
            os.remove(stop_file())
        

    def stop(self, signum=None, frame=None):
        with open(stop_file(), 'w') as f:
            f.write("")
        self.running = False
        print("MecordService waiting stop...")
        while os.path.exists(stop_file()):
            time.sleep(1)

    def is_running(self):
        if self.pid_file and os.path.exists(self.pid_file):
            with open(self.pid_file, 'r', encoding='UTF-8') as f:
                pid = int(f.read())
                try:
                    if process_is_alive(pid):
                        return True
                    else:
                        os.kill(pid, 0)
                        return False
                except OSError:
                    return False
        else:
            return self.running

class MecordService(BaseService):
    def __init__(self):
        pid_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "MecordService.pid")
        super().__init__("MecordService", pid_file)

    def executeLocalPython(self, taskUUID, cmd, param):
        inputArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{taskUUID}.in")
        if os.path.exists(inputArgs):
            os.remove(inputArgs)
        with open(inputArgs, 'w') as f:
            json.dump(param, f)
        outArgs = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{taskUUID}.out")
        if os.path.exists(outArgs):
            os.remove(outArgs)
            
        outData = {
            "result" : [ 
            ],
            "status" : -1,
            "message" : "script error"
        }
        executeSuccess = False
        command = f'{sys.executable} "{cmd}" --run "{inputArgs}" --out "{outArgs}"'
        print(f"exec => {command}")
        try:
            path = os.path.dirname(cmd)
            config_file = os.path.join(path, 'config.json')
            with open(config_file, "r") as f:
                data = json.load(f)

            
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            if data is not None and 'type' in data and data['type'].lower() == 'sd':
                widget_infos = [{"widget":"SD", "port":6006, "name":"", "path":path}]
            else:
                widget_infos = [{"widget":"other", "port":"", "name":"", "pid": process.pid, "path":path}]
            print(f"monitor process: {path}")
            progress_monitor.start(widget_infos)
            output, error = process.communicate()
            progress_monitor.stop()
            if process.returncode == 0:
                print(output.decode(encoding="utf8", errors="ignore"))
                if os.path.exists(outArgs):
                    with open(outArgs, 'r', encoding='UTF-8') as f:
                        outData = json.load(f)
                    executeSuccess = True
                    print(f"exec success result => {outData}")
                else:
                    print(f"task {taskUUID} result is empty!, please check {cmd}")
            else:
                print("====================== script error ======================")
                print(error.decode(encoding="utf8", errors="ignore"))
                print("======================     end      ======================")
        except subprocess.CalledProcessError as e:
            print("====================== process error ======================")
            print(e)
            print("======================      end      ======================")

        if os.path.exists(inputArgs):
            os.remove(inputArgs)
        if os.path.exists(outArgs):
            os.remove(outArgs)
        return executeSuccess, outData,

    def needChangeValue(self, data, type, key):
        if "type" not in data:
            print("result is not avalid")
            return False
        if data["type"] != type:
            return False
        if "extension" not in data or key not in data["extension"] or len(data["extension"][key]) == 0:
            return True
        return False
             
    def checkResult(self, data):
        for it in data["result"]:
            if self.needChangeValue(it, "text", "cover_url"):
                it["extension"]["cover_url"] = ""
            if self.needChangeValue(it, "audio", "cover_url"):
                it["extension"]["cover_url"] = ""
            if self.needChangeValue(it, "image", "cover_url"):
                it["extension"]["cover_url"] = ""
            if self.needChangeValue(it, "video", "cover_url"):
                it["extension"]["cover_url"] = ""
               
            if "extension" in it and "cover_url" in it["extension"] and len(it["extension"]["cover_url"]) > 0:
                w, h = utils.getOssImageSize(it["extension"]["cover_url"])
                if w > 0 and h > 0:
                    if "?" in str(it["extension"]["cover_url"]):
                        it["extension"]["cover_url"] += f"&width={w}&height={h}"
                        it["extension"]["width"] = w
                        it["extension"]["height"] = h
                    else:
                        it["extension"]["cover_url"] = urljoin(it["extension"]["cover_url"], f"?width={w}&height={h}")

    def cmdWithWidget(self, widget_id):
        map = store.widgetMap()
        if widget_id in map:
            path = ""
            is_block = False
            if isinstance(map[widget_id], (dict)):
                is_block = map[widget_id]["isBlock"]
                path = map[widget_id]["path"]
            else:
                is_block = False
                path = map[widget_id]
            if len(path) > 0 and is_block == False:
                return path
        return None

    def start(self, isProduct=False):
        self.is_product = isProduct
        super().start()

    def run_internal(self):
        try:
            if len(store.token()) <= 0:
                self.stop()
                return

            datas = xy_pb.GetTask(self.is_product, store.token())
            for it in datas:
                taskUUID = it["taskUUID"]
                print(f"receive task => {taskUUID}")
                pending_count = it["pending_count"]
                config = json.loads(it["config"])
                params = json.loads(it["data"])
                widget_id = config["widget_id"]
                group_id = config["group_id"]
                #cmd
                local_cmd = self.cmdWithWidget(widget_id)
                cmd = ""
                if local_cmd:
                    cmd = local_cmd
                else:
                    cmd = str(Path(config["cmd"]))
                #params
                params["task_id"] = taskUUID
                params["pending_count"] = pending_count
                #run
                print(f"start execute task : {taskUUID}")
                store.setCurrentTaskUUID(taskUUID)
                executeSuccess, result_obj = self.executeLocalPython(taskUUID, cmd, params)
                store.setCurrentTaskUUID("")
                #result
                is_ok = executeSuccess and result_obj["status"] == 0
                msg = "Unknow Error"
                if executeSuccess and len(msg) > 0:
                    msg = result_obj["message"]
                if is_ok:
                    self.checkResult(result_obj)
                print(f"notify task({taskUUID}) complate")
                print(f"notify task({taskUUID}) complate")
                if xy_pb.TaskNotify(taskUUID, 
                            is_ok, 
                            msg, 
                            json.dumps(result_obj["result"], separators=(',', ':'))):
                    if is_ok:
                        print(f"task : {taskUUID} complete success")
                    else:
                        print(f"task : {taskUUID} fail")
        except Exception as e:
            print(e)
        
    def status_ok(self):
        service_running = super()._is_running()
        socket_running = True #self.socket.isRunning()
        is_login =xy_user.User().isLogin()
        return socket_running and service_running and is_login
    

# python xxxxxx\main.py --run "{\"task_id\":1,\"widget_id\":1,\"pending_count\":1,\"fn_name\":\"test\",\"param\":{\"text\":\"Hello World\"}}"
# MecordService.executeLocalPython(None, "asdasdlasasdasdasdas", r"E:\mecord_sd\44444444444\script\main.py", {"task_id":1,"widget_id":1,"pending_count":1,"fn_name":"test","param":{"text":"Hello World"}})