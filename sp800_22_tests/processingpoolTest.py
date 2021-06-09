'''
author: feifei
date: 2021-3-10
file info: 进程池测试时间
'''

from multiprocessing import Pool
import time
from getRandomnessTest import GetRandomnessTest
import os


# 文件读取转化bits也同样采用多进程实现节省时间
def readFiletoBits(filename):
    file_dir = 'test/' + filename
    with open(file=file_dir, mode='r', encoding='utf-8') as f:
        hex_str = f.read()

    binary_str = bin(int(hex_str, 16))
    binary_str = binary_str[2:]
    binary_list = ' '.join(binary_str)
    numlist = binary_list.split(' ')
    bits = list(map(int, numlist))

    return bits



if __name__ == '__main__':
    ls = os.listdir('test')

    s = time.time()

    pool_readfile = Pool(10)
    bits_list_1 = pool_readfile.map(readFiletoBits, ls)
    pool_readfile.close()
    pool_readfile.join()

    e1 = time.time()
    print('进程执行时间', int(e1 - s))

    s = time.time()

    bits_list_2 = []
    for filename in ls:
        file_dir = 'test/' + filename
        with open(file=file_dir, mode='r', encoding='utf-8') as f:
            hex_str = f.read()

        binary_str = bin(int(hex_str, 16))
        binary_str = binary_str[2:]
        binary_list = ' '.join(binary_str)
        numlist = binary_list.split(' ')
        bits = list(map(int, numlist))

        bits_list_2.append(bits)
    e1 = time.time()
    print('顺序执行时间', int(e1 - s))

    # print(bits_list_1)
    # print(bits_list_2)

    '''
    suggestions_1 = []
    s = time.time()

    for bits in bits_list:
        result_list, result_dict = GetRandomnessTest(bits)
        suggestions_1.append(result_list)

    e1 = time.time()
    print('顺序执行时间：', int(e1 - s))
    time.sleep(5)


    suggestions_2 = []
    s = time.time()
    pool = Pool(10)
    suggestions_list = pool.map(GetRandomnessTest, bits_list)
    pool.close()
    pool.join()
    for suggestions in suggestions_list:
        suggestions_2.append(suggestions[0])

    e1 = time.time()
    print('多进程执行时间：', int(e1 - s))
    time.sleep(5)

    print(suggestions_1)
    print(suggestions_2)
    '''