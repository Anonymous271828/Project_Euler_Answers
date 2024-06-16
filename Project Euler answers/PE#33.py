def add_nums(num):
    num = num[::-1]
    number = 0
    for x, y in enumerate(num):
        number = number + y * 10 ** x
    return number

print(list((set([1, 2, 3, 4, 5]).intersection([1, 6, 7, 8, 9]))))
possible_numbers = []
for num in range(10, 101):
    for num2 in range(10, 101):
        if num == num2:
            continue
        num_list = [int(x) for x in list(str(num))]
        num2_list = [int(x) for x in list(str(num2))]
        similar_num = list(set(num_list).intersection(num2_list))
        if len(similar_num) != 0 and num_list.index(similar_num[0]) != num2_list.index(similar_num[0]):
            newl = [num_list][0]
            newl.pop(newl.index(similar_num[0]))
            newl2 = [num2_list][0]
            newl2.pop(newl2.index(similar_num[0]))
            #print(newl, newl2, similar_num, num, num2)
            if newl2[0] != 0:
                if num/num2 == add_nums(newl) / add_nums(newl2) and num/num2 < 1:
                    possible_numbers.append((num, num2))
print(possible_numbers)
