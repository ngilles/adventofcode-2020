
from utils import puzzle_input
from functools import partial
import timeit

with puzzle_input(1) as f:
    data = [int(l.strip()) for l in f.readlines()]


def find_sum_pair(data: list[int], total: int):
    '''Find the pair of elements that add to the given sum. In linear time'''

    sorted_data = list(sorted(data))
    i = 0
    j = len(sorted_data) - 1

    while True:
        if j == i:
            raise ValueError('Not found!')
        
        current_sum = sorted_data[i] + sorted_data[j]
        if  current_sum == total:
            return sorted_data[i], sorted_data[j]

        if current_sum < total:
            i += 1
        elif current_sum > total:
            j -= 1

def find_sum_triplet(data: list[int], total: int):
    '''Naive implementation of to find triplets. Sufficient for AOC sized loads.'''
    data_len = len(data)
    for i in range(data_len - 2):
        for j in range(i + 1, data_len - 1):
            for k in range(j + 1, data_len):
                current_sum  = data[i] + data[j] + data[k]
                if current_sum == total:
                    return data[i], data[j], data[k]
                if current_sum >  total:
                    break

    raise ValueError('Non found!')

def find_sum_triplet_fast(data: list[int], total: int):
    '''Modified version of find_pairs that finds triplets.

       Should be much faster than the naive version.
    '''
    data_len = len(data)
    i = 0
    m = 1
    j = len(data) - 1

    while (j - i) > 1:
        current_sum = data[i] + data[m] + data[j]
        if current_sum <= total: # start move the middle bit to look for a solution
            while (current_sum := data[i] + data[m] + data[j]) < total:
                m += 1
            if current_sum == total:
                return data[i], data[m], data[j]
            elif current_sum > total:
                i += 1
                m = i + 1
        else:
            j -= 1

    raise ValueError('Non found!')

data = list(sorted(data))
a, b = find_sum_pair(data, 2020)
print(a * b)
# a, b, c = find_sum_triplet(data, 2020)
# print(a, b, c, a * b * c)
a, b, c = find_sum_triplet_fast(data, 2020)
print(a, b, c, a * b * c)

#print(timeit.timeit(partial(find_sum_triplet, data, 2020), number=10000))
#print(timeit.timeit(partial(find_sum_triplet_fast, data, 2020), number=10000))
