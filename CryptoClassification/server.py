from flask import Flask, request, jsonify
import os
import zipfile
from flask_cors import CORS
import DM
import json
from flask_sqlalchemy import SQLAlchemy
# from tasks import cipher_task, modelTrain_task
from main.celery_task.celeryTasks import cipher_task, modelTrain_task
from main.functions import getFileInformation
import shutil
import time
import pymysql


app = Flask(__name__)
CORS(app)
app.secret_key = 'feifei'


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql://root:feifei@whut@122.51.255.207/Cipher_Classify_base?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:feifei@localhost/Cipher_Classify_base?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # REMEMBER_COOKIE_DURATION = datetime.timedelta(seconds=300)


# 用对象对app进行配置
app.config.from_object(Config)
# app.config['MAIL_SERVER'] = 'smtp.qq.com'
# app.config['MAIL_PORT'] = 465
db = SQLAlchemy(app=app, use_native_unicode='utf-8')

# python对redis数据库数据进行操作
'''
import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
r = redis.Redis(connection_pool=pool)
r.set('foo', 'Bar')
'''


# print(app.name)


# 前端上传密文文件路由接口
@app.route('/Ciphertext_file_upload', methods=['POST'])
def ciphertextFileUpload():
    # 获取前端密文文件，并存入CiphertextFile文件夹中
    fileObject = request.files.get('file')
    fileName = fileObject.filename

    # 获取CiphertextFile文件夹中密文的文件名列表
    ls = os.listdir('static/CiphertextFile')
    if ls:
        # 采用循环删除CiphertextFile文件夹中的所有文件
        for filename in ls:
            if os.path.isdir('static/CiphertextFile/' + filename):
                shutil.rmtree('static/CiphertextFile/' + filename)
            else:
                os.remove('static/CiphertextFile/' + filename)

    if fileName.endswith('.zip'):
        # 先将压缩文件保存在本地
        fileObject.save('static/zipFile/' + fileName)
        # 读取压缩文件并解压到CiphertextFile文件夹
        zipFile = zipfile.ZipFile('static/zipFile/' + fileName)
        zipFile.extractall('static/CiphertextFile')
        # zipFileNameList = zipFile.namelist()

        zipFile.close()
        # for zipfile_name in zipFileNameList:
        #     zipfile_dir = 'static/CiphertextFile/' + zipfile_name
        #     # todo: 调用函数接口。传递本地密文文件路径，返回加密结果信息

    else:
        # 不是zip就是csv文件，这个前端已经做出了识别，可以直接保存到features文件夹
        fileObject.save('static/CiphertextFile/' + fileName)
        # zipfile_dir = 'static/CiphertextFile/' + fileName
        # # todo: 调用函数接口。传递本地密文文件路径，返回加密结果信息

    # 之类的msg会在前端进行验证，收到msg为success的信息就会显示上传成功
    return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})


# 前端获取密文分类结果路由接口
@app.route('/CipherResult', methods=['GET'])
def GetCipherResult():
    # DES = request.args.get('DES')
    DES3 = request.args.get('3DES')
    AES = request.args.get('AES')
    # RC4 = request.args.get('RC4')
    Blowfish = request.args.get('Blowfish')
    RSA = request.args.get('RSA')
    # MD5 = request.args.get('MD5')
    # SHA_1 = request.args.get('SHA-1')
    # category = request.args.get('category')
    classifier = request.args.get('classifier')
    # ratio = request.args.get('ratio')
    # input_channel = request.args.get('input_channel')
    # epoch = request.args.get('epoch')
    batch = request.args.get('batch')
    # loss_function = request.args.get('loss_function')
    # optimizer = request.args.get('optimizer')
    save_mode = request.args.get('save_mode')
    # col_name = request.args.get('col_name')
    username = request.args.get('username')
    userdegree = request.args.get('userdegree')

    # 提取用户选择的加密算法
    crypto_list = []
    # if DES:
        # crypto_list.append('DES')
    if DES3:
        crypto_list.append('3DES')
    if AES:
        crypto_list.append('AES')
    # if RC4:
    #     crypto_list.append('RC4')
    if Blowfish:
        crypto_list.append('Blowfish')
    if RSA:
        crypto_list.append('RSA')
    # if MD5:
    #     crypto_list.append('MD5')
    # if SHA_1:
    #     crypto_list.append('SHA-1')
    crypto_list = DM.concat(crypto_list)

    # 得出分类数
    category = len(crypto_list)

    # 将int型参数进行强转
    # if ratio:
    #     ratio = eval(ratio)
    # else:
    #     ratio = 0
    # if epoch:
    #     epoch = int(epoch)
    # else:
    #     epoch = 30
    # if batch:
    #     batch = int(batch)
    # else:
    #     batch = 300
    batch = int(batch)
    # input_channel = int(input_channel)
    input_channel = 1024

    # 根据系统用户的等级来指定celery队列中任务的优先级别
    if userdegree == 'Advanced':
        priority = 3
    elif userdegree == 'Medium':
        priority = 2
    else:
        priority = 1

    cipher_task.apply_async(kwargs={'username': username, 'classifier': classifier,
                                    'crypto_list': crypto_list, 'category': category,
                                    'batch': batch, 'input_channel': input_channel,
                                    'col_name': ['data_frame'], 'save_mode': save_mode}, priority=priority)
    # return_result, time_format = getCipherResult(file_dir='static/CiphertextFile', model_name=classifier, args=args1)

    return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})


