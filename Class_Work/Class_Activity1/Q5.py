# Fibonacci Sequence

n = int(input("Enter number of terms: "))

a = 0
b = 1

print("Fibonacci sequence:")

for i in range(n):
    print(a)
    a, b = b, a + b
