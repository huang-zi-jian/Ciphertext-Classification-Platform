# -*- coding:UTF-8 -*-

# sp800_22_overlapping_template_mathcing_test.py

from __future__ import print_function

import math
#from scipy.special import gamma, gammainc, gammaincc
from gamma_functions import *

def lgamma(x):
    return math.log(gamma(x))
    
def Pr(u, eta):
    if ( u == 0 ):
        p = math.exp(-eta)
    else:
        sum = 0.0
        for l in range(1,u+1):
            sum += math.exp(-eta-u*math.log(2)+l*math.log(eta)-lgamma(l+1)+lgamma(u)-lgamma(l)-lgamma(u-l+1))
        p = sum
    return p

def overlapping_template_matching_test(bits,blen=10):
    n = len(bits)

    m = blen
    # Build the template B as a random list of bits
    B = [1 for x in range(m)]

    K = 5
    M = 1032 # todo(change): M = 1062 改为 M = 1032

    if len(bits) < M:
        print("Insufficient data. %d bit provided. 1032 bits required" % len(bits))
        return False, 0.0, None
    N = int(n/M)
    
    blocks = list() # Split into N blocks of M bits
    for i in range(N):
        blocks.append(bits[i*M:(i+1)*M])

    # Count the distribution of matches of the template across blocks: Vj
    v=[0 for x in range(K+1)] 
    for block in blocks:
        count = 0
        for position in range(M-m):
            if block[position:position+m] == B:
                count += 1
            
        if count >= (K):
            v[K] += 1
        else:
            v[count] += 1

    #lamd = float(M-m+1)/float(2**m) # Compute lambda and nu
    #nu = lamd/2.0

    chisq = 0.0  # Compute Chi-Square
    #pi = [0.324652,0.182617,0.142670,0.106645,0.077147,0.166269] # From spec
    pi = [0.364091, 0.185659, 0.139381, 0.100571, 0.0704323, 0.139865] # From STS
    piqty = [int(x*N) for x in pi]
    
    lambd = (M-m+1.0)/(2.0**m)
    eta = lambd/2.0
    sum = 0.0
    for i in range(K): #  Compute Probabilities
        pi[i] = Pr(i, eta)
        sum += pi[i]

    pi[K] = 1 - sum;

    #for block in blocks:
    #    count = 0
    #    for j in xrange(M-m+1):
    #        if B == block[j:j+m]:
    #            count += 1
    #    if ( count <= 4 ):
    #        v[count]+= 1
    #    else:
    #        v[K]+=1

    sum = 0    
    chisq = 0.0
    for i in range(K+1):
        chisq += ((v[i] - (N*pi[i]))**2)/(N*pi[i])
        sum += v[i]
        
    p = gammaincc(5.0/2.0, chisq/2.0) # Compute P value

    print("  B = ",B)
    print("  m = ",m)
    print("  M = ",M)
    print("  N = ",N)
    print("  K = ",K)
    print("  model = ",piqty)
    print("  v[j] =  ",v) 
    print("  chisq = ",chisq)
    
    success = ( p >= 0.01)
    return (success,p,None)
