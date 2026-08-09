# Frequency Count

n = int(input("Enter number of elements: "))

arr = []

for i in range(n):
    num = int(input("Enter element: "))
    arr.append(num)

freq = {}

for num in arr:
    if num in freq:
        freq[num] += 1
    else:
        freq[num] = 1

print("Frequency count:")

for num in freq:
    print(num, "appears", freq[num], "time(s)")
