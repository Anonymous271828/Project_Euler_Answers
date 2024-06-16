import numpy as np
def identify_prime(number):
    if number == 2 or number == 3:
        return True, 0
    if int(number**(1/2)) == number**(1/2) or number % 2 == 0:
        return False, 0
    for num in range(3, int(np.ceil(number ** (1/2))), 2):
        if number % num == 0:
            return False, num
    else:
        return True, 0
def l_to_i(number_list):
    number = 0
    number_list = number_list[::-1]
    for i in range(len(number_list)):
        number = number + number_list[i] * 10 ** i
    return number
def find_circular(numbers, numbers2):
    for num in range(len(numbers)):
        new_number_list = [numbers[::-1][0]] + numbers[:len(numbers)-1]
        new_number = l_to_i([numbers[::-1][0]] + numbers[:len(numbers)-1])
        print(new_number)
        numbers2.append(new_number)
        numbers = new_number_list
        print(new_number)

numbers2 = []
prime_list = []
circular_numbers = []
for num in range(2, 1000000):
    if identify_prime(num)[0] == True:
        prime_list.append(num)
print(len(prime_list))
for num in prime_list:
    numbers2 = []
    for num2 in list(str(num)):
        if int(num2) % 2 == 0 or int(num2) % 5 == 0:
            break
    else:
        find_circular([int(x) for x in list(str(num))], numbers2)
        for num2 in numbers2:
            prime, value = identify_prime(num2)
            if prime == False:
                print(num2, num, value)
                break
        else:
            circular_numbers.append(num)
# add 2 since the program fails to calculate 2 and 5 because they are both divisble by themselves: they are prime.
print(len(circular_numbers))
print(circular_numbers)