all_perms = []
def permutations(num_list, start_index):
    if start_index == len(num_list):
        all_perms.append(int("".join(num_list)))
    else:
        for i in range(start_index, len(num_list)):
            num_list[start_index], num_list[i] = num_list[i], num_list[start_index]
            permutations(num_list, start_index+1)
            num_list[start_index], num_list[i] = num_list[i], num_list[start_index]
def check_prime(num):
    for i in range(2, int(num**(1/2)) + 1):
        if num % i == 0:
            return False
    else:
        return True
num = 1234567
permutations(list(str(num)), 0)
largest_prime = 0
for i in all_perms:
    if check_prime(i) and i > largest_prime:
        largest_prime = i
print(largest_prime)