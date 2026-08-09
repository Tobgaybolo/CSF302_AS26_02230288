# Binary Search

arr = [10, 20, 30, 40, 50, 60]

target = int(input("Enter a number to search: "))

low = 0
high = len(arr) - 1
found = False

while low <= high:
    mid = (low + high) // 2

    if arr[mid] == target:
        print("Number found at position", mid)
        found = True
        break
    elif target < arr[mid]:
        high = mid - 1
    else:
        low = mid + 1

if found == False:
    print("Number not found")
