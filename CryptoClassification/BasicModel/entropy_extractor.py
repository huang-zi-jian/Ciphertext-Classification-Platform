import numpy as np
import re
import math
from scipy import integrate


# 十六进制转二进制
def D2B(file_name):
    with open(file_name, 'r') as f:
        str = f.readlines()
    lent = 0
    s = ""
    for line in str:
        rlt = bin(int(line, 16))[2:]
        lent = lent + len(rlt)
        s += rlt
    return s


def get_entropy(name):
    data = D2B(name)
    en_56 = F_56b(data)
    en_128 = F_128b(data)
    en_256 = F_256b(data)
    en_1024 = F_1024b(data)
    en_56c = F_56cut_7(data)
    en_128c = F_128cut_16(data)
    en_256c = F_256cut_32(data)
    return [en_56, en_128, en_256, en_1024, en_56c, en_128c, en_256c]


def twoD56_36(bin_data):
    sum = 0
    num = dict()
    for i in range(0, 37):
        num[str(i)] = 0
    data_arr = Cut_text(bin_data, 56)
    # j是数组中x的值，i是数组中y的值
    for i in range(0, 56 - 6):
        ans = 0
        for j in range(0, len(data_arr) - 6):
            ans = n_squre_1(6, 6, data_arr, j, i)
            sum += 1
            key = str(ans)
            num[key] = num[key] + 1
    count = []
    for i in range(0, 37):
        count.append(num[str(i)])
    num_p = []
    for i in range(0, 37):
        num_p.append(count[i] / sum)
    return Pearson_chi_squre(count, 6, 6, sum)


def twoD56_16(bin_data):
    sum = 0
    num = dict()
    for i in range(0, 17):
        num[str(i)] = 0
    data_arr = Cut_text(bin_data, 56)
    # j是数组中x的值，i是数组中y的值
    for i in range(0, 56 - 4):
        ans = 0
        for j in range(0, len(data_arr) - 4):
            ans = n_squre_1(4, 4, data_arr, j, i)
            sum += 1
            key = str(ans)
            num[key] = num[key] + 1
    count = []
    for i in range(0, 17):
        count.append(num[str(i)])
    num_p = []
    for i in range(0, 17):
        num_p.append(count[i] / sum)
    return Pearson_chi_squre(count, 4, 4, sum)


# 求排列组合C(m,n)
def C(m, n):
    a = b = result = 1
    if m < n:
        print("n不能小于m 且均为整数")
    elif (type(m) != int) or (type(n) != int):
        print("n不能小于m 且均为整数")
    else:
        minNI = min(n, m - n)  # 使运算最简便
        for j in range(0, minNI):
            # 使用变量a,b 让所用的分母相乘后除以所有的分子
            a = a * (m - j)
            b = b * (minNI - j)
            result = a // b  # 在此使用“/”和“//”均可，因为a除以b为整数
        return result


def Pearson_chi_squre(count, x, y, sum):
    p = []
    pearson = 0
    for i in range(0, x * y + 1):
        p.append((C(x * y, i) / 2 ** 36))
    for i in range(0, x * y + 1):
        pearson += (count[i] - sum * p[i]) ** 2 / p[i]
    pearson = pearson ** 0.5 / 1000
    sum = sum ** 0.5 / 1000

    # pearson = decimal.Decimal(pearson)
    # sum = decimal.Decimal(sum)
    # E = decimal.Decimal(math.e)
    def p_value(x):
        return x ** (sum - 1) / math.e ** pearson

    ans = integrate.quad(p_value, 0, pearson)
    return ans[0] * 10


def n_squre_1(w, l, data, x, y):
    ans = 0
    for i in range(x, x + w):
        for j in range(y, y + l):
            if data[i][j] == '1':
                ans += 1

    return ans


# 分组比特熵
def F_56b(bin_data):
    entropy = []
    data_arr = Cut_text(bin_data, 56)
    for pos in range(0, 56):
        per_zero, per_one = Z0num_bit(data_arr, pos)
        if per_zero != 0 and per_one != 0 and per_zero != 1 and per_one != 1:
            en_56b = Caculate_entropy_bit(per_one, per_zero)
        else:
            en_56b = 0
        entropy.append(en_56b)
    return entropy


def F_128b(bin_data):
    entropy = []
    data_arr = Cut_text(bin_data, 128)
    for pos in range(0, 128):
        per_zero, per_one = Z0num_bit(data_arr, pos)
        en_128b = Caculate_entropy_bit(per_one, per_zero)
        entropy.append(en_128b)
    return entropy


def F_256b(bin_data):
    entropy = []
    data_arr = Cut_text(bin_data, 256)
    for pos in range(0, 256):
        per_zero, per_one = Z0num_bit(data_arr, pos)
        en_256b = Caculate_entropy_bit(per_one, per_zero)
        entropy.append(en_256b)
    return entropy


def F_1024b(bin_data):
    entropy = []
    data_arr = Cut_text(bin_data, 1024)
    for pos in range(0, 1024):
        per_zero, per_one = Z0num_bit(data_arr, pos)
        en_1024b = Caculate_entropy_bit(per_one, per_zero)
        entropy.append(en_1024b)
        print(entropy)
    return entropy


