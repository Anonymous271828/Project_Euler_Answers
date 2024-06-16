import numpy as np
def find_factors(number):
    factors = []
    for num in range(2, int(np.ceil(number**(1/2)))):
        if number % num == 0:
            factors.append(([int(x) for x in list(str(num))], [int(y) for y in list(str(int(number/num)))]))
    return factors
pandigital_numbers = []
for num in range(1000000):
    num_list = list(str(num))
    if sorted(set(num_list)) == sorted(num_list) and "0" not in num_list:
        pandigital_numbers.append(num)
print((pandigital_numbers))
correct_nums = []
for num in pandigital_numbers:
    factors = find_factors(num)
    for x, y in factors:
        unusual_list = x + y + [int(x) for x in list(str(num))]
        if sorted(unusual_list) == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            correct_nums.append(num)
print(sum(list(set(correct_nums))))
print(list(set(correct_nums)))