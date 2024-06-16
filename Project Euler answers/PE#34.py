def factorial(num, counter):
    if num <= 1:
        return counter
    counter = counter * num
    return factorial(num-1,counter)
# 1.0E+8 is the largest number that could be created; 9999999 is larger than 9! * 7. Divided by 10 to increase speed.
for num in range(1000000):
    counter2 = 0
    for num2 in [int(x) for x in list(str(num))]:
        counter2 = counter2 + factorial(num2, 1)
    if counter2 == num:
        print(num)