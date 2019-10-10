from math import sin, cos, radians
import timeit

def bench():
    product = 1.0
    for counter in range(1, 1000, 1):
        for dex in list(range(1, 360, 1)):
            angle = radians(dex)
            product *= sin(angle)**2 + cos(angle)**2
    return product

if __name__ == '__main__':
    result = timeit.repeat(stmt = bench, setup='from math import sin, cos, radians', number=10, repeat=10)
    result = list(sorted(result))
    final_result = ((3 - result[:1][0]) * 1/1.8) * 100
    print(final_result)