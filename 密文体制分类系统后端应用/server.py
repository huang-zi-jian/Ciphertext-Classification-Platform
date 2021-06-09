'''
author: feifei
date: 2021-2-1
file info: 密文系统的flask后台应用
'''
import shutil
import sys
import time

# # todo：配置地址
# sys.path.append('/Users/feifei/projectFile/Python项目/sp800_22_tests')
# import getRandomnessTest

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
from main.APP_Initial import Admin, ClassifyRecord, dataSetRecord, app, db
import json
import pandas
import numpy
from main.functions import staticsSum, FuzzyFinder, getMysqlExportData, hex_to_binarylist
import os
import zipfile
from main.DES import DES_ECB_class
from main.DES3 import DES3_ECB_class
from main.AES import AES_ECB_class
from main.Blowfish import Blowfish_ECB_class
from main.RC4 import RC4_class
from main.RSA import RSA_class
from main.HASH import Md5, Sha1, Sha512
import rsa
import binascii
import logging
import tempfile
from io import BytesIO
# from tasks import features_Generate
from main.celery_task.celeryTasks import features_Generate, netpackage_capture


# 创建一个handler全局变量，用于写入日志文件
fHandler = logging.FileHandler('System.log', mode='a', encoding='utf-8')
fHandler.setLevel(logging.DEBUG)
# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fHandler.setFormatter(formatter)

'''
# 后端发送压缩文件
@app.route('/sendfile', methods=['POST'])
def sendFile():
    # BytesIO实现内存中读写bytes，而同类似的StringIO是对字符串的内存操作
    memory_file = BytesIO()

    # BytesIO需要传递字节数，但ZipFile对象不属于字节数据，所以
    # 使用BytesIO作为基础在内存中创建ZipFile，（直接ZipFile生成的对象是存储在磁盘中的）
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        # zf = zipfile.ZipFile('test.zip', 'w', zipfile.ZIP_DEFLATED)
        zf.write(filename='System.log', arcname='feifei.log')
        # zf.write(filename='test.zip', arcname='feifei.zip')

    # 将内存文件对象的读写位置‘倒回’到开头
    memory_file.seek(0)

    return send_file(memory_file, attachment_filename='mrsfei.zip', as_attachment=True)
'''


# 管理员账号密码登录请求接口
@app.route('/login', methods=['POST'])
def login():
    username = request.get_json()['username']
    password = request.get_json()['password']
    # 获取用户登录ip地址
    ip = request.remote_addr

    print(username, password, ip)

    user = Admin.query.filter(Admin.name == username, Admin.password == password, Admin.is_delete == False).first()
    if user:
        # 如果用户存在，那么将用户名以及对应的登录信息写入日志
        logger = logging.getLogger(name=username)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(fHandler)
        logger.info('login - ' + ip)
        # url_for()方法传入路由对应的函数就会返回路由对应的地址，
        # redirect()传入路由地址作为参数并且返回就会重定向置该路由执行该路由操作
        return jsonify({'msg': True, 'code': 200, 'token': 'feifei', 'degree': user.degree})
    else:
        return jsonify({'msg': False, 'code': 500, 'token': 'feifei'})


# 管理员登出系统请求接口
@app.route('/logout', methods=['POST'])
def logout():
    # 获取登出用户名以及ip地址
    username = request.get_json()['username']
    ip = request.remote_addr

    user = Admin.query.filter(Admin.name == username, Admin.is_delete == False).first()
    if user:
        # 如果用户存在，那么将用户名以及对应的登录信息写入日志
        logger = logging.getLogger(name=username)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(fHandler)
        logger.info('logout - ' + ip)

        return jsonify({'msg': True, 'code': 200, 'token': 'feifei'})
    else:
        return jsonify({'msg': False, 'code': 500, 'token': 'feifei'})


# 管理员登出系统请求接口
@app.route('/addUser', methods=['POST'])
def doAddUser():
    username = request.get_json()['username']
    password = request.get_json()['password']
    email = request.get_json()['email']
    degree = request.get_json()['degree']

    try:
        admin = Admin(name=username, password=password, email=email, degree=degree, is_delete=False)
        db.session.add(admin)
        db.session.commit()
    except EOFError:
        db.session.callback()
        return jsonify({'msg': False, 'code': 500, 'token': 'feifei'})

    return jsonify({'msg': True, 'code': 200, 'token': 'feifei'})


