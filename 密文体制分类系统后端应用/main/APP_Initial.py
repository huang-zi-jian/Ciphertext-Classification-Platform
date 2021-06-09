'''
author: feifei
date: 2021-2-1
file info: 初始化app
'''
from flask import Flask
from sqlalchemy import PrimaryKeyConstraint
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import datetime

# 将默认的template_folder改成templates路径
app = Flask(__name__,template_folder='../templates')
'''
如果使用不同的协议，或者请求来自于其他的 IP 地址或域名或端口，就需要用到CORS，
这正是 Flask-CORS 扩展帮我们做到的。实际环境中只配置来自前端应用所在的域的请求。
'''
CORS(app)
app.secret_key = 'feifei'

class Config(object):
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:feifei@localhost/Cipher_Classify_base?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:feifei@whut@localhost/Cipher_Classify_base?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = datetime.timedelta(seconds=300)

# 用对象对app进行配置
app.config.from_object(Config)
# app.config['MAIL_SERVER'] = 'smtp.qq.com'
# app.config['MAIL_PORT'] = 465
db = SQLAlchemy(app=app, use_native_unicode='utf-8')


# 定义系统用户对象类
class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer)
    name = db.Column(db.String(16))
    password = db.Column(db.String(32))
    email = db.Column(db.String(32))
    degree = db.Column(db.String(16))
    is_delete = db.Column(db.Boolean,default=False)
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        {},
    )

    def __repr__(self):
        return 'Admin:<id:%s name:%s email:%s>' % (self.id, self.name, self.email)

# 定义密文分类记录表
class ClassifyRecord(db.Model):
    __tablename__ = 'classifyrecords'

    id = db.Column(db.Integer)
    admin = db.Column(db.String(16))
    fileName = db.Column(db.String(32))
    size = db.Column(db.String(16))
    result = db.Column(db.String(16))
    status = db.Column(db.String(16))
    confidence = db.Column(db.String(16))
    datetime = db.Column(db.String(32))
    is_delete = db.Column(db.Boolean,default=False)
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        {},
    )

    def __repr__(self):
        return 'clRecord:<id:%s admin:%s fileName:%s size:%s result:%s confidence:%s datetime:%s>' \
               % (self.id, self.admin, self.fileName, self.size, self.result, self.confidence, self.datetime)


# 定义数据集信息表
class dataSetRecord(db.Model):
    __tablename__ = 'datasetrecords'

    id = db.Column(db.Integer)
    dataSetName = db.Column(db.String(32))
    source = db.Column(db.String(128))
    introduction = db.Column(db.String(256))
    filetype = db.Column(db.String(8))
    size = db.Column(db.String(8))
    sizeAfterCipher = db.Column(db.String(8))
    is_delete = db.Column(db.Boolean,default=False)
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        {},
    )

    def __repr__(self):
        return 'dataSetRecord:<id:%s dataSetName:%s source:%s introduction:%s>' \
               % (self.id, self.dataSetName, self.source, self.introduction)



# 定义模型训练记录信息表
class modelTrainRecord(db.Model):
    __tablename__ = 'modelTrainrecords'

    id = db.Column(db.Integer)
    algorithm = db.Column(db.String(8))
    category = db.Column(db.String(8))
    size = db.Column(db.String(8))
    txtFileNum = db.Column(db.String(8))
    accuracy = db.Column(db.String(8))
    is_delete = db.Column(db.Boolean,default=False)
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        {},
    )

    def __repr__(self):
        return 'dataSetRecord:<id:%s algorithm:%s category:%s size:%s txtFileNum:%s accuracy:%s>' \
               % (self.id, self.algorithm, self.category, self.size, self.txtFileNum, self.accuracy)