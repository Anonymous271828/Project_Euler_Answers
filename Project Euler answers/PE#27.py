import numpy as np
def check_if_prime(number):
    #if number % 2 == 0:
        #return False
    if number < 0:
        return False
    for num in range(2, int(np.ceil(number ** (1/2)))):
        if number % num == 0:
            return False
    else:
        return True
def identify_all_primes(equation):
    counter = 0
    while True:
        final_number = counter ** 2 + equation[0]*counter + equation[1]
        if check_if_prime(final_number) == False:
            return counter, equation
        counter = counter + 1

highest_depth = 0
location = []
for a in range(-1000, 1000):
    for b in range(-1000, 1001):
        amount, equation = identify_all_primes([a, b])
        if amount > highest_depth:
            location = equation
            highest_depth = amount
print(location, highest_depth)