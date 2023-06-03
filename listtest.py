test = [1,2]

i = 0
for number in test:
    i += 1
    test.append(int(test[-1] + test[-2]))
    if i == 20:
        break
print(test)