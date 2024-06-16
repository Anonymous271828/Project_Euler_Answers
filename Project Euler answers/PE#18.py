number_list = "75 95 64 17 47 82 18 35 87 10 20 04 82 47 65 19 01 23 75 03 34 88 02 77 73 07 63 67 99 65 04 28 06 16 70 92 41 41 26 56 83 40 80 70 33 41 48 72 33 47 32 37 16 94 29 53 71 44 65 25 43 91 52 97 51 14 70 11 33 28 77 73 17 78 39 68 17 57 91 71 52 38 17 14 91 43 58 50 27 29 48 63 66 04 68 89 53 67 30 73 16 69 87 40 31 04 62 98 27 23 09 70 98 73 93 38 53 60 04 23".split(" ")
number_list2 = []
number_list = [int(x) for x in number_list]
split_counter = 0
previous_number = 0
for num in range(len(number_list)):
    if num - previous_number == split_counter:
        number_list2.append(number_list[previous_number:num+1])
        split_counter = split_counter + 1
        previous_number = num+1
print(number_list2)
largest_sum = 0
for a in number_list2[0]:
    for b in number_list2[1][number_list2[0].index(a):number_list2[0].index(a) + 2]:
        for c in number_list2[2][number_list2[1].index(b):number_list2[1].index(b) + 2]:
            for d in number_list2[3][number_list2[2].index(c):number_list2[2].index(c) + 2]:
                for e in number_list2[4][number_list2[3].index(d):number_list2[3].index(d) + 2]:
                    for f in number_list2[5][number_list2[4].index(e):number_list2[4].index(e) + 2]:
                        for g in number_list2[6][number_list2[5].index(f):number_list2[5].index(f) + 2]:
                            for h in number_list2[7][number_list2[6].index(g):number_list2[6].index(g) + 2]:
                                for i in number_list2[8][number_list2[7].index(h):number_list2[7].index(h) + 2]:
                                    for j in number_list2[9][number_list2[8].index(i):number_list2[8].index(i) + 2]:
                                        for k in number_list2[10][number_list2[9].index(j):number_list2[9].index(j) + 2]:
                                            for l in number_list2[11][number_list2[10].index(k):number_list2[10].index(k) + 2]:
                                                for m in number_list2[12][number_list2[11].index(l):number_list2[11].index(l) + 2]:
                                                    for n in number_list2[13][number_list2[12].index(m):number_list2[12].index(m) + 2]:
                                                        for o in number_list2[14][number_list2[13].index(n):number_list2[13].index(n) + 2]:
                                                            if sum([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]) > largest_sum:
                                                                largest_sum = sum([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o])
print(largest_sum)