# 分组字节熵
def F_56cut_7(bin_data):
    # 记录熵值
    entropy = []
    # 先将密文按56bit分块
    data_arr = Cut_text(bin_data, 56)
    # 二维矩阵，n行，7列（n由文件大小确定）元素为（十进制数串，出现次数）二元组
    info = np.zeros((data_arr.__len__(), 7), dtype=int)
    for pos in range(0, data_arr.__len__()):
        # 再将每个块分成七个字节
        per_data = Cut_text(data_arr[pos], 8)
        # byte_dict = {}
        for p in range(0, 7):
            # 将二进制字节转化成十进制字符串作为键值
            dec_data = int(Bin2Dec(per_data[p]))
            info[pos][p] = dec_data
    # 矩阵旋转(顺时针旋转90度）
    info90 = np.rot90(info, -1)
    for elem in info90:
        entropy.append(calc_ent(elem))
    # with open('res_F_56cut7.txt', 'a')as f:
    #     f.write('DES_CBC_2的F_56cut7为：' + str(entropy) + '\n')
    return entropy


def F_128cut_16(bin_data):
    # 记录熵值
    entropy = []
    # 先将密文按56bit分块
    data_arr = Cut_text(bin_data, 128)
    # 二维矩阵，n行，7列（n由文件大小确定）元素为（十进制数串，出现次数）二元组
    info = np.zeros((data_arr.__len__(), 16), dtype=int)
    for pos in range(0, data_arr.__len__()):
        # 再将每个块分成16个字节
        per_data = Cut_text(data_arr[pos], 8)
        # byte_dict = {}
        for p in range(0, 16):
            # 将二进制字节转化成十进制字符串作为键值
            dec_data = int(Bin2Dec(per_data[p]))
            info[pos][p] = dec_data
    # 矩阵旋转(顺时针旋转90度）
    info90 = np.rot90(info, -1)
    for elem in info90:
        entropy.append(calc_ent(elem))

    #     for j in range(0, data_arr.__len__()):
    #         print(list.count(info, info[i][j]))

    return entropy


def F_256cut_32(bin_data):
    # 记录熵值
    entropy = []
    # 先将密文按56bit分块
    data_arr = Cut_text(bin_data, 256)
    # 二维矩阵，n行，7列（n由文件大小确定）元素为（十进制数串，出现次数）二元组
    info = np.zeros((data_arr.__len__(), 32), dtype=int)
    for pos in range(0, data_arr.__len__()):
        # 再将每个块分成16个字节
        per_data = Cut_text(data_arr[pos], 8)
        # byte_dict = {}
        for p in range(0, 32):
            # 将二进制字节转化成十进制字符串作为键值
            dec_data = int(Bin2Dec(per_data[p]))
            info[pos][p] = dec_data
    # 矩阵旋转(顺时针旋转90度）
    info90 = np.rot90(info, -1)
    for elem in info90:
        entropy.append(calc_ent(elem))

    #     for j in range(0, data_arr.__len__()):
    #         print(list.count(info, info[i][j]))

    return entropy


# 工具函数
# 二进制转十进制
def Bin2Dec(per_bdate):
    return int(per_bdate, 2)


# 计算列表的熵
def calc_ent(x):
    x_value_list = set([x[i] for i in range(x.shape[0])])
    ent = 0.0
    for x_value in x_value_list:
        p = float(x[x == x_value].shape[0]) / x.shape[0]
        log_p = np.log2(p)
        ent -= p * log_p

    return ent


# 计算指定比特位0和1的个数
def Z0num_bit(data_arr, pos):
    zero_num = 0
    one_num = 0
    for data_elem in data_arr:
        if data_elem[pos] == '0':
            zero_num += 1
        else:
            one_num += 1
    print(zero_num)
    print(one_num)
    if one_num != 0:
        per_one = float(one_num) / float(zero_num + one_num)
        per_zero = 1 - per_one
    else:
        per_one = 0
        per_zero = 1 - per_one
    return per_zero, per_one


# 计算熵值
def Caculate_entropy_bit(*c):
    en = 0
    for x in c:
        en += (-x) * math.log(x, 2)
    return en


# 将字符串按照指定长度分割
def Cut_text(text, len):
    text_arr = re.findall('.{' + str(len) + '}', text)
    return text_arr

# if __name__ == '__main__':
#     data = []
#     twod = []
#     # 读取二进制数据
# for i in range(0, 1800):
#     with open('3DES_ECB_cut/bincut' + str(i) + '.txt', 'r') as f:
#         data = f.read()
#         # print(len(data))
#     # print(data)
#     ans = twoD56_36(data)
#     print('*********************{}********************\n\n'.format(i))
#     print(ans)
#     twod.append(ans)
# with open('2d13DES_ECB.csv', 'w', newline="") as file:
#     writer = csv.writer(file)
#     # for i in range(0, len(twod)):
#     #     writer.writerow([twod[i]])
#     # writer.writerow(["序号", "F_56b", "F_128b", "F_256b", "F_1024b", "F_cut_7", "F_128cut_16", "F_256cut_32"])
#     en_56 = F_56b(data)
#     en_128 = F_128b(data)
#     en_256 = F_256b(data)
#     en_1024 = F_1024b(data)
#     en_56c = F_56cut_7(data)
#     en_128c = F_128cut_16(data)
#     en_256c = F_256cut_32(data)
#     # writer.writerow([i, en_56, en_128, en_256, en_56c, en_128c, en_256c])
#     writer.writerow([i, en_56, en_128, en_256, en_1024, en_56c, en_128c, en_256c])
