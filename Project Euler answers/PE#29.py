counter_list = []
for num in range(2, 101):
    for num2 in range(2, 101):
        counter_list.append(num**num2)
print(len(list(set(counter_list))))