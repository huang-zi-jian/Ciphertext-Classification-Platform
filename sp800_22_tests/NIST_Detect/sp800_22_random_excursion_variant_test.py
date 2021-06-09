# sp800_22_random_excursion_variant_test.py


from __future__ import print_function

import math

def random_excursion_variant_test(bits):
    n = len(bits)

    x = list()             # Convert to +1,-1
    for bit in bits:
        x.append((bit * 2)-1)

    # Build the partial sums
    pos = 0
    s = list()
    for e in x:
        pos = pos+e
        s.append(pos)    
    sprime = [0]+s+[0] # Add 0 on each end

    # Count the number of cycles J
    J = 0
    for value in sprime[1:]:
        if value == 0:
            J += 1
    print("J=",J)
    # Build the counts of offsets
    count = [0 for x in range(-9,10)]
    for value in sprime:
        if (abs(value) < 10):
            count[value] += 1

    # Compute P values
    success = True
    plist = list()
    for x in range(-9,10):
        if x != 0:
            top = abs(count[x]-J)
            bottom = math.sqrt(2.0 * J *((4.0*abs(x))-2.0))
            p = math.erfc(top/bottom)
            plist.append(p)
            if p < 0.01:
                err = " Not Random"
                success = False
            else:
                err = ""
            print("x = %1.0f\t count=%d\tp = %f %s"  % (x,count[x],p,err))
            
    if (J < 500):
        print("J too small (J=%d < 500) for result to be reliable" % J)
    elif success:
        print("PASS")
    else:    
        print("FAIL: Data not random")
    return (success,None,plist)

