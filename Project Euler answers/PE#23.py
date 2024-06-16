import numpy as np
def all_divisors(value):
    factors_list = []
    for num2 in range(2, int(np.ceil(value**(1/2))) + 1):
        if value % num2 == 0:
            factors_list.append(num2)
            factors_list.append(value/num2)
    factors_list.append(1)
    return list(set(factors_list))
abundant_numbers = []
for num in range(12, 28124):
    if sum(all_divisors(num)) > num:
        abundant_numbers.append(num)
print(len(abundant_numbers))
fail_list = []
for num1 in abundant_numbers:
    for num2 in abundant_numbers:
        if num1 + num2 < 28124:
            fail_list.append(num1 + num2)
print(sum(list(set(fail_list))))
# subtract the sum from the total sum of the list to find all successes.



