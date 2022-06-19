import random
from functools import reduce

def bitDump(stream, width):
    out = ""

    i = 0
    while i < len(stream):
        if i%width == 0 and i > 0:
            out += "\n"

        out += str(stream[i])

        i += 1
    
    return out


bits = [random.randint(0, 1) for i in range(16)]

print(bitDump(bits, 4))
print()
print(reduce(lambda x, y: x ^ y, [i for i, bit in enumerate(bits) if bit]))
