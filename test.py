mylist = [1, 2, 3, 4, 5, 6, 7, 8]
otherlist = [9, 10, 11]
x = len(otherlist)
y = len(mylist)-x

del mylist[y:]

print(mylist)  # Output: [4, 5, 6, 7, 8]