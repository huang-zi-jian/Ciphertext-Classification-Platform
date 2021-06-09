'''
author: feifei
date: 2021-3-27
file info: 创造celery任务队列，并在该目录下启动celery（worker从队列中取出任务并且执行）：celery -A tasks worker --loglevel=info
change: 将celery以及配置封装，之后执行命令：celery -A celeryTasks worker --loglevel=info
'''

# todo：配置地址
import sys
sys.path.append('../../')
sys.path.append('/home/ubuntu/sp800_22_tests')
# sys.path.append('/Users/feifei/projectFile/Python项目/sp800_22_tests')
import getRandomnessTest
import os
from pymysql import connect
import json
from main.functions import emailSend_Object, hex_to_binarylist, get_files_Recursively
from main.capture import capture
from main.celery_task import celery_app
import zipfile
import shutil

# 密文文件生成NIST检测指标p值的功能接口
@celery_app.task
def features_Generate(**kwargs):
    print('开始生成密文特征')
    conn = connect(host='122.51.255.207', user='root', password='feifei@whut', port=3306, database='Cipher_Classify_base',
                   charset='utf8')
    # conn = connect(host='127.0.0.1', user='root', password='feifei', port=3306, database='Cipher_Classify_base',
    #                charset='utf8')
    cursor = conn.cursor()
    cursor.execute('''select email from admins where name="{}"'''.format(kwargs.get('username')))
    conn.commit()
    # 获取执行密文分类用户的邮箱
    userEmail = cursor.fetchone()[0]
    try:
        # suggestions列表用于存储特征字典
        suggestions = []
        filedir_list = get_files_Recursively('/home/ubuntu/密文体制分类系统后端应用/static/FeaturesGenerate')

        if filedir_list:
            # 循环读取16进制字符串文件并计算特征值
            for file_dir in filedir_list:
                with open(file=file_dir, mode='r', encoding='utf-8') as f:
                    fileContent = f.read()

                # 先调用函数将16进制字符串转化为二进制int型0/1列表
                bits = hex_to_binarylist(hex_str=fileContent)
                result_list, result_dict = getRandomnessTest.GetRandomnessTest(bits=bits, Linear_len=500, Linear_N_block=30)
                result_dict['filename'] = os.path.basename(file_dir)

                suggestions.append(result_dict)

        # 将NIST计算结果存到一个json文件中
        with open(file='/home/ubuntu/密文体制分类系统后端应用/static/FeaturesGenerate.json', mode='w', encoding='utf-8') as f:
            json.dump(suggestions, f)

        emailSendObject = emailSend_Object(receivers=[userEmail], receiver_name=kwargs.get('username'))
        emailSendObject.send_file(information='密文特征生成完毕，请前往系统查看！')

    except Exception as e:
        import traceback
        msg = traceback.format_exc()
        print(msg)
        # 模型训练完成后发送提示信息给用户，
        emailSendObject = emailSend_Object(receivers=[userEmail], receiver_name=kwargs.get('username'))
        emailSendObject.send_file(information='密文特征生成过程出错！！！\n' + msg)


# 网络抓包
@celery_app.task
def netpackage_capture(**kwargs):
    print('开始抓包')
    conn = connect(host='122.51.255.207', user='root', password='feifei@whut', port=3306, database='Cipher_Classify_base',
                   charset='utf8')
    # conn = connect(host='127.0.0.1', user='root', password='feifei', port=3306, database='Cipher_Classify_base',
    #                charset='utf8')
    cursor = conn.cursor()
    cursor.execute('''select email from admins where name="{}"'''.format(kwargs.get('username')))
    conn.commit()
    # 获取执行密文分类用户的邮箱
    userEmail = cursor.fetchone()[0]
    try:
        if os.path.isdir('/home/ubuntu/密文体制分类系统后端应用/static/明文'):
            shutil.rmtree('/home/ubuntu/密文体制分类系统后端应用/static/明文')
        if os.path.isdir('/home/ubuntu/密文体制分类系统后端应用/static/密文'):
            shutil.rmtree('/home/ubuntu/密文体制分类系统后端应用/static/密文')
        # 抓包代码
        plaintext_path = '/home/ubuntu/密文体制分类系统后端应用/static/明文'
        ciphertext_path = '/home/ubuntu/密文体制分类系统后端应用/static/密文'
        capture(plaintext_path, ciphertext_path, 18)
        with zipfile.ZipFile('/home/ubuntu/密文体制分类系统后端应用/static/package.zip', 'w',
                             zipfile.ZIP_DEFLATED) as zf:
            for dirpath, dirnames, filenames in os.walk(plaintext_path):
                for filename in filenames:
                    zf.write(os.path.join(dirpath, filename), '明文/' + filename)

            for dirpath, dirnames, filenames in os.walk(ciphertext_path):
                for filename in filenames:
                    zf.write(os.path.join(dirpath, filename), '密文/' + filename)
    

        emailSendObject = emailSend_Object(receivers=[userEmail], receiver_name=kwargs.get('username'))
        emailSendObject.send_file(
            filepath='/home/ubuntu/密文体制分类系统后端应用/static/package.zip',
            fileName='package.zip',
            information='网络抓包已完成，请查看附件！')

    except Exception as e:
        import traceback
        msg = traceback.format_exc()
        print(msg)
        # 模型训练完成后发送提示信息给用户，
        emailSendObject = emailSend_Object(receivers=[userEmail], receiver_name=kwargs.get('username'))
        emailSendObject.send_file(information='抓包过程过程出错！！！\n' + msg)


if __name__ == '__main__':
    celery_app.start()
