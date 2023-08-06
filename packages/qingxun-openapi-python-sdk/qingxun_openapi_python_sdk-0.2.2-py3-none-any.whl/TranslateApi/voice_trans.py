# -*- coding: UTF-8 -*-
import requests
import asyncio
from TranslateApi import preproccess
import websockets
import json



# 语音识别翻译
def getConnectionId(ip,appid,privatekey,fromLang,toLang):

    getConnectionIdURL = "http://"+ip + "/TranslateApi/api/voice/online/getConnectionId"

    nonce_str = preproccess.get_nonce_str()

    stringdict = {

        "appid": appid,
        "nonce_str": nonce_str,
        "from": fromLang,
        "to": toLang,
        "privatekey": privatekey,
    }

    data = {
        "appid": appid,
        "token": preproccess.get_token(stringdict),
        "nonce_str": nonce_str,
        "from": fromLang,
        "to": toLang,
    }

    response = requests.post(url=getConnectionIdURL, data=data)

    return response

# 向服务器端发送消息
async def clientSend(websocket,text):

    await websocket.send(text)

# 接收服务端信息
async def getRecv(websocket):
    response = await websocket.recv()
    return response

def getWebscoketURL(ip,appid,privatekey,connectionId):
    nonce_str = preproccess.get_nonce_str()

    stringdict = {
        "appid": appid,
        "nonce_str": nonce_str,
        "privatekey": privatekey,
    }

    wss_url = "wss://" + ip + "/TranslateApi/api/voice/trans/online/" + connectionId + f"/?appid={appid}&token={preproccess.get_token(stringdict)}&nonce_str={nonce_str}"
    return wss_url

# 获取译文音频链接接口
def getTransAudioLink(ip, appid, privatekey, recordId):

    getTransAudioLinkURL = "https://" + ip + "/TranslateApi/api/voice/online/getTransAudioLink"

    nonce_str = preproccess.get_nonce_str()

    stringdict = {

        "appid": appid,
        "nonce_str": nonce_str,
        "recordId": recordId,
        "privatekey": privatekey,
    }

    data = {
        "appid": appid,
        "token": preproccess.get_token(stringdict),
        "nonce_str": nonce_str,
        "recordId": recordId

    }

    response = requests.post(url=getTransAudioLinkURL, data=data)

    return response