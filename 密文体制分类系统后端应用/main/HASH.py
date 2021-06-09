'''
author: feifei
date: 2021-2-25
file info: hash加密
'''

from Crypto.Hash import MD5,SHA1,SHA512


# MD5加密
def Md5(data):
    md5 = MD5.new()
    md5.update(data.encode(encoding='utf-8'))
    encryp_data = md5.hexdigest()

    return encryp_data


# SHA1加密
def Sha1(data):
    sha1 = SHA1.new()
    sha1.update(data.encode(encoding='utf-8'))
    encryp_data = sha1.hexdigest()

    return encryp_data


# SHA512加密
def Sha512(data):
    sha512 = SHA512.new()
    sha512.update(data.encode(encoding='utf-8'))
    encryp_data = sha512.hexdigest()

    return encryp_data