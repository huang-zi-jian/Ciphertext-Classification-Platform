'''
author: feifei
date: 2021-3-23
file info: 创造celery任务队列，并在该目录下启动celery（worker从队列中取出任务并且执行）：celery -A tasks worker --loglevel=info
'''
# todo：配置地址
import sys
sys.path.append('/home/ubuntu/sp800_22_tests')
# sys.path.append('/Users/feifei/projectFile/Python项目/sp800_22_tests')
import getRandomnessTest
import os
from celery import Celery
from pymysql import connect
import json
from main.functions import emailSend_Object, hex_to_binarylist, get_files_Recursively


# 初始化celery对象，传入对应的app应用名称以及消息代理的连接URL
# celery = Celery(app.name, broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')
# celery_app = Celery('tasks', broker='redis://:feifei@127.0.0.1:6379/0', backend='redis://:feifei@127.0.0.1:6379/0')
celery_app = Celery('tasks', broker='redis://:feifei@122.51.255.207:6379/0',
                    backend='redis://:feifei@122.51.255.207:6379/1')


# 密文文件生成NIST检测指标p值的功能接口
@celery_app.task
def features_Generate(**kwargs):
    print('开始生成密文特征')
    conn = connect(host='122.51.255.207', user='root', password='1234', port=3306, database='Cipher_Classify_base',
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
        filedir_list = get_files_Recursively('static/FeaturesGenerate')

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
        with open(file='static/FeaturesGenerate.json', mode='w', encoding='utf-8') as f:
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


if __name__ == '__main__':
    celery_app.start()
