def factorial(starting_num, counter):
    if starting_num > 1:
        return factorial(starting_num-1,counter*starting_num)
    else:
        return counter
number = list(str(factorial(100, 1)))
number = [int(x) for x in number]
print(sum(number))