# 前端获取密文分类结果路由接口
@app.route('/ReturnCipherResult', methods=['GET'])
def returnCipherResult():
    page = request.args.get('page')
    limit = request.args.get('limit')

    with open(file='static/CipherResult.json', mode='r', encoding='utf-8') as f:
        # 从json文件中读取数据
        CipherResult = json.load(f)

    # 通过前端传递过来的页码page以及每页数据量限制limit来返回数据
    data = CipherResult.get('data')
    start = (int(page) - 1) * int(limit)
    end = int(page) * int(limit)
    return_data = data[start: end]

    CipherResult['data'] = return_data

    return jsonify(CipherResult)


# 前端获取最近一次密文分类时间的路由接口
@app.route('/ReturnCiphertime', methods=['GET'])
def returnCiphertime():
    with open(file='static/ciphertimeRecord.json', mode='r', encoding='utf-8') as f:
        # 从json文件中读取数据
        CipherResult = json.load(f)

    timeRecord = CipherResult.get('timeRecord')
    return jsonify({"code": 200, "msg": "success", 'timeRecord': timeRecord})


# 前端上传模型训练文件路由接口
@app.route('/trainmodel_file_upload', methods=['POST'])
def trainmodelFileUpload():
    # 获取前端密文文件，并存入trainSetFile文件夹中
    fileObject = request.files.get('file')
    fileName = fileObject.filename

    # 获取trainModelFile文件夹中密文的文件名列表
    ls = os.listdir('static/trainModelFile')
    if ls:
        # 采用循环删除trainModelFile文件夹中的所有文件
        for filename in ls:
            # os.remove('static/trainSetFile/' + filename)
            if os.path.isdir('static/trainModelFile/' + filename):
                shutil.rmtree('static/trainModelFile/' + filename)
            else:
                os.remove('static/trainModelFile/' + filename)

    if fileName.endswith('.zip'):
        # 先将压缩文件保存在本地
        fileObject.save('static/zipFile/' + fileName)
        # 读取压缩文件并解压到trainSetFile文件夹
        zipFile = zipfile.ZipFile('static/zipFile/' + fileName)
        zipFile.extractall('static/trainModelFile')

        zipFile.close()

        # 之类的msg会在前端进行验证，收到msg为success的信息就会显示上传成功
        return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})
    else:
        # 之类的msg会在前端进行验证，收到msg为success的信息就会显示上传成功
        return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})


