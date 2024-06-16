import numpy as np
highest_depth = 0
value = []
for num in range(2,1000):
    remainder_list = [1]
    #print(num)
    while True:
        if remainder_list[::-1][0] == 0:
            break
        remainder = (remainder_list[::-1][0] * 10) % num
        if remainder in remainder_list:
            if len(remainder_list) > highest_depth:
                highest_depth = len(remainder_list)
                value = remainder_list
            break
        remainder_list.append(remainder)
        #print(remainder_list, num)
print(highest_depth, value)
#rint(1/983 * 10000000000)











#     print(num)
#     num = 1/num
#     if int(num) != num:
#         number_list = list(str(num))
#         number_list = number_list[number_list.index(".")+1:]
#         number_list2 = []
#         for num2 in number_list:
#             if num2
#         #number_list = len(set(number_list))
#         print(set(number_list), num)
#         number_list = len(set(number_list))
#         if highest_depth < number_list:
#             highest_depth = number_list
# print(highest_depth)