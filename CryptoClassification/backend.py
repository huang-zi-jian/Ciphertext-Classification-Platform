# !/usr/bin/python
# -*- coding:utf-8 -*-
# @Time     : 2021/3/16 17:43
# @Author   : JamesYang
# @File     : backend.py

import os
import time

import BM
import DM

'''
此代码的注释是由杨嘉雄完成的，有任何问题，请联系本人
'''


class Args:
    def __init__(self, crypto_list: list, category: int, input_channel: int, col_name: list, ratio=0.0, epoch=30,
                 batch=300, loss_function='CE', optimizer='Adam', save_mode='total'):
        self.crypto_list = crypto_list  # 传入有可能是被谁加密的加密函数列表
        self.category = category  # len(crypto_list)  这就代表了几分类
        self.ratio = ratio  # 默认传0
        self.input_channel = input_channel  # 特征的数目  神经网络要用  先传1024
        self.epoch = epoch  # 可以让用户选择的，默认30
        self.batch = batch  # 可以让用户选择的，默认300
        self.loss_function = loss_function  # 可以让用户选择的 'NLL'、'MSE'、'CE'三种  ，默认CE
        self.optimizer = optimizer  # 可以让用户选择的 'Adam'、'RMSprop'、'Adadelta'、'SGD'四种  ，默认Adam
        self.save_mode = save_mode  # 模型是如何保存的（total、para）  默认total
        self.col_name = col_name  # 选择的特征，他们的名字

    def change_save_mode(self, value):
        self.save_mode = value

    def change_crypto_list(self, c_list):
        self.crypto_list = c_list

'''
def read_raw_files(file_dir):
    """
    读取文件夹下面的文件，用于自适应文件名。Attention ! 不能递归读取
    :param file_dir: 传入要读取的文件夹路径
    :return: 每个文件的地址和文件大小，list
    """
    file_list = os.listdir(file_dir)
    file_size = []
    file_dirs = []
    for file in file_list:
        if file.startswith('.'):
            continue
        path = file_dir + file
        file_dirs.append(path)
        file_size.append(str(round(os.path.getsize(path)/1024)) + 'kb')
    return file_dirs, file_size
'''
# 递归获取文件夹中的所有文件location
def get_all(file_dir):
    result = []
    get_dir = os.listdir(file_dir)

    for i in get_dir:
        sub_dir = os.path.join(file_dir, i)
        if os.path.isdir(sub_dir):
            result = result + get_all(sub_dir)
        else:
            result.append(sub_dir)

    return result

def read_raw_files(file_dir):
    """
    读取文件夹下面的文件，用于自适应文件名。Attention ! 不能递归读取
    :param file_dir: 传入要读取的文件夹路径
    :return: 每个文件的地址和文件大小，list
    """
    file_list = get_all(file_dir)
    file_size = []
    file_dirs = []
    for file_path in file_list:
        if os.path.basename(file_path).startswith('.'):
            continue
        file_dirs.append(file_path)
        file_size.append(str(round(os.path.getsize(file_path)/1024)) + 'kb')
    return file_dirs, file_size


def getCipherResult(file_dir: str, model_name: str, args):
    """
    主调接口，用户上传待测密文文件，使用现有模型进行分类

    :param file_dir:  当前用户文件上传的顶层目录
    :param model_name:  验证所选取的模型名称  四选一
    :param args: 辅助参数
    :return: result-dict list and a timestamp
    """
    args.change_crypto_list(DM.concat(args.crypto_list))
    # 读文件夹  得到两个list [文件名],[大小]
    file_list, file_size = read_raw_files(file_dir)
    timestamp = time.localtime()
    time_format = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    # 开始执行核心分类功能
    if model_name == 'SVM' or model_name == 'RF':
        args.change_save_mode('total')  # 这里为了保证模型的读取模式正确，将此参数设置死
        result, confidence = BM.load_and_test(file_list, model_name, args)

    else:
        args.change_save_mode('para')
        result, confidence = DM.load_and_test(model_name, file_list, args)
    # 设置阈值
    threshold = 1 / args.category  # todo 这里是否要提高难度，1.5或者2？
    return_result = []

    # create result-dict list
    if isinstance(confidence, list):  # 判断是基础模块还是深度模块
        for i in range(len(result)):
            if confidence[i] < threshold:
                status = False
            else:
                status = True
            return_result.append({"fileName": os.path.basename(file_list[i]),
                                  "size": file_size[i],
                                  "status": status,
                                  "result": result[i],
                                  "confidence": confidence[i]})
    else:
        if confidence < threshold:
            status = False
        else:
            status = True
        for i in range(len(result)):
            return_result.append({"fileName": os.path.basename(file_list[i]),
                                  "size": file_size[i],
                                  "status": status,
                                  "result": result[i],
                                  "confidence": confidence})

    return return_result, time_format


def getTrainedModel(file_dir: str, model_name: str, args):
    """
    主调接口，用户上传已经分好类的密文文件，用于训练模型

    :param file_dir: 提供所有密文文件最上层路径
    :param model_name: 训练模型的种类
    :param args: 必备参数，针对不同的模型有不同的训练参数
    :return: result dict
    """
    args.change_crypto_list(DM.concat(args.crypto_list))  # 重新排序
    crypto_files = {}
    for i in args.crypto_list:  # 读取各个分好类的密文文件夹
        crypto_files[i] = read_raw_files(file_dir + i + '/')[0]
    timestamp = time.localtime()
    time_format = time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    # 模型正式开始训练
    if model_name == 'SVM' or model_name == 'RF':
        args.change_save_mode('total')  # 保证模型的保存模式正确
        accuracy, pic_path, model_path = BM.train_and_test(crypto_files, model_name, args)
    else:
        args.change_save_mode('para')
        pic_path, model_path, accuracy = DM.train_and_test(model_name, crypto_files, args)

    # create result dict
    return {
        'model_name': model_name,
        'time': time_format,
        'pic_dir': pic_path,
        'model_dir': model_path,
        'accuracy': accuracy
    }


# 例子
if __name__ == '__main__':
    # # args1 = Args(['AES', 'RSA'], 2, 1024, col_name=['data_frame'], batch=300, epoch=30, ratio=0.8,
    # #              save_mode='para')
    # args1 = Args(['3DES', 'AES'], 2, 1024, col_name=['data_frame'], batch=300, epoch=30, ratio=0.8,
    #              save_mode='para')
    # # return_result, time_format = getCipherResult('', 'SCNN', args1)
    # # print(return_result)
    # # print(time_format)
    # result_dict = getTrainedModel('static/trainModelFile/', 'SCNN', args1)
    # print(result_dict)
    # # lst = ['AES', 'Blowfish','SHA-1','DES']
    # # lst = DM.concat(lst)
    # # args = Args(lst, 2, 1024, ['data_frame'])
    # # getCipherResult('ciphertext/feature/aaa.csv', 'RF', args)

    print(read_raw_files('static/CiphertextFile/'))
