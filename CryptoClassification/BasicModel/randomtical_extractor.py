import sys

sys.path.append('/home/ubuntu/sp800_22_tests')
# sys.path.append('/home/ubuntu/sp800_22_tests')
# sys.path.append('../NISTDetect_sts/')

import getRandomnessTest


def get_random(filename):
    data_str = D2B(filename)
    binary_list = ' '.join(data_str)
    numlist = binary_list.split(' ')
    bits = list(map(int, numlist))
    ans = getRandomnessTest.GetRandomnessTest(bits)
    return ans


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
