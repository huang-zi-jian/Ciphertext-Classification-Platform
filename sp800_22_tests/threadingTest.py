'''
author: feifei
date: 2021-3-10
file info: 多线程测试是否节省时间
'''

from getRandomnessTest import GetRandomnessTest, doneFunction
import threading
import os
import math



# 定义线程类
class myThread(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = self.func(self.args)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None



def getAllResult(ThreadNum, floder_dir):

    suggestions = []

    ls = os.listdir(floder_dir)
    avarageTask = math.ceil(len(ls)/ThreadNum)

    # threads = []
    threads = []
    location = 0
    while location < len(ls):
        # tempThread = myThread(doneFunction, ls[location: location + avarageTask])
        # threads.append(tempThread)
        temp_myThread = myThread(doneFunction, ls[location: location + avarageTask])
        threads.append(temp_myThread)

        location = location + avarageTask

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
        suggestions = suggestions + thread.get_result()

    return suggestions



if __name__ == '__main__':
    # 读取AES-262.txt文件中的字符串然后转成int型的01列表
    # with open(file='AES-262.txt', mode='r', encoding='utf-8') as f:
    ls = os.listdir('test')
    threads = []
    for filename in ls:
        file_dir = 'test/' + filename
        with open(file=file_dir, mode='r', encoding='utf-8') as f:
            hex_str = f.read()

        binary_str = bin(int(hex_str, 16))
        binary_str = binary_str[2:]
        binary_list = ' '.join(binary_str)
        numlist = binary_list.split(' ')
        bits = list(map(int, numlist))

        print(len(bits))
        # 应用默认参数获取二进制bit的随机性检测指标
        # todo: 这边测试Linear_block对时间的影响很大
        temp_thread = threading.Thread(target=GetRandomnessTest, args=(bits,))
        temp_thread.start()
        threads.append(temp_thread)

        # todo: 加入更多线程但是没法改善时间消耗？单线程集合每个任务一个线程总共花费时间相差不大？
        # result = GetRandomnessTest(bits=bits, Linear_len=500, Linear_N_block=30)
        # print(result)

    for thread in threads:
        thread.join()