# 用户模型训练接口
@app.route('/trainmodelResult', methods=['GET'])
def GetTrainModelResult():
    # DES = request.args.get('DES')
    DES3 = request.args.get('3DES')
    AES = request.args.get('AES')
    # RC4 = request.args.get('RC4')
    Blowfish = request.args.get('Blowfish')
    RSA = request.args.get('RSA')
    # MD5 = request.args.get('MD5')
    # SHA_1 = request.args.get('SHA-1')
    # category = request.args.get('category')
    classifier = request.args.get('classifier')
    ratio = request.args.get('ratio')
    # input_channel = request.args.get('input_channel')
    epoch = request.args.get('epoch')
    batch = request.args.get('batch')
    loss_function = request.args.get('loss_function')
    optimizer = request.args.get('optimizer')
    save_mode = request.args.get('save_mode')
    # col_name = request.args.get('col_name')
    username = request.args.get('username')
    userdegree = request.args.get('userdegree')

    # 提取用户选择的加密算法
    crypto_list = []
    # if DES:
    #     crypto_list.append('DES')
    if DES3:
        crypto_list.append('3DES')
    if AES:
        crypto_list.append('AES')
    # if RC4:
    #     crypto_list.append('RC4')
    if Blowfish:
        crypto_list.append('Blowfish')
    if RSA:
        crypto_list.append('RSA')
    # if MD5:
    #     crypto_list.append('MD5')
    # if SHA_1:
    #     crypto_list.append('SHA-1')
    crypto_list = DM.concat(crypto_list)

    # 得出分类数
    # if category:
    #     category = int(category)
    category = len(crypto_list)

    # 将int型参数进行强转
    # if ratio:
    #     ratio = eval(ratio)
    # else:
    #     ratio = 0
    # if epoch:
    #     epoch = int(epoch)
    # else:
    #     epoch = 30
    # if batch:
    #     batch = int(batch)
    # else:
    #     batch = 300
    # input_channel = int(input_channel)
    ratio = eval(ratio)
    # 如果是非神经网络的话，可能就不存在epoch参数值
    if epoch:
        epoch = int(epoch)
    else:
        epoch = 30

    batch = int(batch)
    input_channel = 1024

    # args1 = Args(category=category, input_channel=input_channel,
    #              col_name=['data_frame'], save_mode=save_mode, optimizer=optimizer,
    #              loss_function=loss_function)

    # 根据系统用户的等级来指定celery队列中任务的优先级别
    if userdegree == 'Advanced':
        priority = 3
    elif userdegree == 'Medium':
        priority = 2
    else:
        priority = 1
    
    size, txtFileNum = getFileInformation('static/trainModelFile')
    # apply_async如果换成delay就直接传递参数就行，不必传递可迭代对象
    modelTrain_task.apply_async(kwargs={'crypto_list': crypto_list, 'category': category,
                                        'classifier': classifier, 'ratio': ratio, 'epoch': epoch,
                                        'batch': batch, 'input_channel': input_channel,
                                        'col_name': ['data_frame'], 'save_mode': save_mode,
                                        'optimizer': optimizer, 'loss_function': loss_function,
                                        'username': username, 'size': size,
                                        'txtFileNum': txtFileNum}, priority=priority)
    # getTrainedModel(file_dir='static/CiphertextFile', model_name=classifier, args=args1)
    return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})


# 获取模型训练历史数据接口
@app.route('/getModelTrainRecords', methods=['GET'])
def GetModelTrainRecords():
    # 定义存储分类列表
    RF = {'twoCategories': [], 'threeCategories': [], 'fourCategories': []}
    SVM = {'twoCategories': [], 'threeCategories': [], 'fourCategories': []}
    AlexNet = {'twoCategories': [], 'threeCategories': [], 'fourCategories': []}
    SCNN = {'twoCategories': [], 'threeCategories': [], 'fourCategories': []}
    ResNet = {'twoCategories': [], 'threeCategories': [], 'fourCategories': []}
    VGG = {'twoCategories': [], 'threeCategories': [], 'fourCategories': []}

    try:
        connect = pymysql.connect
        conn = connect(host='127.0.0.1', user='root', password='feifei@whut', port=3306, database='Cipher_Classify_base', charset='utf8')
        # conn = connect(host='127.0.0.1', user='root', port=3306, database='Cipher_Classify_base', charset='utf8')
        cursor = conn.cursor()

        cursor.execute("select * from modelTrainrecords where is_delete=false;")
        mysqlData_list = cursor.fetchall()

        # 用字典进行分类数的转化，方便后续训练记录的分类获取
        select_dict = {'2': 'twoCategories', '3': 'threeCategories', '4': 'fourCategories'}
        for id, algorithm, category, size, txtFileNum, accuracy, is_delete in mysqlData_list:

            # 按照密文分类算法将信息存放进数组
            if algorithm=='RF':
                RF[select_dict.get(category)].append([eval(size), eval(accuracy)])
            elif algorithm=='SVM':
                SVM[select_dict.get(category)].append([eval(size), eval(accuracy)])
            elif algorithm == 'AlexNet':
                AlexNet[select_dict.get(category)].append([eval(size), eval(accuracy)])
            elif algorithm=='SCNN':
                SCNN[select_dict.get(category)].append([eval(size), eval(accuracy)])
            elif algorithm == 'ResNet':
                ResNet[select_dict.get(category)].append([eval(size), eval(accuracy)])
            elif algorithm == 'VGG':
                VGG[select_dict.get(category)].append([eval(size), eval(accuracy)])


        result = {'RF': RF, 'SVM': SVM, 'AlexNet': AlexNet, 'SCNN': SCNN, 'ResNet': ResNet, 'VGG': VGG}
        conn.commit()

        return jsonify({"code": 200, "msg": "success", 'data': result})

    except Exception as e:
        conn.rollback()

        return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})