# 管理员修改密码接口
@app.route('/modify', methods=['POST'])
def doModify():
    username = request.get_json()['username']
    password = request.get_json()['password']
    newPassword = request.get_json()['newPassword']

    print(username, password, newPassword)

    user = Admin.query.filter(Admin.name == username, Admin.password == password, Admin.is_delete == False).first()
    if user:
        # url_for()方法传入路由对应的函数就会返回路由对应的地址，
        # redirect()传入路由地址作为参数并且返回就会重定向置该路由执行该路由操作
        # 用户密码更新
        user.password = newPassword
        db.session.commit()
        return jsonify({'code': 200, 'msg': 'success', 'token': 'feifei'})
    else:
        return jsonify({'code': 500, 'msg': 'error', 'token': 'feifei'})


# 管理员冻结账户
@app.route('/freezeAccount', methods=['POST'])
def doFreezeAccount():
    username = request.get_json()['username']
    user = Admin.query.filter(Admin.name == username, Admin.is_delete == False).first()
    if user:
        user.is_delete = True
        db.session.commit()

        return jsonify({'code': 200, 'msg': 'success', 'token': 'feifei'})
    else:
        return jsonify({'code': 500, 'msg': 'error', 'token': 'feifei'})


# 密文分类数据记录接口
@app.route('/ClassifyRecords', methods=['GET'])
def getClassifyRecords():
    # 获取前端页码page以及每页数据量限制limit参数
    page = request.args.get('page')
    limit = request.args.get('limit')
    # 获取 is_delete 置为False的所有分类记录数据
    data = getMysqlExportData("classifyrecords")
    count = len(data)

    start = (int(page) - 1) * int(limit)
    end = int(page) * int(limit)
    return_data = data[start: end]

    return jsonify({"code": 0, "msg": "success", "count": count, "data": return_data})


# 删除密文分类记录数据接口
@app.route('/deleteClassifyRecord', methods=['POST'])
def deleteClassifyRecord():
    # 获取POST请求传递过来的id
    id = request.get_json()['id']
    # 通过id查找对应的密文分类记录
    clRecord = ClassifyRecord.query.filter(ClassifyRecord.id == id).first()
    if clRecord:
        clRecord.is_delete = True
        db.session.commit()

        return jsonify({'code': 200, 'msg': 'success', 'token': 'feifei'})
    else:
        return jsonify({'code': 500, 'msg': 'error', 'token': 'feifei'})


# 修改密文分类记录数据接口
@app.route('/editClassifyRecord', methods=['POST'])
def editClassifyRecord():
    # 获取POST请求传递过来的id
    id = request.get_json()['id']
    admin = request.get_json()['admin']
    fileName = request.get_json()['fileName']
    size = request.get_json()['size']
    result = request.get_json()['result']
    confidence = request.get_json()['confidence']
    datetime = request.get_json()['datetime']
    print(id, admin)

    # 通过id查找对应的密文分类记录
    clRecord = ClassifyRecord.query.filter(ClassifyRecord.id == id).first()
    if clRecord:
        if admin != '':
            clRecord.admin = admin
        if fileName != '':
            clRecord.fileName = fileName
        if size != '':
            clRecord.size = size
        if result != '':
            clRecord.result = result
        if confidence != '':
            clRecord.confidence = confidence
        if datetime != '':
            clRecord.datetime = datetime

        db.session.commit()

        return jsonify({'code': 200, 'msg': 'success', 'token': 'feifei'})
    else:
        return jsonify({'code': 500, 'msg': 'error', 'token': 'feifei'})


# 分类记录模糊查询接口
@app.route('/selectClassifyRecords', methods=['GET'])
def getSelectRecords():
    title = request.args.get('title')
    # 首先获取指定表中 is_delete 置为False的所有数据
    data = getMysqlExportData('classifyrecords')
    # 对数据进行模糊查询并返回查询结果
    result = FuzzyFinder(user_input=title, collection=data)
    return jsonify({"code": 0, "msg": "success", "count": len(result), "data": result})


