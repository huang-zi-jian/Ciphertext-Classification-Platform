'''
author: feifei
date: 2021-3-4
file info: 随机性测试脚本
'''

if __name__ == '__main__':
    numlist = ' '.join('1100100100001111110110101010001000100001011010001100001000110100110001001100011001100010100010111000')
    renumlist = numlist.split(' ')
    bits = list(map(int, renumlist))

    # todo: Frequency
    '''
    # p >= 0.01时success为true，_变量返回None
    success, p, _ = monobit_test(bits)
    '''

    # todo: BlockFrequency
    '''
    # p >= 0.01时success为true，_变量返回None；
    # 注意，success返回False并且p返回1.0时表示bits小于100，数据量太短而不能参与检测
    # block_size可以指定检测的分块大小，默认为20
    success, p, _ = frequency_within_block_test(bits, block_size=64)
    '''


    '''
    # p >= 0.01时success为true，_变量返回None；
    success, p, _ = approximate_entropy_test(bits, M=10)
    '''

    # todo: Rank
    '''
    # p >= 0.01时success为true，_变量返回None；
    # 注意，success返回False并且p返回0.0时表示block块小于38，块少于最低标准而不能参与检测
    success, p, _ = binary_matrix_rank_test(bits, M=32, Q=32)
    # M, Q指定二元矩阵的行和列，默认均为32
    '''

    # todo: CumulativeSums
    '''
    # plist中每个p值都大于0.01时success为true，_变量返回None；
    # plist中包含两个p值，一个是forward，一个是reverse
    success, _, plist = cumulative_sums_test(bits)
    '''

    # todo: FFT
    '''
    # p >= 0.01时success为true，_变量返回None；
    success, p, _ = dft_test(bits)
    '''

    # todo: LinearComplexity
    '''
    # p >= 0.01时success为true，_变量返回None；
    # 注意，success返回False并且p返回0.0时表示bits小于10^6而不能参与检测
    # 可以选择patternlen参数，这样就不会有最小bits位数限制（patternlen=500无法通国可以尝试300）
    success, p, _ = linear_complexity_test(bits, patternlen=500)
    '''

    # todo: LongestRun
    '''
    # p >= 0.01时success为true，_变量返回None；
    # 注意，success返回False并且p返回1.0时表示bits小于128而不能参与检测
    success, p, _ = longest_run_ones_in_a_block_test(bits)
    '''

    # todo: Universal
    '''
    # p >= 0.01时success为true，_变量返回None；
    success, p, _ = maurers_universal_test(bits)
    '''

    '''
    # p >= 0.01时success为true，_变量返回None；
    success, p, _ = non_overlapping_template_matching_test(bits)
    '''

    # todo: OverlappingTemplate
    '''
    # p >= 0.01时success为true，_变量返回None；
    # 注意，success返回False并且p返回0.0时表示bits小于1,028,016而不能参与检测
    # 可以选择blen参数指定可重复块样本大小，默认为10
    success, p, _ = overlapping_template_matching_test(bits, blen=9)
    '''

    '''
    # plist包含8个特定状态的p-value
    success, _, plist = random_excursion_test(bits)
    '''

    '''
    # plist包含18个特定状态的p-value
    success, _, plist = random_excursion_variant_test(bits)
    '''

    # todo: Runs
    '''
    # p >= 0.01时success为true，_变量返回None；
    # 注意，success返回False并且p返回0.0时表示序列完全不满足游程测试
    success, p, _ = runs_test(bits)
    '''

    '''
    # plist包含2个p-value，类似于Cumulative Sums Test
    # 注意，success返回False并且p返回0时表示bits数据量不够
    # 可以指定patternlen参数来设置可重复序列块的大小，这样可以消除数据量限制，默认为None，
    success, _, plist = serial_test(bits, patternlen=16)
    '''


