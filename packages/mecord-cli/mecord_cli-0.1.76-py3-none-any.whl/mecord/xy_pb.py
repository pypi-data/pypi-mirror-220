import json
import hashlib
import time
import socket
import requests
import urllib3
import os
import random

from mecord import uauth_common_pb2 
from mecord import uauth_ext_pb2 
from mecord import common_ext_pb2 
from mecord import aigc_ext_pb2 
from mecord import rpcinput_pb2 
from mecord import store 
from mecord import utils 
from mecord import constant 

aigc_product_domain = "https://api.mecordai.com/proxymsg"

def _aigc_post(request, function, domain=None, token=None):
    return _post(url=(domain if domain else "https://mecord-beta.2tianxin.com/proxymsg"), 
                 objStr="mecord.aigc.AigcExtObj", 
                 request=request, 
                 function=function,
                 token=token)

def _post(url, objStr, request, function, token=None):
    req = request.SerializeToString()
    opt = {
        "lang": "zh-Hans",
        "region": "CN",
        "appid": "80",
        "application": "mecord",
        "version": "1.0",
        "X-Token": token if token else store.token(),
        "uid": "1",
    }
    input_req = rpcinput_pb2.RPCInput(obj=objStr, func=function, req=req, opt=opt)
    try:
        requests.adapters.DEFAULT_RETRIES = 2
        s = requests.session()
        s.keep_alive = False
        s.headers.update({'Connection':'close'})
        res = s.post(url=url, data=input_req.SerializeToString())
        res.close()
        pb_rsp = rpcinput_pb2.RPCOutput()
        pb_rsp.ParseFromString(res.content)
        s.close()
    except UnicodeDecodeError as e:
        return -1, f"url decode error : {e}", "" 
    except socket.timeout as e:
        return -1, "mecord server timeout", "" 
    except Exception as e:
        return -1, f"mecord server error : {e}", "" 
    if pb_rsp.ret == 0:
        return 0, "", pb_rsp.rsp
    else:
        return pb_rsp.ret, pb_rsp.desc, "" 
    
def GetTask(isProduct, token):
    req = aigc_ext_pb2.GetTaskReq()
    req.version = constant.app_version
    req.DeviceKey = utils.generate_unique_id()
    map = store.widgetMap()
    for it in map:
        if isinstance(map[it], (dict)):
            if map[it]["isBlock"] == False:
                req.widgets.append(it)
        else:
            req.widgets.append(it)
    domain = None
    if isProduct:
        req.token = "NDl8NWU5OGI1ODk4N2ExNTZmZWE1MmI4YzM3MTNjNjI0MDd8ZjI2MzYwZTA2ZWVkODg0Y2ZlNjZlZTBlNzVhZDM1OWY="
        domain = aigc_product_domain
    else:
        req.token = token
    req.limit = store.multitaskNum()
    extInfo = store.readDeviceInfo()
    extInfo["app_version"] = constant.app_version
    extInfo["app_bulld_number"] = constant.app_bulld_number
    extInfo["app_name"] = constant.app_name
    req.extend = json.dumps(extInfo)

    rsp = aigc_ext_pb2.GetTaskRes()
    r1, r2, r3 = _aigc_post(req, "GetTask", domain, req.token)
    if r1 != 0:
        print(f'GetTask failed: {r1} {r2}')
        return []
    rsp.ParseFromString(r3)
    datas = []
    for it in rsp.list:
        datas.append({
            "taskUUID": it.taskUUID,
            "pending_count": rsp.count - rsp.limit,
            "config": it.config,
            "data": it.data,
        })
    return datas

