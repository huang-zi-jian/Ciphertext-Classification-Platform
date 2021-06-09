'''
author: feifei
date: 2021-1-15
file info: RC4加密/解密
'''

from Crypto.Cipher import ARC4
from Crypto.Util.Padding import pad, unpad
from Crypto import Random
import binascii


# RC4的block_size为1
class RC4_class(object):

    def __init__(self):
        self.BLOCK_SIZE = 1

    def encrypt(self, key, data):

        # 加密需要去生成一个DES对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        rc4 = ARC4.new(key.encode(encoding='utf-8'))

        # 加密的过程，pad对数据进行转化，block_size补充数据位数
        # encrypt将数据转化为ASCII编码encrypto_text为ASCII码bytes型数据
        encrypto_data = b''
        if type(data) is str:
            encrypto_data = rc4.encrypt(data.encode(encoding='utf-8'))

        elif type(data) is bytes:
            encrypto_data = rc4.encrypt(data)

        encrypto_data = binascii.b2a_hex(encrypto_data)
        encrypto_data = encrypto_data.decode(encoding='utf-8')

        return encrypto_data

    def decrypt(self, key, encrypto_data):
        # 解密需要去生成一个DES对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        rc4 = ARC4.new(key.encode(encoding='utf-8'))
        # print(binascii.b2a_hex(encrypto_data),encrypto_data.hex())
        # encrypto_data.hex()返回的是binascii.b2a_hex(encrypto_data)的字符串形式

        encrypto_data = encrypto_data.encode(encoding='utf-8')
        encrypto_data = binascii.a2b_hex(encrypto_data)

        # 加密时是先pad再encrypt加密，所以解密时我们就先decrypt解密再unpad
        decrypto_data = rc4.decrypt(encrypto_data).decode(encoding='utf-8')

        return decrypto_data


if __name__ == '__main__':
    key = '1234567812345678'
    data = '邓怡菲穿小棉袄！'

    RC4_object = RC4_class()
    encrypto_data = RC4_object.encrypt(key, data)
    print(encrypto_data)

    decrypto_data = RC4_object.decrypt(key, encrypto_data)
    print(decrypto_data)
