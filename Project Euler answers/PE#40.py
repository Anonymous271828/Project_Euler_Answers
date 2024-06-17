import numpy as np
c = 0
c2 = 0
final_answer = 1
while True:
    c = c + 1
    for i in str(c):
        c2 = c2 + 1
        #print(np.log10(c2), c2)
        if int(np.log10(c2)) == np.log10(c2):
            final_answer = final_answer * int(i)
    if c2 >= 1000000:
        break
print(final_answer)