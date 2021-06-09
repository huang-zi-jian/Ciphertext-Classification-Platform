'''
author: feifei
date: 2021-2-24
file info: DES加密/解密
'''

from Crypto.Cipher import DES
from Crypto.Util.Padding import pad,unpad
from Crypto import Random
import binascii

# MD5最终digest结果为16bytes，也就是32个十六进制数，SHA1最终digest结果为20bytes，SHA512最终digest结果为64bytes
# MD5.block_size, SHA1.block_size,SHA512.block_size

#DES的block_size只能为8，所以pad中的BLOCK_SIZE必须是8的倍数，而且秘钥key也只能选择8
class DES_ECB_class(object):

    def __init__(self):
        self.BLOCK_SIZE = 8

    def encrypt(self,key,data):

        # 加密需要去生成一个DES对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        des = DES.new(key.encode(encoding='utf-8'), DES.MODE_ECB)

        # 加密的过程，pad对数据进行转化，block_size补充数据位数
        # encrypt将数据转化为ASCII编码encrypto_text为ASCII码bytes型数据
        encrypto_data = b''
        if type(data) is str:
            encrypto_data = des.encrypt(pad(data.encode(encoding='utf-8'), self.BLOCK_SIZE))

        elif type(data) is bytes:
            encrypto_data = des.encrypt(pad(data, self.BLOCK_SIZE))

        encrypto_data = binascii.b2a_hex(encrypto_data)
        encrypto_data = encrypto_data.decode(encoding='utf-8')

        return encrypto_data

    def decrypt(self, key, encrypto_data):

        # 解密需要去生成一个DES对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        des = DES.new(key.encode(encoding='utf-8'), DES.MODE_ECB)
        # print(binascii.b2a_hex(encrypto_data),encrypto_data.hex())
        # encrypto_data.hex()返回的是binascii.b2a_hex(encrypto_data)的字符串形式
        encrypto_data = encrypto_data.encode(encoding='utf-8')
        encrypto_data = binascii.a2b_hex(encrypto_data)

        # 加密时是先pad再encrypt加密，所以解密时我们就先decrypt解密再unpad
        decrypto_data = unpad(des.decrypt(encrypto_data),self.BLOCK_SIZE).decode(encoding='utf-8')

        return decrypto_data


iv = b'-X\xb1\x13\xe8\xe2\xb4\\'

class DES_CBC_class(object):

    def __init__(self):
        self.BLOCK_SIZE = 8

    def encrypt(self,key,data):

        # 生成长度等于DES块大小(DES.block_size)的不可重复的密钥向量
        # iv = Random.new().read(DES.block_size)

        global iv
        # 加密需要去生成一个DES对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        des = DES.new(key.encode(encoding='utf-8'), DES.MODE_CBC, iv)

        # 加密的过程，pad对数据进行转化，block_size补充数据位数
        # encrypt将数据转化为ASCII编码encrypto_text为ASCII码bytes型数据
        encrypto_data = b''
        if type(data) is str:
            encrypto_data = iv + des.encrypt(pad(data.encode(encoding='utf-8'), self.BLOCK_SIZE))

        elif type(data) is bytes:
            encrypto_data = iv + des.encrypt(pad(data, self.BLOCK_SIZE))

        return encrypto_data

    def decrypt(self, key, encrypto_data):
        # 解密需要去生成一个DES对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        des = DES.new(key.encode(encoding='utf-8'), DES.MODE_CBC, encrypto_data[:self.BLOCK_SIZE])
        # print(binascii.b2a_hex(encrypto_data),encrypto_data.hex())
        # encrypto_data.hex()返回的是binascii.b2a_hex(encrypto_data)的字符串形式

        # 加密时是先pad再encrypt加密，所以解密时我们就先decrypt解密再unpad
        decrypto_data = unpad(des.decrypt(encrypto_data[self.BLOCK_SIZE:]),self.BLOCK_SIZE)

        return decrypto_data


if __name__ == '__main__':

    # DES秘钥必须是8字节的
    key = 'mefeifei'
    data = '邓怡菲穿小棉袄！'

    print("-----EBC模式下的DES加密-----")

    des_ECB_object = DES_ECB_class()
    encrypto_data = des_ECB_object.encrypt(key,data)
    print('十六进制密文：',encrypto_data)

    decrypto_data = des_ECB_object.decrypt(key,encrypto_data)
    print('原明文：',decrypto_data)

    print("-----CBC模式下的DES加密-----")

    des_CBC_object = DES_CBC_class()
    encrypto_data = des_CBC_object.encrypt(key,data)
    print('iv：',binascii.b2a_hex(encrypto_data[:8]))
    print('十六进制密文：', encrypto_data[8:])
    print('ASCII密文：', binascii.b2a_hex(encrypto_data[8:]))

    # 返回解密后的明文
    decrypto_data = des_CBC_object.decrypt(key, encrypto_data)
    print('十六进制明文：', decrypto_data)
    print('ASCII明文：', binascii.b2a_hex(decrypto_data))
    print('原明文：', decrypto_data.decode('utf-8'))









