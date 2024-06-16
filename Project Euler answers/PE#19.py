dotw = 3
counter = 0
for year in range(1,101):
    for month in range(1, 13):
        if month == 4 or month == 6 or month == 9 or month == 11:
            dotw = dotw + 30%7
        elif month == 2:
            if year%4 == 0:
                dotw = dotw + 29%7
        else:
            dotw = dotw + 31%7
        if dotw > 7:
            dotw = dotw - 7
        if dotw == 1:
            counter = counter + 1
print(counter)