# 各项特征p-value统计数据接口
@app.route('/statistics/p-value', methods=['GET'])
def index():
    # 获取前端选择的特征参数加密算法以及加密模式
    Algorithm = request.args.get('Algorithm')
    Mode = request.args.get('Mode')
    print(Algorithm, Mode)

    fileName = ''
    if Algorithm in ['DES', '3DES', 'AES', 'Blowfish']:
        fileName = Algorithm + '_' + Mode + '.csv'
    else:
        fileName = Algorithm + '.csv'

    # os拼接密文特征文件地址
    filePath = os.path.join('static/features', fileName)
    # 读取密文特征文件
    featuresData = pandas.read_csv(filePath, encoding='utf-8', index_col=0)
    features = featuresData.columns
    result = {}
    # 循环计算每个p-value范围内的样本数量，以0.01为范围步长
    for feature in features:
        temp = []
        for i in numpy.arange(0, 1, 0.01):
            temp.append(staticsSum(featuresData[feature], i, i + 0.01))
        result[feature] = temp

    # 读取随机特征文件
    random_features = pandas.read_csv('static/features/randomfiletest.csv', encoding='utf-8', index_col=0)
    features_norm = random_features.columns
    random_result = {}
    # 循环计算每个p-value范围内的样本数量，以0.01为范围步长
    for feature in features_norm:
        temp = []
        for i in numpy.arange(0, 1, 0.01):
            temp.append(staticsSum(random_features[feature], i, i + 0.01))
        random_result[feature] = temp

    return jsonify({"code": 200, "msg": "success", "data": result, 'random_feature': random_result})


# 前端上传特征文件路由接口，layui上传文件的请求方式默认为post
@app.route('/pvalue_file_upload', methods=['POST'])
def pvalueFileUpload():
    # 获取前端文件
    fileObject = request.files.get('file')
    fileName = fileObject.filename
    print('static/' + fileName)
    # 如果前端上传的文件时zip压缩文件
    if fileName.endswith('.zip'):
        # 先将压缩文件保存在本地
        fileObject.save('static/zipFile/' + fileName)
        # 读取压缩文件并解压到features文件夹
        zipFile = zipfile.ZipFile('static/zipFile/' + fileName)
        zipFile.extractall('static/features')
        zipFile.close()

    else:
        # 不是zip就是csv文件，这个前端已经做出了识别，可以直接保存到features文件夹
        fileObject.save('static/features/' + fileName)

    return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})


# todo:密文文件上传以及密文识别的两个接口转至8080端口
'''

'''


# 进行明文/密文 的 加密/解密
@app.route('/encryption', methods=['GET'])
def doEncryption():
    Algorithm = request.args.get('Algorithm')
    PassWord = request.args.get('PassWord')
    Text = request.args.get('Text')
    event = request.args.get('event')
    # print(Algorithm, PassWord, Text, event)

    Symmetric_Selection = {
        'DES': DES_ECB_class(), '3DES': DES3_ECB_class(), 'AES': AES_ECB_class(),
        'Blowfish': Blowfish_ECB_class(), 'RC4': RC4_class()
    }
    Asymmetric_Selection = {'RSA': RSA_class()}
    Hash_Selection = {'MD5': Md5, 'SHA-1': Sha1, 'SHA-512': Sha512}

    ConverText = ''
    # 加密算法为对称加密的情况
    if Algorithm in Symmetric_Selection.keys():
        Cipher_Object = Symmetric_Selection.get(Algorithm)
        # 用于捕抓使用非正确密码解密密文或者非正确加密的操作
        try:
            if event == 'encryption':
                ConverText = Cipher_Object.encrypt(key=PassWord, data=Text)
            elif event == 'decryption':
                ConverText = Cipher_Object.decrypt(key=PassWord, encrypto_data=Text)

        # 密码错误会引发ValueError报错
        except ValueError:
            if event == 'encryption':
                ConverText = 'encode error!(The password length may be wrong!/or the password degenerates!)'
            elif event == 'decryption':
                ConverText = 'decode error!'
            return jsonify({"code": 200, "msg": "false", "data": ConverText})
        # 如果无异常，则msg置为success
        else:
            return jsonify({"code": 200, "msg": "success", "data": ConverText})

    # 加密算法为非对称的情况
    elif Algorithm in Asymmetric_Selection.keys():
        Cipher_Object = Asymmetric_Selection.get(Algorithm)
        # 用于捕抓使用非正确密码或者非正确密文的错误操作
        try:
            if event == 'encryption':
                # 加载公钥文件
                with open('main/public.pem') as publickfile:
                    p = publickfile.read()
                    pub_key = rsa.PublicKey.load_pkcs1(p)
                ConverText = Cipher_Object.encrypt(data=Text, pub_key=pub_key)
            elif event == 'decryption':
                # 加载私钥文件
                with open('main/private.pem') as privatefile:
                    p = privatefile.read()
                    priv_key = rsa.PrivateKey.load_pkcs1(p)
                ConverText = Cipher_Object.decrypt(encrypto_data=Text, priv_key=priv_key)

        # 密文无法被私钥解密会捕获此错误
        except rsa.pkcs1.DecryptionError:
            ConverText = 'Decryption failed!'
            return jsonify({"code": 200, "msg": "false", "data": ConverText})
        # 密文长度不对会捕获此错误
        except binascii.Error:
            ConverText = 'Decryption failed!'
            return jsonify({"code": 200, "msg": "false", "data": ConverText})
        else:
            return jsonify({"code": 200, "msg": "success", "data": ConverText})

    else:
        Cipher_Function = Hash_Selection.get(Algorithm)
        ConverText = Cipher_Function(Text)

        return jsonify({"code": 200, "msg": "success", "data": ConverText})


