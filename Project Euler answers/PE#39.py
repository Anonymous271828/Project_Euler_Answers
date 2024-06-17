p_dict = {}
for p in range(2, 1000,2):
    for a in range(1, p):
        for b in range(1, p):
            c = (a**2 + b**2)**(1/2)
            if int(c) == c and a+b+c == p:
                if p == 120:
                    print(a, b, c)
                if p in p_dict:
                    p_dict[p] = p_dict[p] + 1
                else:
                    p_dict[p] = 1
largest_val = (0, 0)
for i in list(p_dict):
    if p_dict[i] > largest_val[1]:
        largest_val = (i, p_dict[i])
print(largest_val)