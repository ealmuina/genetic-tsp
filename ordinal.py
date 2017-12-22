import bisect
import random


def cross(c1, c2, p):
    if random.random() > p:
        return c1, c2
    e1 = encode(c1)
    e2 = encode(c2)
    pos = random.randrange(0, len(e1))
    return decode(e1[:pos] + e2[pos:]), decode(e2[:pos] + e1[pos:])


def decode(e):
    canonic = list(range(len(e)))
    result = []
    for i in e:
        result.append(canonic[i])
        canonic.pop(i)
    return result


def encode(c):
    canonic = list(range(len(c)))
    result = []
    for x in c:
        i = bisect.bisect_left(canonic, x)
        result.append(i)
        canonic.pop(i)
    return result
