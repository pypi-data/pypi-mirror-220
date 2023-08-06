# -*- coding: UTF-8 -*-
import requests
from TranslateApi import preproccess


# 词典
def findDict(ip,appid,privatekey,word):

    # 词典，小于等于15个字符
    if len(word) > 0 and len(word) < 16:
        dict_searchURL = "https://"+ip + "/TranslateApi/api/dict/search"

        nonce_str = preproccess.get_nonce_str()

        stringdict = {

            "appid": appid,
            "nonce_str": nonce_str,
            "word": word,
            "privatekey": privatekey
        }

        data = {
            "appid": appid,
            "nonce_str": nonce_str,
            "word": word,
            "token": preproccess.get_token(stringdict)
        }


        response = requests.post(url=dict_searchURL, data=data)
        return response
    else:
        return "参数word不符合规格，字符数需大于0小于等于15！！！"