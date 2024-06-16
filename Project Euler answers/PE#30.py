c = 1
c_list = []
while True:
    c = c + 1
    num = [int(x)**5 for x in list(str(c))]
    if sum(num) == c:
        c_list.append(c)
    # 9999999 is the easiest large number to locate, where the addition of a digit after it will result in an impossibly large value.
    if c >= 9999999:
        break