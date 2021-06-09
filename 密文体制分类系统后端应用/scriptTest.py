import shutil
import os
import ntpath
import json

# ls = os.listdir('static/CiphertextFile')
# for filename in ls:
#     os.remove('static/CiphertextFile/' + filename)
# os.remove('static/CiphertextFile/abc.csv')
# shutil.rmtree('static/CiphertextFile')

# testdict = {'DES':'on'}
#
# if 'DES' in testdict.keys():
#     print(1)

# filename = ntpath.basename('static/CiphertextFile/aaa.csv')
# print(filename)

# t_list = [1,2,3,4]
# print(t_list[0:2])

import logging

# # 创建一个logger
# logger = logging.getLogger(name='mylogger')
# logger.setLevel(logging.DEBUG)
#
# # 创建一个handler，用于写入日志文件
# fh = logging.FileHandler('System.log', mode='a', encoding='utf-8')
# fh.setLevel(logging.DEBUG)
#
# # 再创建一个handler，用于输出到控制台
# ch = logging.StreamHandler()
# ch.setLevel(logging.WARNING)
#
# # 定义handler的输出格式
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# ch.setFormatter(formatter)
#
# # 给logger添加handler
# logger.addHandler(fh)
# logger.addHandler(ch)
#
# # 记录一条日志
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')
#
# logging.debug('debug message')
# logging.info('info message')
# logging.warn('warn message')
# logging.error('error message')
# logging.critical('critical message')


# with open(file='System.log', mode='r', encoding='utf-8') as f:
#     lines = f.readlines()
#     for line in lines:
#         # 去除换行符
#         line = line.replace('\n', '')
#         # print(line)
#         print(line.split(' - '))
#         # print(line)

# os.remove('static/zipFile/test.zip')
import time

# modifiedTime = time.localtime(os.stat("static/zipFile/features.zip").st_mtime)
# createdTime = time.localtime(os.stat("static/zipFile/features.zip").st_ctime)
#
# mTime = time.strftime('%Y-%m-%d %H:%M:%S', modifiedTime)
# cTime = time.strftime('%Y-%m-%d %H:%M:%S', createdTime)
#
# print("modifiedTime " + mTime)
# print("createdTime " + cTime)
# ls = os.listdir('static/zipFile')
# print(ls)


'''
for root, dirs, files in os.walk('static'):
    # print(root)
    # print(dirs)
    for file in files:
        print(file)

print(os.listdir('static'))
'''


import pandas
from main.functions import staticsSum
import numpy

'''
random_features = pandas.read_csv('static/features/random_feature.csv', encoding='utf-8', index_col=0)
features_norm = random_features.columns
random_result = {}
# 循环计算每个p-value范围内的样本数量，以0.01为范围步长
for feature in features_norm:
    temp = []
    for i in numpy.arange(0, 1, 0.01):
        temp.append(staticsSum(random_features[feature], i, i + 0.01))
    random_result[feature] = temp

print(random_result)
'''


# import zipfile
#
# zf = zipfile.ZipFile('test.zip', 'w', zipfile.ZIP_DEFLATED)
# zf.write('System.log')
# zf.close()
#
# os.sendfile()

# file_src = 'trained_model/SCNN/SCNN_3DES_ECB_ones&AES_ECB_ones&Blowfish_ECB_ones&RSA_ones&SHA-1_ones_parameter.pkl'
# file_arc = os.path.basename(file_src)
# print(file_arc)
# from unrar import rarfile
import zipfile

zipFile = zipfile.ZipFile('/Users/feifei/Downloads/测试——分类数据.zip')
print(zipFile.namelist())
zipFile.extractall('static/CiphertextFile')