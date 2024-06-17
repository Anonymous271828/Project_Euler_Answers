c = 1
def check_if_pandigital(num):
    #print(sorted(list(str(num))))
    #print(list(sorted(list(str(num)))) == ["1", "2", "3", "4", "5", "6", "7", "8", "9"])
    if sorted(str(num)) == ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        return True
    else:
        return False
largest = 0
while True:
    c = c + 1
    num = []
    for i in range(1, 7):
        num.extend(list(str(c * i)))
        if len(num) >= 9:
            break
    #print(c)
    if check_if_pandigital(int("".join(num))):
        if int("".join(num)) > largest:
            largest = int("".join(num))
            print(largest)