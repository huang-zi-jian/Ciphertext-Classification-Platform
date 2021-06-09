'''
author: feifei
date: 2021-2-25
file info: RSA对称加密/解密
'''

import rsa
import binascii
import time


class RSA_class(object):

    # 初始化最大加密长度，117
    def __init__(self):
        self.encrypt_length = 117

    # 使用网页中获得的n和e值，将明文加密
    def encrypt(self, data, pub_key):

        # 用公钥把明文加密
        # result = rsa.encrypt(data.encode('utf-8'), pub_key)

        # encrypto_data用于连接存储分段加密的密文
        encrypto_data = ''

        # 明文为字符串时转字节然后调用encrypt函数
        if type(data) is str:
            return self.encrypt(data.encode('utf-8'), pub_key)
            # encrypto_data = rsa.encrypt(data.encode('utf-8'), pub_key)

        elif type(data) is bytes:
            # 明文字节数据长度
            data_length = len(data)
            # position起到了指针的作用，position指向加密开始的位置
            position = 0

            while data_length > position:
                # 用于处理不满117的余数字节密文，rsa.encrypt加密后的密文长度和公钥长度相同
                if data_length <= position + 117:
                    section_data = rsa.encrypt(data[position:data_length], pub_key)
                    encrypto_data = encrypto_data + binascii.b2a_hex(section_data).decode(encoding='utf-8')
                else:
                    section_data = rsa.encrypt(data[position:position + 117], pub_key)
                    encrypto_data = encrypto_data + binascii.b2a_hex(section_data).decode(encoding='utf-8')
                # position位置指向下一个分开开头
                position = position + 117

        # 将加密结果按照字符串连接返回
        return encrypto_data

    def decrypt(self, encrypto_data, priv_key):
        data = b''
        position = 0
        while len(encrypto_data) > position:
            section_data = encrypto_data[position:position + 256]
            position = position + 256
            # 直接用私钥解密
            decrypto_data = rsa.decrypt(binascii.a2b_hex(section_data.encode(encoding='utf-8')), priv_key)
            data = data + decrypto_data

        return data.decode(encoding='utf-8')


if __name__ == '__main__':
    '''
    # 生成一次性 公钥/秘钥
        # 用newkeys生成公钥和私钥，1024位的秘钥可以一次性最多可以加密117字节明文数据
        pub_key, priv_key = rsa.newkeys(1024)

        pub = pub_key.save_pkcs1()
        with open('public.pem', 'wb') as pubfile:
            pubfile.write(pub)

        pri = priv_key.save_pkcs1()
        with open('private.pem', 'wb') as prifile:
            prifile.write(pri)
    '''
    # pub_key = ''
    # priv_key = ''
    with open('public.pem') as publickfile:
        p = publickfile.read()
        pub_key = rsa.PublicKey.load_pkcs1(p)

    with open('private.pem') as privatefile:
        p = privatefile.read()
        priv_key = rsa.PrivateKey.load_pkcs1(p)

    data = '邓怡菲穿小棉袄！邓怡菲穿小棉袄！邓怡菲穿小棉袄！邓怡菲穿小棉袄！邓怡菲穿小棉袄！邓怡菲穿小棉袄！邓怡菲穿小棉袄！'
    Cipher_Object = RSA_class()
    encrypto_data = Cipher_Object.encrypt(data=data, pub_key=pub_key)
    Data = Cipher_Object.decrypt(encrypto_data=encrypto_data, priv_key=priv_key)
    print(Data)

# import rsa
#
# def rsa_encrypt(plaintext):
#     '''
#     输入明文、生成公钥、私钥
#     公钥对明文进行加密、字符串加密
#     :return:加密结果及私钥
#     '''
#     pub_key, priv_key = rsa.newkeys(1024)
#     print(pub_key)
#     print(priv_key)
#     plaintext = plaintext.encode()     #the message to encrypt. Must be a byte string no longer than``k-11`` bytes
#     ciphertext = rsa.encrypt(plaintext, pub_key)
#     print('加密后：', ciphertext)
#     return ciphertext, priv_key
#
# def rsa_decrypt(ciphertext, priv_key):
#     '''
#     传参私钥和加密的明文
#     :param ciphertext:
#     :param priv_key:
#     :return:解密结果
#     '''
#     plaintext = rsa.decrypt(ciphertext, priv_key)
#     plaintext = plaintext.decode()
#     print('解密后:', plaintext)
#
# if __name__ == '__main__':
#     plaintext = input("输入明文:\n").strip()
#     ciphertext, priv_key = rsa_encrypt(plaintext)
#     rsa_decrypt(ciphertext, priv_key)
