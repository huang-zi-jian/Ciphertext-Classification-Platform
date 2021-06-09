'''
author: feifei
date: 2021-3-14
file info: 脚本测试
'''
import zipfile
import os
import shutil

'''
print(round(34.456))

filename = os.path.basename('./static/CiphertextFile/AES-7231.txt')
print(filename)
'''

# 删除文件测试
'''
ls = os.listdir('static/trainSetFile')
if ls:
    # 采用循环删除CiphertextFile文件夹中的所有文件
    for filename in ls:
        # os.remove('static/trainSetFile/' + filename)
        shutil.rmtree('static/trainSetFile/' + filename)

zipFile = zipfile.ZipFile('C:\\Users\23796\\Desktop\\dataset.zip')
zipFile.extractall('static/trainSetFile')
# path = 'static/trainSetFile'
# zipFileNameList = zipFile.namelist()

zipFile.close()
'''

# celery异步任务队列测试脚本
'''
import time
from celery import Celery
from main.functions import emailSend_Object
from celery.result import AsyncResult
celery_app = Celery('scriptTest', broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')

@celery_app.task
def add(**kwargs):
    print('hello world!')
    print(kwargs.get('key1'), kwargs.get('key2'))
    emailSendObject = emailSend_Object(receivers=['2379631316@qq.com'])
    emailSendObject.send_file(information='celery异步消息队列测试')
    # with open('hello.txt', 'w', encoding='utf-8') as f:
    #     f.write(args)
    # print('异步开始')
    # return args[0] + args[1]
    return kwargs.get('key1') + kwargs.get('key2')


if __name__ == '__main__':
    # result = add.apply_async(kwargs={"key1": 1, "key2": 2}, countdown=20)
    result = add.apply_async(kwargs={"key1": 1, "key2": 2})
    time.sleep(3)
    print(result)
    print(result.result)
    # print(result.info)
    print(result.status)
    # async_task = AsyncResult(id=result.id, app=celery_app)
    # while True:
    #     print(async_task.status, async_task.info)
    # print(async_task)
'''

# 写入压缩文件测试
'''
import zipfile

with zipfile.ZipFile('trained_model.zip', 'w', zipfile.ZIP_DEFLATED) as zf:
    # zf = zipfile.ZipFile('test.zip', 'w', zipfile.ZIP_DEFLATED)
    # 这里如果不指定arcname的话压缩文件中文件会自动加上file_src的路径
    zf.write(filename='flask_1.log', arcname='flask.log')
    zf.write(filename='redis.log', arcname='redis.log')
    zf.write(filename='AFBE08D6-8A6E-4037-8D2F-BC86FCB535AC_1_105_c.jpeg', arcname='feifei.jpg')
'''

# pymysql测试
'''
from pymysql import connect

conn = connect(host='127.0.0.1', user='root', password='feifei', port=3306, database='Cipher_Classify_base',
                       charset='utf8')
cursor = conn.cursor()
cursor.execute('select email from admins where name="feifei"')
information = cursor.fetchone()
print(information)
'''

'''
num = eval('0.6')
print(num)

d = "%.3f%%" % (0.99257 * 100)
print(d)
'''

from celery import Celery
import json


# 初始化celery对象，传入对应的app应用名称以及消息代理的连接URL
# celery = Celery(app.name, broker='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379/0')
# celery_app = Celery('tasks', broker='redis://:feifei@122.51.255.207:6379/0', backend='redis://:feifei@122.51.255.207:6379/0')

# python操作redis数据库数据，可远程连接服务器redis
'''
import redis
# decode_responses为真表示取出来的是字符串而不是字节
pool = redis.ConnectionPool(host='122.51.255.207', port=6379, password='feifei', decode_responses=True)
redis_app = redis.Redis(connection_pool=pool)
redis_app.set('name', 'feifei-1')
wait_name = 'wait'
down_name = 'down'
redis_app.sadd(wait_name, 'a', 'b', 'c', 'd', 'e', 'f')

while True:
    down_routine = redis_app.spop(wait_name)
    if down_routine:
        redis_app.sadd(down_name, down_routine)
    else:
        break

print(redis_app.smembers(down_name))
'''