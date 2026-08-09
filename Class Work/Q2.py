# linear Search

arr = [10, 20, 30, 40, 50, 60]

target = int(input("Enter number to search: "))

found = False

for i in range(len(arr)):
	if arr[i] == target:
		print("Number found at position", i)
		found = True
		break

if found == False:
	print("Number not found")