# 获取模型训练饼状图数据接口
@app.route('/pieChartModelTrain', methods=['GET'])
def GetPieChartModelTrain():
    # 定义存储分类列表
    categories = {'twoCategories': 0, 'threeCategories': 0, 'fourCategories': 0}
    algorithms ={'RF': 0, 'SVM': 0, 'AlexNet': 0, 'SCNN': 0, 'ResNet': 0, 'VGG': 0}

    try:
        connect = pymysql.connect
        conn = connect(host='127.0.0.1', user='root', password='feifei@whut', port=3306, database='Cipher_Classify_base', charset='utf8')
        # conn = connect(host='127.0.0.1', user='root', port=3306, database='Cipher_Classify_base', charset='utf8')
        cursor = conn.cursor()

        cursor.execute("select * from modelTrainrecords where is_delete=false;")
        mysqlData_list = cursor.fetchall()

        # 用字典进行分类数的转化，方便后续训练记录的分类获取
        select_dict = {'2': 'twoCategories', '3': 'threeCategories', '4': 'fourCategories'}
        for id, algorithm, category, size, txtFileNum, accuracy, is_delete in mysqlData_list:

            # 每次循环对分类数以及加密算法自加1
            categories[select_dict.get(category)] += 1
            algorithms[algorithm] += 1

        result = {'category': categories, 'algorithm': algorithms}
        conn.commit()

        return jsonify({"code": 200, "msg": "success", 'data': result})

    except Exception as e:
        import traceback
        # traceback.print_exc()
        msg = traceback.format_exc()
        print(msg)
        conn.rollback()

        return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})


# 放弃同步文件发送，采用celery异步任务队列处理
'''
# 后端给前端发送压缩文件，指定路径作为参数
@app.route('/sendfile', methods=['GET'])
def sendFile():
    model_path = request.args.get('model_path')

    # BytesIO实现内存中读写bytes，而同类似的StringIO是对字符串的内存操作
    memory_file = BytesIO()
    # BytesIO需要传递字节数，但ZipFile对象不属于字节数据，所以
    # 使用BytesIO作为基础在内存中创建ZipFile，（直接ZipFile生成的对象是存储在磁盘中的）
    # file_src = 'trained_model/SCNN/SCNN_3DES_ECB_ones&AES_ECB_ones&Blowfish_ECB_ones&RSA_ones&SHA-1_ones_parameter.pkl'
    # file_src = url_path
    model_arc = os.path.basename(model_path)
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # zf = zipfile.ZipFile('test.zip', 'w', zipfile.ZIP_DEFLATED)

        # 这里如果不指定arcname的话压缩文件中文件会自动加上file_src的路径
        zf.write(filename=model_path, arcname=model_arc)
        # zf.write(filename='test.zip', arcname='feifei.zip')

    # 将内存文件对象的读写位置‘倒回’到开头
    memory_file.seek(0)
    return send_file(memory_file, attachment_filename='trained_model.zip', as_attachment=True)
'''


# 获取static静态文件接口
@app.route('/getStaticFiles', methods=['POST'])
def getStaticFiles():
    # 获取前端页码page以及每页数据量限制limit参数
    page = request.get_json()['page']
    limit = request.get_json()['limit']
    folder = request.get_json()['folder']

    print(folder)

    suggestions = []
    filename_list = os.listdir('static/' + folder)

    for filename in filename_list:
        temp = {}

        file_dir = 'static/' + folder + '/' + filename

        # 获取文件大小（kb为单位）并且返回字符串形式
        size = os.path.getsize(file_dir)
        size = int(size / 1024)
        size = str(size) + 'kb'

        createdTime = time.localtime(os.stat(file_dir).st_ctime)
        modifiedTime = time.localtime(os.stat(file_dir).st_mtime)

        cTime = time.strftime('%Y-%m-%d %H:%M:%S', createdTime)
        mTime = time.strftime('%Y-%m-%d %H:%M:%S', modifiedTime)

        temp['filename'] = filename
        temp['size'] = size
        temp['createdTime'] = cTime
        temp['modifiedTime'] = mTime
        # 根据前端传来的文件夹的名称将不同的文件分为不同搞的状态
        temp['status'] = folder + "[Temporary File]"

        suggestions.append(temp)

    start = (int(page) - 1) * int(limit)
    end = int(page) * int(limit)
    return_data = suggestions[start: end]

    return jsonify({"code": 0, "msg": "success", 'count': len(suggestions), 'data': return_data})


# 删除static静态文件请求接口
@app.route('/delStaticFile', methods=['POST'])
def delStaticFile():
    filename = request.get_json()['filename']
    status = request.get_json()['status']

    # 根据文件不同的状态进行不同的删除操作
    if "zipFile" in status:
        if filename in os.listdir('static/zipFile'):
            file_dir = 'static/zipFile/' + filename
            os.remove(file_dir)

            return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})
        else:
            return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})

    elif "trainModelFile" in status:
        if filename in os.listdir('static/trainModelFile'):
            file_dir = 'static/trainModelFile/' + filename
            # os.remove(file_dir)
            shutil.rmtree(file_dir)

            return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})
        else:
            return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
