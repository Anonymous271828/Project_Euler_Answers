counter = 1
total = 1
amount = 1
amount2 = 0
while True:
    amount2 = amount2 + 1
    counter = counter + amount*2
    total = total + counter
    if amount2 % 4 == 0:
        amount = amount + 1
    if amount*2 + 1 > 1001:
        break
print(total)