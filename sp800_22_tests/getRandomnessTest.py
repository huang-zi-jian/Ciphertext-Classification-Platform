# -*- coding:UTF-8 -*-

'''
author: feifei
date: 2021-3-7
file info: 获取随机性测试p-value特征值
'''
import os

from NIST_Detect.sp800_22_approximate_entropy_test import approximate_entropy_test
from NIST_Detect.sp800_22_binary_matrix_rank_test import binary_matrix_rank_test
from NIST_Detect.sp800_22_cumulative_sums_test import cumulative_sums_test
from NIST_Detect.sp800_22_dft_test import dft_test
from NIST_Detect.sp800_22_frequency_within_block_test import frequency_within_block_test
from NIST_Detect.sp800_22_linear_complexity_test import linear_complexity_test
from NIST_Detect.sp800_22_longest_run_ones_in_a_block_test import longest_run_ones_in_a_block_test
from NIST_Detect.sp800_22_maurers_universal_test import maurers_universal_test
from NIST_Detect.sp800_22_monobit_test import monobit_test
from NIST_Detect.sp800_22_non_overlapping_template_matching_test import non_overlapping_template_matching_test
from NIST_Detect.sp800_22_overlapping_template_matching_test import overlapping_template_matching_test
from NIST_Detect.sp800_22_random_excursion_test import random_excursion_test
from NIST_Detect.sp800_22_random_excursion_variant_test import random_excursion_variant_test
from NIST_Detect.sp800_22_runs_test import runs_test
from NIST_Detect.sp800_22_serial_test import serial_test
import random


def GetRandomnessTest(bits, Frequence_block = 128, Over_block = 9, Linear_len = 500, Linear_N_block = 30, Rank_list = (32, 32)):
    '''

    :param bits: int型0/1列表，如[1, 0, 0, 1, 1, 1, 0...]
    :param Frequence_block: Frequence检测块大小，默认为128
    :param Over_block: OverlappingTemplate检测块大小，默认为9
    :param Linear_block: LinearComplexity检测块大小，默认为500
    :param Rank_list: binary_matrix_rank中秩检验中矩阵的行和列大小，默认均为32
    :return: 如果返回结果result中对应随机性指标的p值不是数字而是False，
            说明可能因为数据量过少的原因而无法通过对应测试
    '''
    result_list = []
    result_dict = {}

    # 获取块内频数检验的随机性指标
    success, p, _ = frequency_within_block_test(bits, block_size=Frequence_block)
    if success==False and p==1.0:
        p = False
    result_list.append(p)
    result_dict['BlockFrequency'] = p
    print('1-finish')

    # 获取累加和检验的随机性指标
    success, _, plist = cumulative_sums_test(bits)
    result_list = result_list + plist
    result_dict['CumulativeSums1'] = plist[0]
    result_dict['CumulativeSums2'] = plist[1]
    print('2-finish')

    # 获取离散傅里叶变换检验的随机性指标
    success, p, _ = dft_test(bits)
    result_list.append(p)
    result_dict['FFT'] = p
    print('3-finish')

    # 获取频率检验的随机性指标
    success, p, _ = monobit_test(bits)
    result_list.append(p)
    result_dict['Frequency'] = p
    print('4-finish')

    # 获取线性复杂度检验的随机性指标
    success, p, _ = linear_complexity_test(bits, patternlen=Linear_len, N_block=Linear_N_block)
    if success==False and p==0.0:
        p = False
    result_list.append(p)
    result_dict['LinearComplexity'] = p
    print('5-finish')

    # 获取块内最长游程检验的随机性指标
    success, p, _ = longest_run_ones_in_a_block_test(bits)
    if success==False and p==1.0:
        p = False
    result_list.append(p)
    result_dict['LongestRun'] = p
    print('6-finish')

    # 获取重叠模块匹配检验的随机性指标
    success, p, _ = overlapping_template_matching_test(bits, blen=Over_block)
    if success==False and p==0.0:
        p = False
    result_list.append(p)
    result_dict['OverlappingTemplate'] = p
    print('7-finish')

    # 获取二元矩阵秩检验的随机性指标
    success, p, _ = binary_matrix_rank_test(bits, M=Rank_list[0], Q=Rank_list[1])
    if success==False and p==0.0:
        p = False
    result_list.append(p)
    result_dict['Rank'] = p
    print('8-finish')

    # 获取游程检验的随机性指标
    success, p, _ = runs_test(bits)
    if success==False and p==0.0:
        p = False
    result_list.append(p)
    result_dict['Runs'] = p
    print('9-finish')

    # 获取Maurer通用统计检验的随机性指标（检验序列能否在没有信息损耗的条件下被大大的压缩）
    success, p, _ = maurers_universal_test(bits)
    result_list.append(p)
    result_dict['Universal'] = p
    print('10-finish')

    return result_list, result_dict



# 传入文件名列表，获取文件名列表对应的随机性检测结果列表
def doneFunction(ls):

    suggestions = []
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
        result_list, result_dict = GetRandomnessTest(bits=bits, Linear_len=500, Linear_N_block=30)
        print(result_list)

        suggestions.append(result_list)

    return suggestions




if __name__ == '__main__':
    # numlist = ' '.join('11001001000011111101101010100010001000010110100011000010001101')
    # renumlist = numlist.split(' ')
    # bits = list(map(int, renumlist))

    '''
    # 读取test.txt文件中的01字符串然后转成int型的01列表
    with open(file='test.txt', mode='r', encoding='utf-8') as f:
        binary_str = f.read()
        binary_list = ' '.join(binary_str)
        numlist = binary_list.split(' ')
        bits = list(map(int, numlist))
    '''

    '''
    bits = []
    random.seed(0)
    for i in range(1, 507265):
        digit = random.choice([0, 1])
        bits.append(digit)
    '''


    # 读取AES-262.txt文件中的字符串然后转成int型的01列表
    # with open(file='AES-262.txt', mode='r', encoding='utf-8') as f:
    ls = os.listdir('test')
    processings = []
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
        # temp_thread = threading.Thread(target=GetRandomnessTest, args=(bits,))
        # temp_thread.start()
        temp_processing = multiprocessing.Process(target=GetRandomnessTest, args=(bits,))
        processings.append(temp_processing)
        temp_processing.start()


        # todo: 加入更多线程但是没法改善时间消耗？单线程集合每个任务一个线程总共花费时间相差不大？
        # result = GetRandomnessTest(bits=bits, Linear_len=500, Linear_N_block=30)
        # print(result)

    for processing in processings:
        processing.join()


    # 开始线程
    '''
    suggestions = getAllResult(ThreadNum=10, floder_dir='test')
    print(suggestions)
    '''

    '''
    # 开始进程
    suggestions = getAllResult(ThreadNum=60, floder_dir='test')
    print(suggestions)
    '''
