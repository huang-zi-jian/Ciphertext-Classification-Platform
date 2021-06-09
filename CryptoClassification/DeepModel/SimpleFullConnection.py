from torch.autograd import Variable

from DeepModel.NNutil import *
from DeepModel.feature_modeling import data_preparation


class SFCNet(nn.Module):  # MLP方法
    def __init__(self, input_channel, output_channel):
        # 定义Net的初始化函数，这个函数定义了该神经网络的基本结构
        super(SFCNet, self).__init__()  # 复制并使用Net的父类的初始化方法，即先运行nn.Module的初始化函数
        self.in_to_hidden = nn.Linear(input_channel, 46)  # 定义输入层到隐含层的连结关系函数  todo 这里需要调整神经元个数
        self.hidden_to_out = nn.Linear(46, output_channel)  # 定义隐含层到输出层的连结关系函数

    def forward(self, input_data):
        # 定义该神经网络的向前传播函数，该函数必须定义，一旦定义成功，向后传播函数也会自动生成  todo  这里选择的激活函数是sigmoid
        x = torch.sigmoid(self.in_to_hidden(input_data))  # 输入input在输入层经过经过加权和与激活函数后到达隐含层
        x = torch.sigmoid(self.hidden_to_out(x))  # 类似上面
        return x


class Improve_SFCNet(nn.Module):
    """
    节点数目不能太多，超过64会下降
    损失函数Relu反而不好
    深度不能太大
    """

    def __init__(self, input_channel, output_channel):
        # 定义Net的初始化函数，这个函数定义了该神经网络的基本结构
        super(Improve_SFCNet, self).__init__()  # 复制并使用Net的父类的初始化方法，即先运行nn.Module的初始化函数
        self.in_to_h1 = nn.Linear(input_channel, 64)  # 定义输入层到隐含层的连结关系函数  todo 这里需要调整神经元个数
        self.h1_2_h2 = nn.Linear(64, 16)
        self.h2_to_out = nn.Linear(16, output_channel)  # 定义隐含层到输出层的连结关系函数

    def forward(self, input_data):
        # 定义该神经网络的向前传播函数，该函数必须定义，一旦定义成功，向后传播函数也会自动生成  todo  这里选择的激活函数是sigmoid
        x = torch.sigmoid(self.in_to_h1(input_data))  # 输入input在输入层经过经过加权和与激活函数后到达隐含层
        x = torch.sigmoid(self.h1_2_h2(x))
        x = torch.sigmoid(self.h2_to_out(x))  # 类似上面
        return x


def SFCN(crypto_list: list, feature_file_dirs: list, input_channel: int, ratio=0.8, epoch=30, batch=100,
         loss_function='MES', optimizer='SGD', mode='basic', save_mode=False):
    """
    the Classification method using a Simple Full Connection.

    :param crypto_list: the crypto_algorithm to be classified.
    :param feature_file_dirs: the files dirs for features
    :param input_channel:  feature dims
    :param ratio: the ratio to split dataset. default: 0.8
    :param epoch: epoch number. default: 30
    :param batch: number for one batch. default: 100
    :param loss_function: loss function that you choose. default: MES do not support others
    :param optimizer: optimizer that you choose. default: SGD but not recommend
    :param mode: default basic usually did
    :param save_mode: how to save the model you trained. default: False means only save parameter
    :return: result figure's name and model's name and highest accuracy
    """
    # crypto_list = concat(crypto_list)
    if mode == 'advance':
        SFC = Improve_SFCNet(input_channel, len(crypto_list))
    else:
        SFC = SFCNet(input_channel, len(crypto_list))
    train_data, train_label, test_data, test_label = data_preparation(feature_file_dirs, ratio)

    train_length = len(train_data)
    train_label = Variable(torch.from_numpy(train_label).float())  # 训练标签
    train_data = Variable(torch.from_numpy(train_data).float())  # 训练特征
    test_length = len(test_data)
    test_label = Variable(torch.from_numpy(test_label).float())  # 测试标签
    test_data = Variable(torch.from_numpy(test_data).float())  # 测试特征

    # 损失函数选择
    if loss_function == 'NLL':
        loss_fn = nn.NLLLoss()
    elif loss_function == 'CE':
        loss_fn = nn.CrossEntropyLoss()
    else:
        loss_fn = torch.nn.MSELoss()

    # 优化器选择
    if optimizer == 'Adam':
        optim = torch.optim.Adam(SFC.parameters())
    elif optimizer == 'RMSprop':
        optim = torch.optim.RMSprop(SFC.parameters(), alpha=0.9)
    elif optimizer == 'Adadelta':
        optim = torch.optim.Adadelta(SFC.parameters())
    else:
        optim = torch.optim.SGD(SFC.parameters(), lr=0.05, momentum=0.9)  # momentum小一点

    loss = []
    acc = []
    for i in range(1, epoch + 1):
        print("第" + str(i) + "轮")
        start = time.time()
        train(SFC, train_data, train_label, optim, loss_fn, train_length)
        end = time.time()
        print("消耗时间为：" + str(end - start))
        l, a, r = test(SFC, test_data, test_label, loss_fn, test_length)
        loss.append(l)
        acc.append(a)
    pic_name = plot_fig('SFC_' + mode, crypto_list, epoch, loss, acc)
    h_accuracy = max(acc)

    cl = concat2str(crypto_list)
    model_name = 'SFC_' + mode + '_' + cl
    if save_mode:
        torch.save(SFC, '/home/ubuntu/CryptoClassification/self_model/SFC_' + mode + '/' + model_name + '_model.pkl')
        model_name = model_name + '_model.pkl'
    else:
        torch.save(SFC.state_dict(), '/home/ubuntu/CryptoClassification/self_model/SFC_' + mode + '/' + model_name + '_parameter.pkl')
        model_name = model_name + '_parameter.pkl'
    return pic_name, model_name, h_accuracy

# 样例
# if __name__ == '__main__':
#     SFCN(['AES_ECB', 'DES_ECB'], 5, batch=200, optimizer='Adam', mode='advance')
# ['3DES_CBC', '3DES_ECB', 'SHA-512']
# 四分类 'DES_ECB', '3DES_ECB', 'AES_ECB', 'Blowfish_ECB'
# 简单模型（41），33.7%  （36） 35.8%  （48） 35.4%  （128） 33%  （64） 36.1%
# 复杂模型 （(32, 16)） 32.7%  （(48, 16)） 37.5%  （(64, 16)） 37.1%  （(64, 32)） 差  （(64, 9)） 36.8%
#           （(84, 16)） 35.0%

# 五分类 ['DES_ECB', '3DES_ECB', 'AES_ECB', 'Blowfish_ECB', 'RC4']
# 简单模型（18） 30.5%
# 复杂模型 （(128, 64)） 28.5%

# 'LinearComplexity', 'LongestRun', 'OverlappingTemplate', 'Runs', 'BlockFrequency'
# 分'DES_ECB', 'AES_ECB','SHA-1' 60%准确率
# 分'DES_ECB', 'SHA-1' 81.38%
