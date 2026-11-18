n = int(input("Enter number of elements: "))

arr = []

for i in range(n):
	num = int(input("Enter element: "))
	arr.append(num)

largest = arr[0]
second_largest = arr[0]

for num in arr:
	if num > largest:
		second_largest = largest
		largest = num
	elif num > second_largest and num != largest:
		second_largest = num

print("Array:", arr)
print("Second largest element is:", second_largest)