def TaskNotify(taskUUID, status, msg, dataStr):
    req = aigc_ext_pb2.TaskNotifyReq()
    req.version = constant.app_version
    req.taskUUID = taskUUID
    if status:
        req.taskStatus = common_ext_pb2.TaskStatus.TS_Success
    else:
        req.taskStatus = common_ext_pb2.TaskStatus.TS_Failure
    req.failReason = msg
    req.data = dataStr

    rsp = aigc_ext_pb2.TaskNotifyRes()
    r1, r2, r3 = _aigc_post(req, "TaskNotify")
    if r1 != 0:
        print(f'task notify failed: {r1} {r2}')
        return False
    rsp.ParseFromString(r3)
    return True

def DeviceUnbind():
    req = aigc_ext_pb2.AigcDeviceUnBindReq()
    req.deviceToken = store.token()

    rsp = aigc_ext_pb2.AigcDeviceUnBindRes()
    r1, r2, r3 = _aigc_post(req, "DeviceUnBind")
    if r1 != 0:
        print(f'DeviceUnBind failed: {r1} {r2}')
        return False
    rsp.ParseFromString(r3)
    return False

def GetAigcDeviceInfo():
    req = aigc_ext_pb2.AigcDeviceInfoReq()
    req.version = constant.app_version
    req.deviceKey = utils.generate_unique_id()
    extInfo = store.readDeviceInfo()
    extInfo["app_version"] = constant.app_version
    extInfo["app_bulld_number"] = constant.app_bulld_number
    extInfo["app_name"] = constant.app_name
    req.extend = json.dumps(extInfo)

    rsp = aigc_ext_pb2.AigcDeviceInfoRes()
    r1, r2, r3 = _aigc_post(req, "DeviceInfo")
    if r1 != 0:
        if r1 != 11000:
            print(f'get DeviceInfo failed: {r1} {r2}')
        return False
    rsp.ParseFromString(r3)
    
    if len(rsp.groupUUID) > 0:
        sp = store.Store()
        data = sp.read()
        data["groupUUID"] = rsp.groupUUID
        data["token"] = rsp.token
        if rsp.isCreateWidget == True:
            data["isCreateWidget"] = rsp.isCreateWidget
        sp.write(data)
        return True
    return False

def CreateWidgetUUID():
    req = aigc_ext_pb2.ApplyWidgetReq()
    rsp = aigc_ext_pb2.ApplyWidgetRes()
    r1, r2, r3 = _aigc_post(req, "ApplyWidget")
    if r1 != 0:
        print(f'CreateWidgetUUID failed: {r1} {r2}')
        return ""
    rsp.ParseFromString(r3)
    return rsp.widgetUUID

def DeleteWidget(widgetid):
    req = aigc_ext_pb2.DeleteAigcWidgetReq()
    req.widgetUUID = widgetid
    req.deviceToken = store.token()
    rsp = aigc_ext_pb2.DeleteAigcWidgetRes()
    r1, r2, r3 = _aigc_post(req, "DeleteWidget")
    if r1 != 0:
        print(f'DeleteWidget failed: {r1} {r2}')
        return False
    rsp.ParseFromString(r3)
    return True

def GetTaskCount(widgetid):
    req = aigc_ext_pb2.TaskCountReq()
    req.deviceToken = store.token()
    rsp = aigc_ext_pb2.TaskCountRes()
    r1, r2, r3 = _aigc_post(req, "TaskCount")
    if r1 != 0:
        print(f'GetTaskCount failed: {r1} {r2}')
        return []
    rsp.ParseFromString(r3)
    datas = []
    for it in rsp.items:
        datas.append({
            "widgetUUID": it.widgetUUID,
            "taskCount": it.taskCount
        })
    return datas

def RemoteWidgetList(widgetid):
    req = aigc_ext_pb2.AigcWidgetListReq()
    req.deviceToken = store.token()
    rsp = aigc_ext_pb2.AigcWidgetListRes()
    r1, r2, r3 = _aigc_post(req, "WidgetList")
    if r1 != 0:
        print(f'RemoteWidgetList failed: {r1} {r2}')
        return []
    rsp.ParseFromString(r3)
    datas = []
    for it in rsp.items:
        datas.append({
            "uuid": it.uuid,
            "name": it.name,
            "updated_at": it.updated_at,
        })
    return datas