# 系统算法训练数据集请求接口
@app.route('/dataSet', methods=['GET'])
def getTestSet():
    # page = request.args.get('page')
    # limit = request.args.get('limit')
    # 获取 is_delete 置为False的所有测试集数据
    data = getMysqlExportData('datasetrecords')
    count = len(data)

    # start = (int(page) - 1) * int(limit)
    # end = int(page) * int(limit)
    # return_data = data[start: end]

    return jsonify({"code": 0, "msg": "success", "count": count, "data": data})


# 个人日志数据请求接口
@app.route('/personalLog', methods=['POST'])
def getPersonalLog():
    username = request.get_json()['username']
    # 获取前端页码page以及每页数据量限制limit参数
    page = request.get_json()['page']
    limit = request.get_json()['limit']

    # print(username, page, limit)

    suggestions = []
    # 读取日志文件中的数据，提取该用户的日志信息
    with open(file='System.log', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # 去除换行符
            line = line.replace('\n', '')
            # print(line)
            logPieceList = line.split(' - ')
            # 匹配到了该用户名就将数据加入
            if logPieceList[1] == username:
                temp_dict = {}
                temp_dict['username'] = logPieceList[1]
                temp_dict['time'] = logPieceList[0]
                temp_dict['status'] = logPieceList[2]
                temp_dict['logDetail'] = logPieceList[3]
                temp_dict['ip'] = logPieceList[4]

                suggestions.append(temp_dict)

    suggestions = sorted(suggestions, key=lambda x: x['time'], reverse=True)
    count = len(suggestions)

    start = (int(page) - 1) * int(limit)
    end = int(page) * int(limit)
    return_data = suggestions[start: end]

    return jsonify({"code": 0, "msg": "success", "count": count, "data": return_data})


# 系统日志数据请求接口
@app.route('/consoleLog', methods=['POST'])
def getConsoleLog():
    # 获取前端页码page以及每页数据量限制limit参数
    page = request.get_json()['page']
    limit = request.get_json()['limit']

    suggestions = []
    # 读取日志文件中的数据，提取该用户的日志信息
    with open(file='System.log', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # 去除换行符
            line = line.replace('\n', '')
            # print(line)
            logPieceList = line.split(' - ')
            # 匹配到了该用户名就将数据加入
            temp_dict = {}
            temp_dict['username'] = logPieceList[1]
            temp_dict['time'] = logPieceList[0]
            temp_dict['status'] = logPieceList[2]
            temp_dict['logDetail'] = logPieceList[3]
            temp_dict['ip'] = logPieceList[4]

            suggestions.append(temp_dict)

    suggestions = sorted(suggestions, key=lambda x: x['time'], reverse=True)
    count = len(suggestions)

    start = (int(page) - 1) * int(limit)
    end = int(page) * int(limit)
    return_data = suggestions[start: end]

    return jsonify({"code": 0, "msg": "success", "count": count, "data": return_data})


# 系统日志数据模糊查询接口
@app.route('/selectConsoleLog', methods=['POST'])
def selectConsoleLog():
    # 获取前端页码page以及每页数据量限制limit参数
    keyword = request.get_json()['keyword']

    suggestions = []
    # 读取日志文件中的数据，提取该用户的日志信息
    with open(file='System.log', mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            # 去除换行符
            line = line.replace('\n', '')
            # print(line)
            logPieceList = line.split(' - ')
            # 匹配到了该用户名就将数据加入
            temp_dict = {}
            temp_dict['username'] = logPieceList[1]
            temp_dict['time'] = logPieceList[0]
            temp_dict['status'] = logPieceList[2]
            temp_dict['logDetail'] = logPieceList[3]
            temp_dict['ip'] = logPieceList[4]

            suggestions.append(temp_dict)

    return_data = FuzzyFinder(user_input=keyword, collection=suggestions)
    count = len(return_data)

    return jsonify({"code": 0, "msg": "success", "count": count, "data": return_data})


# 用户信息数据请求接口
@app.route('/userInform', methods=['POST'])
def getUserInform():
    # 获取前端页码page以及每页数据量限制limit参数
    page = request.get_json()['page']
    limit = request.get_json()['limit']

    data = getMysqlExportData('admins')
    count = len(data)

    start = (int(page) - 1) * int(limit)
    end = int(page) * int(limit)
    return_data = data[start: end]

    return jsonify({"code": 0, "msg": "success", "count": count, "data": return_data})


# 修改用户信息数据接口
@app.route('/modifyUserInform', methods=['POST'])
def ModifyUserInform():
    id = request.get_json()['id']
    name = request.get_json()['username']
    password = request.get_json()['password']
    email = request.get_json()['email']
    degree = request.get_json()['degree']
    is_delete = request.get_json()['is_delete']

    # 将前端传递过来的字符串转化为boolean型数据传递给数据库
    if is_delete == 'false':
        is_delete = False

    else:
        is_delete = True

    try:
        user = Admin.query.filter(Admin.id == id).first()
        user.degree = degree
        user.is_delete = is_delete
        if name != '':
            user.name = name
        if password != '':
            user.password = password
        if email != '':
            user.email = email

        db.session.commit()

    except OSError:
        # todo: 事务回滚？
        db.session.rollback()
        return jsonify({'msg': False, 'code': 500, 'token': 'feifei'})
    return jsonify({'msg': True, 'code': 200, 'token': 'feifei'})


# 生成NIST检测指标p值的文件上传接口
@app.route('/ciphertxt_file_upload', methods=['POST'])
def cipherFileUpload():
    fileObject = request.files.get('file')
    fileName = fileObject.filename
    # fileContent = fileObject.read().decode(encoding='utf-8') 可读取fileObject流中的数据

    # 获取featuresGenerate文件夹中密文的文件名列表
    ls = os.listdir('static/FeaturesGenerate')
    if ls:
        # 采用循环删除CiphertextFile文件夹中的所有文件
        for filename in ls:
            if os.path.isdir('static/FeaturesGenerate/' + filename):
                shutil.rmtree('static/FeaturesGenerate/' + filename)
            else:
                os.remove('static/FeaturesGenerate/' + filename)
    # if ls:
    #     # 采用循环删除featuresGenerate文件夹中的所有文件
    #     for filename in ls:
    #         os.remove('static/FeaturesGenerate/' + filename)

    # 保存不同类型的文件
    if fileName.endswith('.txt'):
        fileObject.save('static/FeaturesGenerate/' + fileName)

    elif fileName.endswith('.zip'):
        # 先将压缩文件保存在本地
        fileObject.save('static/zipFile/' + fileName)
        # 读取压缩文件并解压到features文件夹
        zipFile = zipfile.ZipFile('static/zipFile/' + fileName)
        zipFile.extractall('static/FeaturesGenerate')
        zipFile.close()

    return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})


'''
# 密文文件生成NIST检测指标p值的功能接口
@app.route('/cipherFeaturesGenerate', methods=['POST'])
def doFeaturesGenerate():
    # suggestions列表用于存储特征字典
    suggestions = []

    filename_list = os.listdir('static/FeaturesGenerate')
    if filename_list:

        # 循环读取16进制字符串文件并计算特征值
        for filename in filename_list:
            file_dir = 'static/FeaturesGenerate/' + filename

            with open(file=file_dir, mode='r', encoding='utf-8') as f:
                fileContent = f.read()

            # 先调用函数将16进制字符串转化为二进制int型0/1列表
            bits = hex_to_binarylist(hex_str=fileContent)
            result_list, result_dict = getRandomnessTest.GetRandomnessTest(bits=bits, Linear_len=500, Linear_N_block=30)
            result_dict['filename'] = filename

            suggestions.append(result_dict)

    # 将NIST计算结果存到一个json文件中
    with open(file='static/FeaturesGenerate.json', mode='w', encoding='utf-8') as f:
        json.dump(suggestions, f)

    return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})
'''


# 采用celery异步任务队列生成NIST检测指标p值
@app.route('/cipherFeaturesGenerate', methods=['POST'])
def doFeaturesGenerate():
    # 返回执行者的名称，以便匹配邮箱发送系统执行功能结果
    username = request.get_json()['username']
    userdegree = request.get_json()['userdegree']

    # 根据系统用户的等级来指定celery队列中任务的优先级别
    if userdegree=='Advanced':
        priority = 3
    elif userdegree=='Medium':
        priority = 2
    else:
        priority = 1

    features_Generate.apply_async(kwargs={'username': username}, priority=priority)

    return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})


