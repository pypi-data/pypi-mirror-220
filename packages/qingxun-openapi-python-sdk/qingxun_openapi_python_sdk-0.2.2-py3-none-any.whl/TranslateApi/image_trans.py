import requests
from TranslateApi import preproccess

# 图片上传并翻译
def uploadTranslateImage(ip,appid,privatekey,from_,to,filepath,filename):
    """

    :param from_:源语言
    :param to:目标语言
    :param filepath:图片路径
    :param filename:图片名称
    :return:
    """

    if filepath.split(".")[-1] in ["jpg","jpeg","png","bmp"]:

        uploadTranslateImageURL = "https://"+ip + "/TranslateApi/api/image/uploadTranslateImage"

        nonce_str = preproccess.get_nonce_str()

        filemd5 = preproccess.file_md5(filepath)

        stringdict = {

            "appid": appid,
            "nonce_str": nonce_str,
            "from": from_,
            "to": to,
            "md5": filemd5,
            "privatekey": privatekey
        }

        data = {
            "appid": appid,
            "nonce_str": nonce_str,
            "from": from_,
            "to": to,
            "md5": filemd5,
            "token": preproccess.get_token(stringdict),
        }

        files = {
            filename: open(filepath, "rb")
        }

        response = requests.post(url=uploadTranslateImageURL, data=data, files=files)
        return response.json()
    else:
        return "请上传符合类型的图片！！！"

#图片翻译获取进度
def queryImageTransProgress(ip,appid,privatekey,tid):
    """
    图片翻译获取进度
    :param tid:图片id
    :return:
    """
    queryImageTransProgressURL ="https://"+ ip + "/TranslateApi/api/image/queryImageTransProgress"


    nonce_str = preproccess.get_nonce_str()

    stringdict = {

        "appid": appid,
        "nonce_str": nonce_str,
        "tid": tid,
        "privatekey": privatekey
    }


    data = {
        "appid": appid,
        "nonce_str": nonce_str,
        "tid": tid,
        "token": preproccess.get_token(stringdict),
    }


    response = requests.post(url=queryImageTransProgressURL, data=data)
    return response.json()

#图片翻译下载
def downloadImage(ip,appid,privatekey,tid):

    """
    图片翻译下载
    :param tid: 图片id
    :return:
    """
    downloadImageURL = "https://"+ip + "/TranslateApi/api/image/downloadImage"

    nonce_str = preproccess.get_nonce_str()
    stringdict = {
        "appid": appid,
        "nonce_str": nonce_str,
        "tid": tid,
        "privatekey": privatekey
    }

    data = {
        "appid": appid,
        "nonce_str": nonce_str,
        "tid": tid,
        "token": preproccess.get_token(stringdict),
    }


    r = requests.post(downloadImageURL, data=data )

    if r.headers["Content-Type"] in 'application/octet-stream;charset=UTF-8':
        return r.content
    else:
        return "下载失败！"