# -*- coding: UTF-8 -*-
import random
import string
import hashlib

def file_md5(file_name):
    with open(file_name, 'rb') as fp:
        data = fp.read()
    file_md5 = hashlib.md5(data).hexdigest()
    return file_md5.lower()


def get_token(stringdict):
    stringA = ""
    for key in sorted(stringdict.keys()):
        stringA += key + "=" + str(stringdict.get(key)) + "&"

    token = hashlib.md5(stringA[:-1].encode("utf-8")).hexdigest().upper()

    return token


def get_nonce_str():
    return ''.join(random.choice(string.ascii_letters) for x in range(16))