'''
author: feifei
date: 2021-2-4
file info: 实现一些外部方法
file change: 2021-3-1增加 fuzzyfinder 模糊查询实现接口
'''
import pandas
import numpy
import re
import pymysql
pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()
# from pymysql import connect
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os


# 统计一个序列数中在指定范围内的数据个数
def staticsSum(Series, start, end):
    # .sum返回的是numpy类型的int64，不能被json序列化，所以应该直接转为int型
    sum = int(((Series > start) & (Series < end)).sum())
    return sum


# user_input表示用户输入的查询字段，collection为所有的待查询数据
def fuzzyfinder(user_input, collection):
    suggestions = []
    # 加上?表示非贪婪匹配
    pattern = '.*?'.join(user_input)
    regex = re.compile(pattern)

    for item in collection:
        # 匹配成功后search返回match对象，否则返回None
        match = regex.search(item)
        # print('match', match)
        if match:
            # print('group', match.group(), match.start())
            # match.group()返回正则匹配到的字符串，match.start()返回匹配开始的下标
            suggestions.append((len(match.group()), match.start(), item))

    # print(suggestions)
    # print(sorted(suggestions))
    return [x for _, _, x in sorted(suggestions)]


# 获取数据库中某个表的所有数据（被is_delete标记为True的数据除外），并且以字典格式返回
def getMysqlExportData(tableName):
    suggestions = []
    connect = pymysql.connect
    conn = connect(host='127.0.0.1', user='root', password='feifei@whut', port=3306, database='Cipher_Classify_base', charset='utf8')
    # conn = connect(host='127.0.0.1', user='root', passwd='feifei', port=3306, database='Cipher_Classify_base', charset='utf8')
    cursor = conn.cursor()

    if tableName=='admins':
        cursor.execute("select * from admins;")
        mysqlData_list = cursor.fetchall()
        for id, name, password, email, degree, is_delete in mysqlData_list:
            # 将注销状态0和1转化为boolean型
            if is_delete==0:
                is_delete = False
            else:
                is_delete = True

            mysqlData_dict = {
                "id": id,
                "name": name,
                "password": password,
                "email": email,
                "degree": degree,
                "is_delete": is_delete
            }
            suggestions.append(mysqlData_dict)

        return suggestions

    else:
        count = cursor.execute("select * from " + tableName + " where is_delete=False;")

        if count:
            mysqlData_list = cursor.fetchall()
            if tableName=='classifyrecords':
                for id, admin, fileName, size, result, status, confidence, datetime, _ in mysqlData_list:
                    mysqlData_dict = {
                        "id": id,
                        "admin": admin,
                        "fileName": fileName,
                        "size": size,
                        "result": result,
                        "status": status,
                        "confidence": confidence,
                        "datetime": datetime
                    }
                    suggestions.append(mysqlData_dict)
		# 将分类数据结果按照id降序排列返回，确保优先展示最近一次的数据
                suggestions = sorted(suggestions, key=lambda x: x['id'], reverse=True)

            elif tableName=='datasetrecords':
                for id, dataSetName, source, introduction, filetype, size, sizeAfterCipher, _ in mysqlData_list:
                    mysqlData_dict = {
                        # "id": id,
                        "dataSetName": dataSetName,
                        "source": source,
                        "introduction": introduction,
                        "filetype": filetype,
                        "size": size,
                        "sizeAfterCipher": sizeAfterCipher
                    }
                    suggestions.append(mysqlData_dict)

            return suggestions

        else:
            return False



def FuzzyFinder(user_input, collection):
    '''

    :param user_input: 查询字段
    :param collection: 数据库中的每条数据以字典格式存放在列表中
    :return: 返回模糊查询匹配到的数据
    '''
    suggestions = []
    # 加上?表示非贪婪匹配
    pattern = '.*?'.join(user_input)
    regex = re.compile(pattern)
    # 取两数的最小值并且返回
    gfun = lambda x, y: x if x < y else y

    for item in collection:
        # 初始化匹配长度为1000
        matchLength = 1000
        # 对字典中的每个键值进行正则匹配
        for value in item.values():
            # 匹配成功后search返回match对象，否则返回None
            match = regex.search(str(value))
            if match:
                # 找到匹配长度的最小值作为该条数据的Rank标准
                matchLength = gfun(matchLength, len(match.group()))
                # match.group()返回正则匹配到的字符串，match.start()返回匹配开始的下标

        if matchLength < 1000:
            suggestions.append((matchLength, item))
    # 传入参数key表示按照matchLength进行递增排序，item不参与排序
    return [x for _, x in sorted(suggestions, key=lambda x: x[0])]



# 16进制字符串返回二进制int型01列表
def hex_to_binarylist(hex_str):
    binary_str = bin(int(hex_str, 16))
    binary_str = binary_str[2:]
    binary_list = ' '.join(binary_str)
    renumlist = binary_list.split(' ')
    bits = list(map(int, renumlist))

    return bits


# 递归获取文件夹中的所有文件location
def get_files_Recursively(file_dir):
    result = []
    get_dir = os.listdir(file_dir)

    for i in get_dir:
        sub_dir = os.path.join(file_dir, i)
        if os.path.isdir(sub_dir):
            result = result + get_files_Recursively(sub_dir)
        else:
            result.append(sub_dir)

    return result


# 定义传参对象
class Args:
    def __init__(self, crypto_list: list, category: int, input_channel: int, col_name: list, ratio=0, epoch=30,
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


class emailSend_Object():
    def __init__(self, receivers, receiver_name='feifei'):
        # receivers = ['791844724@qq.com', '2379631316@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
        # 这里为了将用户名区分开来，我们传递的receivers列表中只有一个用户邮箱
        self.receivers = receivers
        self.receiver_name = receiver_name


    def send_file(self, information, filepath='', fileName=''):
        '''

        :param filepath: 指定发送文件的地址
        :param fileName: 指定用户端收到文件时的文件名
        :param information: 指定发送邮件的提示信息
        :return:
        '''
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header("CnPo密文分类平台", 'utf-8')
        # message['To'] = Header("feifei", 'utf-8')
        message['To'] = Header(self.receiver_name, 'utf-8')
        subject = 'Cryptographic Technology Department'
        message['Subject'] = Header(subject, 'utf-8')

        # 邮件正文内容
        message.attach(MIMEText(information, 'plain', 'utf-8'))

        # 如果用户传递了文件地址，就发送附件，否则直接发送information
        if filepath:
            # 构造附件1，传送用户模型训练下的模型文件
            att1 = MIMEText(open(filepath, 'rb').read(), 'base64', 'utf-8')
            att1["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att1["Content-Disposition"] = 'attachment; filename="{}"'.format(fileName)
            message.attach(att1)

        try:
            smtpObj = smtplib.SMTP_SSL("smtp.qq.com", 465)
            smtpObj.login('2379631316@qq.com', 'kvmntugpsnroecdj')
            smtpObj.sendmail('2379631316@qq.com', self.receivers, message.as_string())
            print("邮件发送成功")
            return True
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")
            return False


if __name__ == '__main__':

    # suggestions = FuzzyFinder(user_input='10002', collection=collection)
    # print(suggestions)
    print(getMysqlExportData('classifyrecords'))
