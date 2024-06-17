def is_prime(num):
    if num == 1:
        return False
    for i in range(2, int(num**(1/2)) + 1):
        if num % i == 0:
            return False
    #print(num)
    return True
c = 10
acceptable = []
print("A")
while True:
    c = c + 1
    c_digits = [i for i in str(c)]
    #print(c_digits)
    if is_prime(c):
        for i in range(1, len(c_digits)):
            #print(int("".join(c_digits[:i])), c)
            if is_prime(int("".join(c_digits[:i]))) == False:
                break
        else:
            for i in range(1, len(c_digits)):
                #print(int("".join(c_digits[:])), c)
                if is_prime(int("".join(c_digits[i:]))) == False:
                    break
            else:
                acceptable.append(c)
    if len(acceptable) == 11:
        print(sum(acceptable), acceptable)
        break
    #print(acceptable)