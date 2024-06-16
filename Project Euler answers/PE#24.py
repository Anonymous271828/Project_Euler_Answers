# counter = 0
# numbers_list = [x for x in range(10)]
# numbers_list2 = []
# print(numbers_list)
# for num in numbers_list:
#     for num2 in numbers_list:
#         for num3 in numbers_list:
#             for num4 in numbers_list:
#                 for num5 in numbers_list:
#                     for num6 in numbers_list:
#                         for num7 in numbers_list:
#                             for num8 in numbers_list:
#                                 for num9 in numbers_list:
#                                     for num10 in numbers_list:
#                                         counter = counter + 1
#                                         if list(set([num, num2, num3, num4, num5,num6, num7, num8, num9, num10])) == [num, num2, num3, num4, num5,num6, num7, num8, num9, num10]:
#                                             numbers_list2.append([num, num2, num3, num4, num5,num6, num7, num8, num9, num10])
#                                         print(num)
                                        #if counter == 0:
#                                             #pass
# print(numbers_list2)
# print(len(numbers_list2))
# 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
# def find_permutation(numbers, step, all_numbers):
#     numbers2 = [numbers[::-1]][0]
#     if numbers[0] == 9
#     for num in range(numbers2):
#         if numbers2[num] == 10:
#             numbers2[num] = 0
#             if num+1 < 9:
#                 numbers2[num+1] = numbers2[num+1] + 1
def find_permutation(numbers, step, numbers2):
    if step == len(numbers):
        numbers3 = [str(x) for x in numbers]
        final_num = "".join(numbers3)
        numbers2.append(int(final_num))
    else:
        for i in range(step, len(numbers)):
            numbers[i], numbers[step] = numbers[step], numbers[i]
            find_permutation(numbers,step+1, numbers2)
            numbers[i], numbers[step] = numbers[step], numbers[i]
numbers2 = []
find_permutation([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 0, numbers2)
print(sorted(numbers2)[999999])