# 密文文件生成NIST检测指标p值的功能接口
@app.route('/selectFeaturesGenerate', methods=['POST'])
def selectFeaturesGenerate():
    # 获取前端页码page以及每页数据量限制limit参数
    page = request.get_json()['page']
    limit = request.get_json()['limit']

    with open(file='static/FeaturesGenerate.json', mode='r', encoding='utf-8') as f:
        # 将数据写入json文件
        # json.dump(result, f)
        suggestions = json.load(f)

        start = (int(page) - 1) * int(limit)
        end = int(page) * int(limit)
        return_data = suggestions[start: end]

        return jsonify({"code": 0, "msg": "success", 'count': len(suggestions), 'data': return_data})


# 获取ZipFile静态文件接口
@app.route('/getZipFile', methods=['POST'])
def getZipFile():
    # 获取前端页码page以及每页数据量限制limit参数
    page = request.get_json()['page']
    limit = request.get_json()['limit']

    suggestions = []
    filename_list = os.listdir('static/zipFile')

    for filename in filename_list:
        temp = {}

        file_dir = 'static/zipFile/' + filename

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
        temp['status'] = 'Temporary File'

        suggestions.append(temp)

    start = (int(page) - 1) * int(limit)
    end = int(page) * int(limit)
    return_data = suggestions[start: end]

    return jsonify({"code": 0, "msg": "success", 'count': len(suggestions), 'data': return_data})


