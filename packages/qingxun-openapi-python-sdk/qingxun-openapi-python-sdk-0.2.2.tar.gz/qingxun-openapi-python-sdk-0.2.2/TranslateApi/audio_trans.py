# -*- coding: UTF-8 -*-
import requests
from TranslateApi import preproccess


# 音频识别翻译
# 音频文件上传接口
def audio_upload(ip,appid,privatekey,fromLang,toLang,filepath):

    uploadURL = "https://"+ ip + "/TranslateApi/api/voice/audio/upload"

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

    files = {
        "file": open(filepath, "rb")
    }

    response = requests.post(url=uploadURL, data=data, files=files)

    return response.json()

# 音频翻译任务查询接口
def audio_queryProgress(ip,appid,privatekey,recordId):

    queryProgressURL = "https://" + ip + "/TranslateApi/api/voice/audio/queryProgress"

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

    response = requests.post(url=queryProgressURL, data=data)

    return response.json()

# 音频下载译文链接接口
def audio_download(ip,appid,privatekey,recordId):

    audio_downloadURL = "https://" + ip + "/TranslateApi/api/voice/audio/download"

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

    response = requests.post(url=audio_downloadURL, data=data)

    return response

