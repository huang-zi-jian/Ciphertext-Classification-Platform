'''
author: feifei
date: 2021-3-27
file info: 创造celery任务队列，并在该目录下启动celery（worker从队列中取出任务并且执行）：celery -A tasks worker --loglevel=info
change: 将celery以及配置封装，之后执行命令：celery -A celeryTasks worker --loglevel=info
'''
import sys

sys.path.append('/home/ubuntu/CryptoClassification/')

from backend import Args, getCipherResult, getTrainedModel
from pymysql import connect
import json
from main.functions import emailSend_Object
import zipfile
import os
from main.celery_task import celery_app


# 创建异步celery任务——密文分类
@celery_app.task
def cipher_task(**kwargs):
    print('开始分类')
    conn = connect(host='127.0.0.1', user='root', password='feifei@whut', port=3306, database='Cipher_Classify_base',
                   charset='utf8')
    # conn = connect(host='127.0.0.1', user='root', password='feifei', port=3306, database='Cipher_Classify_base',
    #                charset='utf8')
    cursor = conn.cursor()
    cursor.execute('''select email from admins where name="{}"'''.format(kwargs.get('username')))
    conn.commit()
    # 获取执行密文分类用户的邮箱
    userEmail = cursor.fetchone()[0]
    try:
        args1 = Args(crypto_list=kwargs.get('crypto_list'), category=kwargs.get('category'),
                     input_channel=kwargs.get('input_channel'), col_name=kwargs.get('col_name'),
                     save_mode=kwargs.get('save_mode'), optimizer=kwargs.get('optimizer'),
                     loss_function=kwargs.get('loss_function'), ratio=kwargs.get('ratio'),
                     epoch=kwargs.get('epoch'), batch=kwargs.get('batch'))
        # args1 = Args(['3DES', 'AES'], 2, 1024, col_name=['data_frame'], batch=300, epoch=30, ratio=0.8,
        #              save_mode='para')
        return_result, time_format = getCipherResult(
            file_dir='/home/ubuntu/CryptoClassification/static/CiphertextFile/',
            model_name=kwargs.get('classifier'), args=args1)

        for result in return_result:
            sql = """insert into classifyrecords(admin, fileName, size, result, status, confidence, datetime, is_delete)
            values('%s', '%s', '%s', '%s', '%s', '%s', '%s', false);""" % (kwargs.get('username'),
                                                                           result['fileName'],
                                                                           result['size'], result['result'],
                                                                           result['status'],
                                                                           "%.3f%%" % (result['confidence'] * 100),
                                                                           time_format)

            cursor.execute(sql)

        conn.commit()
        # clRecord_temp = ClassifyRecord(admin='feifei', fileName="0.csv", size="0kb", result="DES", status="true",
        #                             confidence="64%", datetime="2020-12-12", is_delete=False)
        cursor.close()

        count = len(return_result)
        Result = {"code": 0, "msg": "success", "count": count, 'data': return_result}

        # try:
        with open(file='/home/ubuntu/CryptoClassification/static/CipherResult.json', mode='w',
                  encoding='utf-8') as f:
            # 将数据写入json文件
            json.dump(Result, f)

        with open(file='/home/ubuntu/CryptoClassification/static/ciphertimeRecord.json', mode='w',
                  encoding='utf-8') as f:
            # 将分类时间写入json文件
            json.dump({'timeRecord': time_format}, f)

        # 分类完成后发送提示信息给用户，
        emailSendObject = emailSend_Object(receivers=[userEmail], receiver_name=kwargs.get('username'))
        # 直接发送information提示信息，没有附件
        emailSendObject.send_file(information='密文分类已完成，请登录系统查看！')
    # 事务回滚
    except Exception as e:
        import traceback
        # traceback.print_exc()
        msg = traceback.format_exc()
        print(msg)
        conn.rollback()
        # 分类完成后发送提示信息给用户，
        emailSendObject = emailSend_Object(receivers=[userEmail], receiver_name=kwargs.get('username'))
        # 直接发送information提示信息，没有附件
        emailSendObject.send_file(information='密文分类过程出错！！！\n' + msg)

    finally:
        conn.close()


