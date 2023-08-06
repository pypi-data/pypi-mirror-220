# -*- coding: UTF-8 -*-
import requests
from TranslateApi import preproccess


# 文字翻译
def trans(ip,appid,privatekey,fromLang,toLang,text):
    """
    文字翻译
    :param from_: 源语言
    :param to: 目标语言
    :param text: 文字
    :return:
    """
    transURL = "https://" + ip + "/TranslateApi/api/trans"

    nonce_str = preproccess.get_nonce_str()

    stringdict = {

        "appid": appid,
        "nonce_str": nonce_str,
        "from": fromLang,
        "to": toLang,
        "text": text,
        "privatekey": privatekey
    }

    data = {
        "appid": appid,
        "nonce_str": nonce_str,
        "token": preproccess.get_token(stringdict),
        "from": fromLang,
        "to": toLang,
        "text": text,
    }
    response = requests.post(transURL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})

    return response
