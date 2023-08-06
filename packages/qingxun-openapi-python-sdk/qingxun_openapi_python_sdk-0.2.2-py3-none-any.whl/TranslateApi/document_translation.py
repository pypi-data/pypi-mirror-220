# -*- coding: UTF-8 -*-
import requests
from TranslateApi import preproccess

# 文件上传
def uploadTranslate(ip,appid,privatekey, fromLang, toLang, filepath, filename, **params):
    """
    文件上传并翻译
    :param from_:源语言
    :param to:目标语言
    :param filepath:本地文件地址
    :param filename:文件名
    :param params:可选参数（industryId，transImg，excelMode，bilingualControl）
    :return:
    """

    # 文档上传有四个追加参数
    # industryId	行业代码	int	见行业列表	否
    # transImg	文档内图片翻译	int	0：不翻译文档内图片（默认），1：翻译文档内图片。目前支持中、英、日、韩的文档内图片翻译。（如有需要请联系销售开通）
    # excelMode	指定excel翻译模式	int	0：只翻译当前打开sheet（默认），1：翻译全部sheet（页数按全部sheet字符数来计算）
    # bilingualControl	指定翻译模式	int	0：译文单独为一个文档（默认），1：双语对照（原文和译文在一个文档）
    # 可以在参数后边用（industryId = 0 ,transImg=0 , excelMode = 0,bilingualControl=0）进行追加

    uploadTranslateURL = "https://" + ip + "/TranslateApi/api/uploadTranslate"

    filemd5 = preproccess.file_md5(filepath)

    nonce_str = preproccess.get_nonce_str()

    stringdict = {
        "appid": appid,
        "nonce_str": nonce_str,
        "from": fromLang,
        "to": toLang,
        "md5": filemd5,
        "privatekey": privatekey
    }
    for key in params.keys():
        stringdict[key] = params.get(key)

    data = {
        "appid": appid,
        "token": preproccess.get_token(stringdict),
        "nonce_str": nonce_str,
        "from": fromLang,
        "to": toLang,
        "md5": filemd5,

    }

    files = {
        filename: open(filepath, "rb")
    }

    for key in params.keys():
        data[key] = params.get(key)

    response = requests.post(url=uploadTranslateURL, data=data, files=files)
    return response

# 获取进度
def queryTransProgress(ip,appid,privatekey, tid):
    """
    获取翻译进度
    :param tid: 文档id
    :return:
    """

    nonce_str = preproccess.get_nonce_str()

    stringdict = {
        "appid": appid,
        "nonce_str": nonce_str,
        "tid": tid,
        "privatekey": privatekey
    }

    data = {

        "appid": appid,
        "token": preproccess.get_token(stringdict),
        "nonce_str": nonce_str,
        "tid": tid,
    }

    return requests.post("https://" + ip + "/TranslateApi/api/queryTransProgress", data=data)

# 下载
def downloadFile(ip, appid,privatekey, tid, dtype):
    """
    下载翻译后的文档
    :param tid: 文档id
    :param dtype: 类型
    :return:
    """

    downloadFileURL = "https://" + ip + "/TranslateApi/api/downloadFile"
    nonce_str = preproccess.get_nonce_str()
    stringdict = {
        "appid": appid,
        "nonce_str": nonce_str,
        "dtype": dtype,
        "tid": tid,
        "privatekey": privatekey
    }

    data = {
        "appid": appid,
        "nonce_str": nonce_str,
        "token": preproccess.get_token(stringdict),
        "dtype": dtype,
        "tid": tid,

    }

    r = requests.post(downloadFileURL, data=data)
    if r.status_code == 200:
        if r.headers["Content-Type"] in 'application/octet-stream;charset=UTF-8':
            return r.content
        else:
            print("下载失败！")
            return None
    else:
        return None
#上传文件检测页数
def detectDocPage(ip,appid,privatekey,filepath,filename,excelMode=0):

    """
    上传文件检测页数
    :param filepath: 本地文件地址
    :param filename: 文件名
    :param excelMode: 指定excel翻译模式
    :return:
    """

    detectDocPageURL = "https://"+ ip + "/TranslateApi/api/detectDocPage"

    nonce_str = preproccess.get_nonce_str()

    filemd5 = preproccess.file_md5(filepath)

    stringdict = {

        "appid": appid,
        "nonce_str": nonce_str,
        "md5": filemd5,
        "excelMode": excelMode,
        "privatekey": privatekey
    }

    data = {
        "appid": appid,
        "nonce_str": nonce_str,
        "token": preproccess.get_token(stringdict),
        "md5": filemd5,
        "excelMode": excelMode,
    }

    files = {
        filename: open(filepath, "rb")
    }



    response = requests.post(url=detectDocPageURL, data=data, files=files)
    return response.json()

# 检测页数文件提交翻译
def submitForDetectDoc(ip,appid,privatekey,tid,fromLang,toLang,**params):

    """
    检测页数文件提交翻译
    :param tid:文档id
    :param from_:源语言
    :param to:目标语言
    :param params:可选参数（industryIdindustryId,transImg,excelMode,bilingualControl）
    :return:
    """
    # industryId 行业代码 int 见行业列表 否
    # transImg 文档内图片翻译 int 0：不翻译文档内图片（默认），1：翻译文档内图片。目前支持中、英、日、韩的文档内图片翻译。（如有需要请联系销售开通）    否
    # excelMode 指定excel翻译模式 int 0：只翻译当前打开sheet（默认），1：翻译全部sheet（页数按全部sheet字符数来计算）    否
    # bilingualControl  指定翻译模式int 0：译文单独为一个文档（默认），1：双语对照（原文和译文在一个文档）    否

    submitForDetectDocURL = "https://"+ ip + "/TranslateApi/api/submitForDetectDoc"

    nonce_str = preproccess.get_nonce_str()

    stringdict = {

        "appid": appid,
        "nonce_str": nonce_str,
        "tid": tid,
        "from": fromLang,
        "to": toLang,
        "privatekey": privatekey
    }

    for key in params.keys():
        stringdict[key] = params.get(key)

    data = {
        "appid": appid,
        "token": preproccess.get_token(stringdict),
        "nonce_str": nonce_str,
        "tid": tid,
        "from": fromLang,
        "to": toLang,
    }

    for key in params.keys():
        data[key] = params.get(key)

    response = requests.post(submitForDetectDocURL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})

    return response.json()