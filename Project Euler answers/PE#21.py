import numpy as np
def all_divisors(value):
    factors_list = []
    for num2 in range(2, int(np.ceil(num**(1/2))) + 1):
        if value % num2 == 0:
            factors_list.append(num2)
            factors_list.append(value/num2)
    factors_list.append(1)
    return list(set(factors_list))
pm_not = []
for num in range(3,10000):
    for num2 in range(2, int(np.ceil(num**(1/2))) + 1):
        if num % num2 == 0:
            pm_not.append(num)
            break
numbers = []
for num in pm_not:
    total = sum(all_divisors(num))
    #if num == 220:
        #print(total)
    if total in pm_not and sum(all_divisors(total)) == num and total != num:
        print(num, total)
        numbers.append(num)
        numbers.append(total)
#print(pm_not)
print(sum(list(set(numbers))))