# -*- coding: UTF-8 -*-
'''
author: feifei
date: 2021-3-23
file info: 实现一些后端功能接口
'''

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import os


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


def getFileInformation(filePath):
    size = 0
    txtFileNum = 0
    for root, dirs, files in os.walk(filePath):
        for f in files:
            size += os.path.getsize(os.path.join(root, f))
            txtFileNum = txtFileNum + 1
    return str(round(size/1000000, 1)), str(txtFileNum)


if __name__ == '__main__':
    emailSendObject = emailSend_Object(receivers=['2379631316@qq.com'], receiver_name='feifei')
    emailSendObject.send_file(information='CnPo密文分类平台 邮件发送测试…… 分类完成')


