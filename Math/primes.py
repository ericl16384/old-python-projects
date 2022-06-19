import math

def primes(upTo):
    nums = list(range(upTo))

    for divisor in range(2, int(math.sqrt(upTo)+1)):
        for i in range(divisor, upTo, divisor-1):
            nums.pop(i)
    
    return nums

for i in primes(10):
    print(i)
