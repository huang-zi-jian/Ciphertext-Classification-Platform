import base64
import os
import threading

from Crypto.Cipher import AES
from scapy.all import sniff

Block_SIZE = 16  # BYTES
# 分割
pad = lambda s: s + (Block_SIZE - len(s) % Block_SIZE) * \
                chr(Block_SIZE - len(s) % Block_SIZE)
# 合并
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

plaintext_path = '/home/ubuntu/密文体制分类系统后端应用/static/明文'  # 明文路径
ciphertext_path = '/home/ubuntu/密文体制分类系统后端应用/static/密文'  # 密文路径

packet_save_index = 0
lock = threading.Lock()


# 获取保存包下表
def get_save_index():
    global packet_save_index
    # 线程互斥
    with lock:
        packet_save_index += 1
        return packet_save_index


def mkdir(plaintext_save_folder, ciphertext_save_folder):
    """
    文件夹不存在则创建
    :param plaintext_save_folder:  保存明文的文件夹
    :param ciphertext_save_folder: 保存密文的文件夹
    :return: none
    """
    if not os.path.exists(plaintext_save_folder):
        os.mkdir(plaintext_save_folder)
    if not os.path.exists(ciphertext_save_folder):
        os.mkdir(ciphertext_save_folder)


def aesEncrypt(data, key='5c44c819appsapi0'):
    """
    AES的ecb加密解密
    :param data:加密解密的密钥
    :param key:加密解密的字符串
    :return:
    """
    key = key.encode('utf-8')
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    result = cipher.encrypt(data.encode())
    encodestrs = base64.b64encode(result)
    enctext = encodestrs.decode('utf-8')
    return bytes(enctext, 'UTF-8').hex()


def aesDecrypt(data, key='5c44c819appsaip0'):
    """
    AES的ecb加密解密
    :param data:加密解密的密钥
    :param key:加密解密的字符串
    :return:
    """
    key = key.encode('utf-8')
    data = pad(data)
    cipher = AES.new(key, AES.MODE_ECB)
    # 去部位
    text_decrypted = unpad(cipher.decrypt(data))
    text_decrypted = text_decrypted.decode('utf-8')

    return text_decrypted


def savePacket(packet_text, plaintext_save_folder):
    """
    save the packet to text-file

    :param packet_text: raw context
    :param plaintext_save_folder: path to save
    :return: none
    """
    plaintext = bytes(packet_text, 'UTF-8').hex()
    # ciphertext = aesEncrypt(packet_text)
    save_index = get_save_index()
    with open(os.path.join(plaintext_save_folder, '%d.txt' % save_index), 'w') as file:
        file.write(plaintext)
    # with open(os.path.join(ciphertext_save_folder, '%d.txt' % save_index), 'w') as file:
    #     file.write(ciphertext)


def handle_packet(packet):
    """
    handle the packet that captured, deal with thread
    :param packet:
    :return:
    """
    save_thread = threading.Thread(target=savePacket, args=(str(packet), plaintext_path))  # callback func savePacket
    save_thread.start()
    save_thread.join()


def capture(plaintext_save_folder: str, ciphertext_save_folder: str, count, iface=None):
    """
    外调函数，传入密文和明文包的保存路径，抓取的网卡，抓取包的个数
    返回抓到包的个数

    sniff(count=0,   抓取报的数量，设置为0时则一直捕获
          store=1,   保存抓取的数据包或者丢弃，1保存，0丢弃
          offline=None,   从pcap文件中读取数据包，而不进行嗅探，默认为None
          prn=None,   为每个数据包定义一个回调函数
          filter=None,   过滤规则，可以在里面定义winreshark里面的过滤语法
          L2socket=None,   使用给定的L2socket
          timeout=None,    在给定的事件后停止嗅探，默认为None
          opened_socket=None,  对指定的对象使用.recv进行读取
          stop_filter=None,   定义一个函数，决定在抓到指定的数据之后停止
          iface=None)   指定抓包的网卡,不指定则代表所有网卡
    """
    mkdir(plaintext_save_folder, ciphertext_save_folder)
    sniff(prn=handle_packet, iface=iface, count=count)
    return packet_save_index


# testing
if __name__ == '__main__':
    capture(plaintext_path, ciphertext_path, 18)
