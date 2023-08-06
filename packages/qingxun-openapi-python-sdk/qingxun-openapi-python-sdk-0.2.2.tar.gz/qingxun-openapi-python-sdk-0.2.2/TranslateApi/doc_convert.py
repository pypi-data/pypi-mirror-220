# -*- coding: UTF-8 -*-
import requests
from TranslateApi import preproccess



# 文档转换
def convert(ip,appid,privatekey,filepath,filename,conversionFormat,**params):

    """
    文档转换
    :param filepath:本地文件地址
    :param filename:文件名
    :param conversionFormat:转换的目标格式
    :param params:一个可选参数（from）源文件的语言（扫描件需设置语言）
    :return:
    """

    convertURL = "https://"+ ip + "/TranslateApi/api/convert"

    nonce_str = preproccess.get_nonce_str()

    filemd5 = preproccess.file_md5(filepath)

    stringdict = {

        "appid": appid,
        "nonce_str": nonce_str,
        "conversionFormat":conversionFormat,
        "md5": filemd5,
        "privatekey": privatekey
    }
    for key in params.keys():
        stringdict[key] = params.get(key)

    data = {
        "appid": appid,
        "nonce_str": nonce_str,
        "conversionFormat":conversionFormat,
        "md5": filemd5,
        'file': (filename, open(filepath, "rb")),
        "token": preproccess.get_token(stringdict),
    }

    files = {
        filename: open(filepath, "rb")
    }

    for key in params.keys():
        data[key] = params.get(key)


    response = requests.post(url=convertURL, data=data, files=files)
    return response
