# -*- coding:UTF-8 -*-

# sp800_22_frequency_within_block_test.pylon


from __future__ import print_function

import math
from fractions import Fraction
#from scipy.special import gamma, gammainc, gammaincc
from gamma_functions import *

#ones_table = [bin(i)[2:].count('1') for i in range(256)]
def count_ones_zeroes(bits):
    ones = 0
    zeroes = 0
    for bit in bits:
        if (bit == 1):
            ones += 1
        else:
            zeroes += 1
    return (zeroes,ones)

def frequency_within_block_test(bits, block_size=128):
    '''

    :param bits:
    :param block_size: block_size默认为20
    :return:
    '''
    # Compute number of blocks M = block size. N=num of blocks
    # N = floor(n/M)
    # miniumum block size 20 bits, most blocks 100
    n = len(bits)
    # 自己增加的block_size参数
    M = block_size
    N = int(math.floor(n/M))
    if N > 99:
        N=99
        M = int(math.floor(n/N))
    
    if len(bits) < 100:
        print("Too little data for test. Supply at least 100 bits")
        return False,1.0,None
    
    print("  n = %d" % len(bits))
    print("  N = %d" % N)
    print("  M = %d" % M)
    
    num_of_blocks = N
    block_size = M #int(math.floor(len(bits)/num_of_blocks))
    #n = int(block_size * num_of_blocks)
    
    proportions = list()
    for i in range(num_of_blocks):
        block = bits[i*(block_size):((i+1)*(block_size))]
        zeroes,ones = count_ones_zeroes(block)
        proportions.append(Fraction(ones,block_size))

    chisq = 0.0
    for prop in proportions:
        chisq += 4.0*block_size*((prop - Fraction(1,2))**2)
    
    p = gammaincc((num_of_blocks/2.0),float(chisq)/2.0)
    success = (p >= 0.01)
    return (success,p,None)