# 创建异步celery任务——用户模型训练
@celery_app.task
def modelTrain_task(**kwargs):
    print('开始训练模型')
    conn = connect(host='127.0.0.1', user='root', password='feifei@whut', port=3306, database='Cipher_Classify_base',
                   charset='utf8')
    # conn = connect(host='127.0.0.1', user='root', password='feifei', port=3306, database='Cipher_Classify_base',
    #                charset='utf8')
    # conn = connect(host='122.51.255.207', user='root', password='1234', port=3306, database='Cipher_Classify_base',
    #                charset='utf8')
    cursor = conn.cursor()
    cursor.execute('''select email from admins where name="{}"'''.format(kwargs.get('username')))
    conn.commit()
    # 获取执行密文分类用户的邮箱
    userEmail = cursor.fetchone()[0]
    try:
        args1 = Args(crypto_list=kwargs.get('crypto_list'), category=kwargs.get('category'),
                     input_channel=kwargs.get('input_channel'), col_name=kwargs.get('col_name'),
                     save_mode=kwargs.get('save_mode'), optimizer=kwargs.get('optimizer'),
                     loss_function=kwargs.get('loss_function'), ratio=kwargs.get('ratio'),
                     epoch=kwargs.get('epoch'), batch=kwargs.get('batch'))
        # 模型相关信息从modelTrainResult中提取
        # return {
        #     'model_name': model_name,
        #     'time': str(timestamp),
        #     'pic_dir': pic_path,
        #     'model_dir': model_path,
        #     'accuracy': accuracy
        modelTrainResult = getTrainedModel(
            file_dir='/home/ubuntu/CryptoClassification/static/trainModelFile/',
            model_name=kwargs.get('classifier'),
            args=args1)
        # todo: 将训练模型的pkl模型文件以及模型效果图保存至压缩包中，获取modelTrainResult中的两文件地址信息
        with zipfile.ZipFile('/home/ubuntu/CryptoClassification/static/trained_model.zip', 'w',
                             zipfile.ZIP_DEFLATED) as zf:
            # zf = zipfile.ZipFile('test.zip', 'w', zipfile.ZIP_DEFLATED)
            # 这里如果不指定arcname的话压缩文件中文件会自动加上file_src的路径
            model_filePath = modelTrainResult.get('model_dir')
            img_filePath = modelTrainResult.get('pic_dir')
            zf.write(filename=model_filePath, arcname=os.path.basename(model_filePath))
            zf.write(filename=img_filePath, arcname=os.path.basename(img_filePath))
            print(model_filePath)
            print(img_filePath)
	
	# 将模型训练数据写入modelTrainrecords数据表
        conn = connect(host='127.0.0.1', user='root', password='feifei@whut', port=3306, database='Cipher_Classify_base',
                   charset='utf8')
        cursor = conn.cursor()
        cursor.execute(
            '''insert into modelTrainrecords(algorithm, category, size, txtFileNum, accuracy, is_delete) value("{}", "{}", "{}", "{}", "{}", false)'''.format(
                kwargs.get('classifier'), str(kwargs.get('category')), kwargs.get('size'), kwargs.get('txtFileNum'),
                str(round(modelTrainResult.get('accuracy'), 2))))
        conn.commit()

        # 模型训练完成后发送提示信息给用户，
        emailSendObject = emailSend_Object(receivers=[userEmail], receiver_name=kwargs.get('username'))
        emailSendObject.send_file(
            filepath='/home/ubuntu/CryptoClassification/static/trained_model.zip',
            fileName='trained_model.zip',
            information='模型训练已完成，模型文件请查看附件！')

    except Exception as e:
        import traceback
        # traceback.print_exc()
        msg = traceback.format_exc()
        print(msg)
        conn.rollback()
        # 模型训练完成后发送提示信息给用户，
        emailSendObject = emailSend_Object(receivers=[userEmail], receiver_name=kwargs.get('username'))
        emailSendObject.send_file(information='模型训练过程出错！！！\n' + msg)
    finally:
        conn.close()


if __name__ == '__main__':
    celery_app.start()