def ExpansionWithToken(token):
    req = aigc_ext_pb2.AigcDeviceExpansionReq()
    req.DeviceToken = token
    req.DeviceKey = utils.generate_unique_id()

    rsp = aigc_ext_pb2.AigcDeviceExpansionRes()
    r1, r2, r3 = _aigc_post(req, "DeviceExpansion")
    if r1 == 11000:
        return False, r1
    elif r1 != 0:
        print(f'add token failed: {r1} {r2}')
        return ""
    rsp.ParseFromString(r3)

    if len(rsp.groupUUID) > 0:
        sp = store.Store()
        data = sp.read()
        data["groupUUID"] = rsp.groupUUID
        data["token"] = rsp.deviceToken
        sp.write(data)
        return True, 0
    return False, -1
 
def GetOssUrl(ext):
    req = aigc_ext_pb2.UploadFileUrlReq()
    req.token = store.token()
    req.version = constant.app_version
    req.fileExt = ext

    rsp = aigc_ext_pb2.UploadFileUrlRes()
    r1, r2, r3 = _aigc_post(req, "UploadFileUrl")
    if r1 != 0:
        print(f'GetOssUrl failed: {r1} {r2}')
        return "", ""
    rsp.ParseFromString(r3)
    return rsp.url, rsp.contentType
   
def GetWidgetOssUrl(widgetid):
    req = aigc_ext_pb2.UploadWidgetUrlReq()
    req.version = constant.app_version
    req.widgetUUID = widgetid

    rsp = aigc_ext_pb2.UploadWidgetUrlRes()
    r1, r2, r3 = _aigc_post(req, "UploadWidgetUrl")
    if r1 != 0:
        print(f'GetWidgetOssUrl failed: {r1} {r2}')
        return "", ""
    rsp.ParseFromString(r3)
    return rsp.url, rsp.contentType

def WidgetUploadEnd(url):
    req = aigc_ext_pb2.UploadWidgetReq()
    req.version = constant.app_version
    req.fileUrl = url
    
    rsp = aigc_ext_pb2.UploadWidgetRes()
    r1, r2, r3 = _aigc_post(req, "UploadWidget")
    if r1 != 0:
        print(f'WidgetUploadEnd failed: {r1} {r2}')
        return 0
    rsp.ParseFromString(r3)
    return rsp.checkId
    
def UploadWidgetCheck(checkId):
    req = aigc_ext_pb2.UploadWidgetCheckReq()
    req.version = constant.app_version
    req.checkId = checkId

    rsp = aigc_ext_pb2.UploadWidgetCheckRes()
    r1, r2, r3 = _aigc_post(req, "UploadWidgetCheck")
    if r1 != 0:
        print(f'UploadWidgetCheck failed: {r1} {r2}')
        return 0
    rsp.ParseFromString(r3)
    if rsp.status == aigc_ext_pb2.UploadWidgetStatus.UWS_SUCCESS:
        return 1
    elif rsp.status == aigc_ext_pb2.UploadWidgetStatus.UWS_FAILURE:
        print(f"widget pulish fail msg => {rsp.failReason}")
        return 0
    else:
        return -1

def UploadMarketModel(name, cover, model_url, type, taskuuid):
    req = aigc_ext_pb2.MarketModelCreateWithTaskReq()
    req.name = name
    req.cover = cover
    req.url = model_url
    req.type = type
    req.TaskUUID = taskuuid

    rsp = aigc_ext_pb2.MarketModelCreateWithTaskRes()
    r1, r2, r3 = _aigc_post(req, "MarketModelCreateWithTask")
    if r1 != 0:
        print(f'MarketModelCreateWithTask failed: {r1} {r2}')
        return 0
    rsp.ParseFromString(r3)
    return True
