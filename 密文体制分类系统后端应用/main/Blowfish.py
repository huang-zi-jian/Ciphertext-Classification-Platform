'''
author: feifei
date: 2021-1-13
file info: Blowfish加密/解密
'''
from Crypto.Cipher import Blowfish
from Crypto import Random
import binascii
from Crypto.Util.Padding import pad,unpad


class Blowfish_ECB_class(object):

    def __init__(self):
        self.BLOCK_SIZE = 8

    def encrypt(self,key,data):

        # 加密需要去生成一个Blowfish对象，MODE_ECB表示ECB模式，还可选择MODE_CBC
        blowfish = Blowfish.new(key.encode(encoding='utf-8'), Blowfish.MODE_ECB)

        # 加密的过程，pad对数据进行转化，block_size补充数据位数
        # encrypt将数据转化为ASCII编码encrypto_text为ASCII码bytes型数据
        # 判断输入的数据是字符串还是字节型数据
        encrypto_data = b''
        if type(data) is str:
            encrypto_data = blowfish.encrypt(pad(data.encode(encoding='utf-8'),self.BLOCK_SIZE))

        elif type(data) is bytes:
            encrypto_data = blowfish.encrypt(pad(data, self.BLOCK_SIZE))

        encrypto_data = binascii.b2a_hex(encrypto_data)
        encrypto_data = encrypto_data.decode(encoding='utf-8')

        return encrypto_data


    def decrypt(self, key, encrypto_data):
        # 解密需要去生成一个DES对象，DES.MODE_ECB表示ECB模式，还可选择MODE_CBC
        blowfish = Blowfish.new(key.encode(encoding='utf-8'), Blowfish.MODE_ECB)
        # print(binascii.b2a_hex(encrypto_data),encrypto_data.hex())
        # encrypto_data.hex()返回的是binascii.b2a_hex(encrypto_data)的字符串形式

        encrypto_data = encrypto_data.encode(encoding='utf-8')
        encrypto_data = binascii.a2b_hex(encrypto_data)

        # 加密时是先pad再encrypt加密，所以解密时我们就先decrypt解密再unpad
        decrypto_data = unpad(blowfish.decrypt(encrypto_data),self.BLOCK_SIZE).decode(encoding='utf-8')

        return decrypto_data


iv = b'-X\xb1\x13\xe8\xe2\xb4\\'

# AES的block_size只能为16，所以pad中的BLOCK_SIZE必须是16的倍数，秘钥key可以选择16,24和32
# CBC模式中每个模块与前一个密文块进行异或，因为第一个密文块没有前一块所以需要增加和块大小相同的初始化向量i
# 而CFB模式中由于加密流程和解密流程中被块加密器加密的数据是前一段密文，所以不需要用pad进行填充的
class Blowfish_CBC_class(object):

    def __init__(self):
        self.BLOCK_SIZE = 8

    def encrypt(self,key,data):

        # 生成长度等于Blowfish块大小(AES.block_size)的不可重复的密钥向量
        # iv = Random.new().read(Blowfish.block_size)
        # print(iv)

        # 声明全局iv，保持iv变量一致
        global iv

        # 使用key和iv初始化Blowfish对象, 使用MODE_CBC模式
        blowfish = Blowfish.new(key.encode(encoding='utf-8'), Blowfish.MODE_CBC, iv)
        # 加密的明文长度必须为16的倍数，如果长度不为16的倍数，则需要补足为16的倍数
        # 将iv（密钥向量）加到加密的密文开头，一起传输。iv占16个块，数据占一个快
        encrypto_data = b''
        if type(data) is str:
            encrypto_data = iv + blowfish.encrypt(pad(data.encode(encoding='utf-8'),self.BLOCK_SIZE))

        elif type(data) is bytes:
            encrypto_data = iv + blowfish.encrypt(pad(data,self.BLOCK_SIZE))

        return encrypto_data

    def decrypt(self,key,encrypto_data):
        # 解密的话要用key和iv生成新的Blowfish对象([:16]表示前16块数据，也就是iv)
        blowfish = Blowfish.new(key.encode(encoding='utf-8'), Blowfish.MODE_CBC, encrypto_data[:self.BLOCK_SIZE])
        # 使用新生成的Blowfish对象，将加密的密文解密([16:]表示最后一块数据，也就是加密数据)
        decrypto_data = unpad(blowfish.decrypt(encrypto_data[self.BLOCK_SIZE:]),self.BLOCK_SIZE)
        return decrypto_data


if __name__ == '__main__':

    key = 'feifei870126577d'
    data = '邓怡菲穿小棉袄！'

    print("-----EBC模式下的Blowfish加密-----")

    Blowfish_ECB_object = Blowfish_ECB_class()
    encrypto_data = Blowfish_ECB_object.encrypt(key,data)
    print('二进制密文：',encrypto_data)
    print('十六进制密文：',binascii.b2a_hex(encrypto_data))

    decrypto_data = Blowfish_ECB_object.decrypt(key,encrypto_data)
    print('原明文：',decrypto_data)

    print("-----CBC模式下的Blowfish加密-----")

    Blowfish_CBC_object = Blowfish_CBC_class()
    encrypto_data = Blowfish_CBC_object.encrypt(key,data)
    print('iv：',binascii.b2a_hex(encrypto_data[:8]))
    print('十六进制密文：', encrypto_data[8:])
    print('ASCII密文：', binascii.b2a_hex(encrypto_data[8:]))

    # 返回解密后的明文
    decrypto_data = Blowfish_CBC_object.decrypt(key, encrypto_data)
    print('十六进制明文：', decrypto_data)
    print('ASCII明文：', binascii.b2a_hex(decrypto_data))
    print('原明文：', decrypto_data.decode('utf-8'))

