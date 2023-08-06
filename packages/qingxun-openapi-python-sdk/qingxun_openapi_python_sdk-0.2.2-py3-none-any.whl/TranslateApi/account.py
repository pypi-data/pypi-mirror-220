import requests
from TranslateApi import preproccess

#获取账户信息
def getAccount(ip,appid,privatekey,**params):
    """
    获取账户信息
    :param params:type(资源包类型 1.文档翻译 2.文字翻译 3.图片翻译 4.格式转换)
    :return:
    """
    getAccountURL = "https://"+ip + "/TranslateApi/api/getAccount"

    nonce_str = preproccess.get_nonce_str()

    stringdict = {

        "appid": appid,
        "nonce_str": nonce_str,
        "privatekey": privatekey
    }
    for key in params.keys():
        stringdict[key] = params.get(key)

    data = {
        "appid": appid,
        "nonce_str": nonce_str,
        "token": preproccess.get_token(stringdict),
    }

    for key in params.keys():
        data[key] = params.get(key)

    response = requests.post(getAccountURL, data=data,
                             headers={"Content-Type": "application/x-www-form-urlencoded"})

    return response