# 删除ZipFile文件请求接口
@app.route('/delZipFile', methods=['POST'])
def delZipFile():
    filename = request.get_json()['filename']
    if filename in os.listdir('static/zipFile'):
        file_dir = 'static/zipFile/' + filename
        os.remove(file_dir)

        return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})

    else:
        return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})


# 获取static静态文件接口
@app.route('/getStaticFiles', methods=['POST'])
def getStaticFiles():
    # 获取前端页码page以及每页数据量限制limit参数
    page = request.get_json()['page']
    limit = request.get_json()['limit']
    folder = request.get_json()['folder']

    print(folder)

    suggestions = []
    if folder == 'singlefile':
        for filename in os.listdir('static'):
            if os.path.isfile('static/' + filename):
                temp = {}
                file_dir = 'static/' + filename
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
                temp['status'] = folder + "[Showing]"

                suggestions.append(temp)

    else:
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
            if folder == 'zipFile':
                temp['status'] = folder + "[Temporary File]"

            elif folder == 'CiphertextFile' or folder == 'FeaturesGenerate':
                temp['status'] = folder + "[Repeat Call]"

            elif folder == 'features':
                temp['status'] = folder + "[Showing]"

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

    elif "CiphertextFile" in status:
        if filename in os.listdir('static/CiphertextFile'):
            file_dir = 'static/CiphertextFile/' + filename
            os.remove(file_dir)

            return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})
        else:
            return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})

    elif "FeaturesGenerate" in status:
        if filename in os.listdir('static/FeaturesGenerate'):
            file_dir = 'static/FeaturesGenerate/' + filename
            os.remove(file_dir)

            return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})
        else:
            return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})

    elif "features" in status:
        if filename in os.listdir('static/features'):
            file_dir = 'static/features/' + filename
            os.remove(file_dir)

            return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})
        else:
            return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})

    elif "singlefile" in status:
        if filename in os.listdir('static'):
            file_dir = 'static/' + filename
            os.remove(file_dir)

            return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})
        else:
            return jsonify({"code": 500, "msg": "error", 'token': 'feifei'})



