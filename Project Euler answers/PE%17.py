ones_digits = {0: "", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}
tens_digits = {0: "", 2: "twenty", 3: 'thirty', 4: "forty", 5: "fifty", 6: 'sixty', 7: "seventy", 8: 'eighty',
               9: "ninety"}
special_numbers = {10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
                   17: "seventeen", 18: "eighteen", 19: "nineteen", 1000: "onethousand"}
counter = 0
n2 = []
for num in range(1, 1001):
    number_list = []
    digits = [int(x) for x in list(str(num))]
    # print(digits)
    if num < 10:
        number_list.append(ones_digits[num])
    elif num < 100 or num == 1000:
        if 10 <= num <= 19 or num == 1000:
            number_list.append(special_numbers[num])
        else:
            # print(digits)
            number_list.append(tens_digits[digits[0]])
            if digits[1] != 0:
                number_list.append(ones_digits[digits[1]])
    else:
        number_list.append(ones_digits[digits[0]])
        number_list.append("hundred")
        if digits[1] > 0 or digits[2] > 0:
            number_list.append("and")
        if digits[1] == 1:
            number_list.append(special_numbers[10 + digits[2]])
        else:
            number_list.append(tens_digits[digits[1]])
            number_list.append(ones_digits[digits[2]])
    n2.append(number_list)
    # print(number_list)
    # c2= [counter][0]
    for number in number_list:
        counter = counter + len(number)
    # print(counter)

    # word = ""
    # for value in number_list:
    # word = word + value
    # counter = counter + len(word)
    # print(number_list)
print(counter)
print(n2)
