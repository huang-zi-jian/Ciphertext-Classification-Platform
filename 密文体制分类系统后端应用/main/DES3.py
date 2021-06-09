'''
author: feifei
date: 2021-2-24
file info: 3DES加密/解密
'''

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad,unpad
from Crypto import Random
import binascii

#3DES的block_size只能为8，所以pad中的BLOCK_SIZE必须是8的倍数，key_size可以选择16和24
class DES3_ECB_class(object):
    def __init__(self):
        self.BLOCK_SIZE = 8

    def encrypt(self,key,data):
        # 需要去生成一个DES3对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        des3 = DES3.new(key.encode(encoding='utf-8'), DES3.MODE_ECB)

        # 加密的过程，pad对数据进行转化，block_size补充数据位数
        # encrypt将数据转化为ASCII编码encrypto_text为ASCII码bytes型数据
        encrypto_data = b''
        if type(data) is str:
            encrypto_data = des3.encrypt(pad(data.encode(encoding='utf-8'), self.BLOCK_SIZE))

        elif type(data) is bytes:
            encrypto_data = des3.encrypt(pad(data, self.BLOCK_SIZE))

        encrypto_data = binascii.b2a_hex(encrypto_data)
        encrypto_data = encrypto_data.decode(encoding='utf-8')

        return encrypto_data


    def decrypt(self,key,encrypto_data):

        des3 = DES3.new(key.encode(encoding='utf-8'), DES3.MODE_ECB)

        encrypto_data = encrypto_data.encode(encoding='utf-8')
        encrypto_data = binascii.a2b_hex(encrypto_data)

        decrypto_data = unpad(des3.decrypt(encrypto_data), self.BLOCK_SIZE).decode(encoding='utf-8')

        # unpad返回的是二进制数据，需要decode解码为str
        return decrypto_data



iv = b'-X\xb1\x13\xe8\xe2\xb4\\'

class DES3_CBC_class(object):

    def __init__(self):
        self.BLOCK_SIZE = 8

    def encrypt(self,key,data):

        # 生成长度等于DES块大小(DES.block_size)的不可重复的密钥向量
        # iv = Random.new().read(DES3.block_size)

        global iv
        # 加密需要去生成一个DES对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        des3 = DES3.new(key.encode(encoding='utf-8'), DES3.MODE_CBC, iv)

        # 加密的过程，pad对数据进行转化，block_size补充数据位数
        # encrypt将数据转化为ASCII编码encrypto_text为ASCII码bytes型数据
        encrypto_data = b''
        if type(data) is str:
            encrypto_data = iv + des3.encrypt(pad(data.encode(encoding='utf-8'), self.BLOCK_SIZE))

        elif type(data) is bytes:
            encrypto_data = iv + des3.encrypt(pad(data, self.BLOCK_SIZE))

        return encrypto_data

    def decrypt(self, key, encrypto_data):
        # 解密需要去生成一个DES对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        des = DES3.new(key.encode(encoding='utf-8'), DES3.MODE_CBC, encrypto_data[:self.BLOCK_SIZE])
        # print(binascii.b2a_hex(encrypto_data),encrypto_data.hex())
        # encrypto_data.hex()返回的是binascii.b2a_hex(encrypto_data)的字符串形式

        # 加密时是先pad再encrypt加密，所以解密时我们就先decrypt解密再unpad
        decrypto_data = unpad(des.decrypt(encrypto_data[self.BLOCK_SIZE:]),self.BLOCK_SIZE)

        return decrypto_data


if __name__ == '__main__':

    key = '123456781234567a'
    data = '邓怡菲穿小棉袄！'

    print("-----ECB模式下的3DES加密-----")

    des3_ECB_object = DES3_ECB_class()
    encrypto_data = des3_ECB_object.encrypt(key,data)
    print('密文：',encrypto_data)

    decrypto_data = des3_ECB_object.decrypt(key,encrypto_data)
    print('明文：',decrypto_data)

    print("-----CBC模式下的3DES加密-----")

    des3_CBC_object = DES3_CBC_class()
    encrypto_data = des3_CBC_object.encrypt(key, data)
    print('iv：', binascii.b2a_hex(encrypto_data[:8]))
    print('十六进制密文：', encrypto_data[8:])
    print('ASCII密文：', binascii.b2a_hex(encrypto_data[8:]))

    # 返回解密后的明文
    decrypto_data = des3_CBC_object.decrypt(key, encrypto_data)
    print('十六进制明文：', decrypto_data)
    print('ASCII明文：', binascii.b2a_hex(decrypto_data))
    print('原明文：', decrypto_data.decode('utf-8'))