# 网络抓包请求接口
@app.route('/PackageCapture', methods=['GET'])
def getPackage():
    # 返回执行者的名称，以便匹配邮箱发送系统执行功能结果
    username = request.args.get('username')
    userdegree = request.args.get('userdegree')

    # 根据系统用户的等级来指定celery队列中任务的优先级别
    if userdegree == 'Advanced':
        priority = 3
    elif userdegree == 'Medium':
        priority = 2
    else:
        priority = 1

    netpackage_capture.apply_async(kwargs={'username': username}, priority=priority)

    return jsonify({"code": 200, "msg": "success", 'token': 'feifei'})



if __name__ == '__main__':
    # 注释如果再次运行，数据库已经保存内容
    '''
    db.drop_all()
    db.create_all()

    admin_1 = Admin(name='feifei', password='20000', email='2379631316@qq.com', degree='Advanced', is_delete=False)
    admin_2 = Admin(name='袁楚轩', password='12345', email='1290163467@qq.com', degree='Medium', is_delete=False)
    admin_3 = Admin(name='杨嘉雄', password='12312', email='2625398619@qq.com', degree='Medium', is_delete=False)
    admin_4 = Admin(name='test-Advanced', password='123', email='15931695205@163.com', degree='Advanced', is_delete=False)
    admin_5 = Admin(name='test-Medium', password='123', email='15931695205@163.com', degree='Medium', is_delete=False)
    admin_6 = Admin(name='test-Junior', password='123', email='15931695205@163.com', degree='Junior', is_delete=False)
    # admin_3 = Admin(name='admin', password='123456', is_delete=False)
    db.session.add_all([admin_1, admin_2, admin_3, admin_4, admin_5, admin_6])

    dataRecord_1 = dataSetRecord(dataSetName="CIFAR-10 python version 图片数据集",
                                 source="http://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz",
                                 introduction="本身具有良好的标签 数据格式为：<标签> <3072byte个像素>（其中3*1024个rgb图）。该数据集共有60000张彩色图像，这些图像大小为32*32，分为10个类，每类6000张图。 这里面有50000张用于训练，另外10000用于测试。",
                                 filetype="tar.gz", size="163MB", sizeAfterCipher="1.72GB", is_delete=False)
    dataRecord_2 = dataSetRecord(dataSetName="Caltech256 图片数据集",
                                 source="http://www.vision.caltech.edu/Image_Datasets/Caltech256/256_ObjectCategories.tar",
                                 introduction="包含30607张图片，256类图片，每类图片最少有80张图片。照片大小不固定， 每张照片都进行过挑选，因此可以认为是具有良好标签的数据。",
                                 filetype="	tar", size="1.2GB", sizeAfterCipher="8.84GB", is_delete=False)
    dataRecord_3 = dataSetRecord(dataSetName="LibriSpeech ASR corpus",
                                 source="https://openslr.magicdatatech.com/resources/12/train-clean-100.tar.gz",
                                 introduction="是一个包含大约1000小时的英语语音的大型语料库， 它被分割并对齐，整理成每条10秒左右的、经过文本标注的音频文件。",
                                 filetype="	tar.gz", size="6.3GB", sizeAfterCipher="38.8GB", is_delete=False)
    dataRecord_4 = dataSetRecord(dataSetName="THUCNews",
                                 source="https://thunlp.oss-cn-qingdao.aliyuncs.com/THUCNews.zip",
                                 introduction="根据新浪新闻RSS订阅频道2005~2011年间的历史数据筛选过滤生成均为纯文字的新闻文本，大小不固定这里我们选取了其中财经、股票、时政、体育四个类别中的568个文件进行加密。",
                                 filetype="zip", size="15.3MB", sizeAfterCipher="125MB", is_delete=False)
    db.session.add_all([dataRecord_1, dataRecord_2, dataRecord_3, dataRecord_4])

    db.session.commit()
    '''

    app.run(host='0.0.0.0', port=8000)
