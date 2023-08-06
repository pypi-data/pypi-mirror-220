# -*- coding: UTF-8 -*-
import requests
from TranslateApi import preproccess



# OCR上传
def ocrUploadImage(ip, appid,privatekey, from_, filepath, filename):
    """
    OCR上传
    :param from_:源语言
    :param filepath:本地文件地址
    :param filename:图片名称
    :return:
    """
    if filepath.split(".")[-1] in ["jpg", "jpeg", "png", "bmp"]:

        ocrUploadImageURL = "https://" + ip + "/TranslateApi/api/image/ocrUploadImage"

        nonce_str = preproccess.get_nonce_str()

        filemd5 = preproccess.file_md5(filepath)

        stringdict = {

            "appid": appid,
            "nonce_str": nonce_str,
            "from": from_,
            "md5": filemd5,
            "privatekey": privatekey
        }

        data = {
            "appid": appid,
            "nonce_str": nonce_str,
            "from": from_,
            "md5": filemd5,
            'file': (filename, open(filepath, "rb")),
            "token": preproccess.get_token(stringdict),
        }

        files = {
            filename: open(filepath, "rb")
        }

        response = requests.post(url=ocrUploadImageURL, data=data, files=files)
        return response.json()
    else:
        return "请上传符合类型的图片！！！"
