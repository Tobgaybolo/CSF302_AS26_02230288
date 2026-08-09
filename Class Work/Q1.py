import random

n = int(input("Enter how many numbers you want: "))

numbers = []

for i in range(n):
	value = random.randint(1, 100)
	numbers.append(value)

print("Random numbers are:", numbers)

smallest = numbers[0]
largest = numbers[0]

for num in numbers:
	if num < smallest:
		smallest = num
	if num > largest:
		largest = num

print("Smallest number is:", smallest)
print("Largest number is:", largest)

