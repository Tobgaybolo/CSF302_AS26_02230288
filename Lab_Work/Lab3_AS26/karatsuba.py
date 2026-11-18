"""
karatsuba.py
-------------
Q2: Karatsuba's Algorithm for Large Integer Multiplication

This program:
  1. Multiplies large integers using the Traditional grade-school method (O(n^2))
  2. Multiplies the same integers using Karatsuba's Algorithm (O(n^1.585))
  3. Verifies both methods give the same result
  4. Times both methods for increasing digit sizes
  5. Prints a comparison table
  6. Plots a graph of time vs number of digits

Both methods work on the digit-string representation of the numbers so
they don't just fall back on Python's own (already fast) big-integer
multiplication - the point is to actually implement the algorithms.

Run this file directly: python3 karatsuba.py
"""

import random
import time
import matplotlib.pyplot as plt


def traditional_multiply(x, y):
    """
    Grade-school ("long") multiplication done digit by digit. O(n^2).
    x and y are non-negative integers.
    """
    x_str, y_str = str(x), str(y)
    n, m = len(x_str), len(y_str)
    result = [0] * (n + m)

    # multiply each digit of x with each digit of y, just like on paper
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            mul = int(x_str[i]) * int(y_str[j])
            p1, p2 = i + j, i + j + 1        # p2 is the "ones" position, p1 is the "carry" position
            total = mul + result[p2]
            result[p2] = total % 10
            result[p1] += total // 10

    result_str = ''.join(map(str, result)).lstrip('0')
    return int(result_str) if result_str else 0


def karatsuba(x, y):
    """
    Multiply two non-negative integers using Karatsuba's Algorithm.
    Divide and conquer: 3 recursive multiplications per split instead of 4.
    """
    # Base case: numbers small enough to multiply directly
    if x < 10 or y < 10:
        return x * y

    # number of digits in the larger of the two numbers
    n = max(len(str(x)), len(str(y)))
    half = n // 2

    # split x into (a, b) and y into (c, d) such that
    #   x = a * 10^half + b
    #   y = c * 10^half + d
    power = 10 ** half
    a, b = divmod(x, power)
    c, d = divmod(y, power)

    # 3 recursive multiplications (this is the trick that saves one
    # multiplication compared to the naive divide-and-conquer approach)
    ac = karatsuba(a, c)
    bd = karatsuba(b, d)
    ad_plus_bc = karatsuba(a + b, c + d) - ac - bd

    return ac * (10 ** (2 * half)) + ad_plus_bc * power + bd


def random_n_digit_number(n_digits):
    """Generate a random non-negative integer with exactly n_digits digits."""
    if n_digits == 1:
        return random.randint(0, 9)
    first = random.randint(1, 9)
    rest = ''.join(str(random.randint(0, 9)) for _ in range(n_digits - 1))
    return int(str(first) + rest)


# ---------------------------------------------------------
# PART 1: Small demo
# ---------------------------------------------------------
print("=" * 60)
print("DEMO")
print("=" * 60)

x = random_n_digit_number(6)
y = random_n_digit_number(6)

trad = traditional_multiply(x, y)
kara = karatsuba(x, y)

print(f"x = {x}")
print(f"y = {y}")
print(f"Traditional result: {trad}")
print(f"Karatsuba result:   {kara}")
print("Do both methods match?", trad == kara)
print()

# ---------------------------------------------------------
# PART 2: Performance comparison across digit sizes
# ---------------------------------------------------------
print("=" * 60)
print("PERFORMANCE COMPARISON")
print("=" * 60)

digit_sizes = [8, 16, 32, 64, 128, 256, 512, 1024]
traditional_times = []
karatsuba_times = []

print(f"{'digits':>7} | {'Traditional (s)':>16} | {'Karatsuba (s)':>14} | {'Match?':>6}")
print("-" * 55)

for d in digit_sizes:
    x = random_n_digit_number(d)
    y = random_n_digit_number(d)

    start = time.perf_counter()
    trad = traditional_multiply(x, y)
    t_time = time.perf_counter() - start

    start = time.perf_counter()
    kara = karatsuba(x, y)
    k_time = time.perf_counter() - start

    match = (trad == kara)
    traditional_times.append(t_time)
    karatsuba_times.append(k_time)

    print(f"{d:>7} | {t_time:>16.6f} | {k_time:>14.6f} | {str(match):>6}")

# ---------------------------------------------------------
# PART 3: Plot the graph
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(digit_sizes, traditional_times, marker='o', label='Traditional O(n^2)')
plt.plot(digit_sizes, karatsuba_times, marker='o', label='Karatsuba O(n^1.585)')
plt.xlabel('Number of digits (n)')
plt.ylabel('Time (seconds)')
plt.title('Traditional vs Karatsuba Big Integer Multiplication')
plt.legend()
plt.grid(True)
plt.savefig('Q3.png')
print("\nGraph saved as Q3.png")

# ---------------------------------------------------------
# Analysis / Conclusion
# ---------------------------------------------------------
# For small numbers, the Traditional method is competitive - sometimes
# even faster - because Karatsuba's recursion carries overhead: splitting
# numbers, extra additions, and many nested function calls.
#
# As the number of digits grows, Traditional's O(n^2) cost grows much
# faster than Karatsuba's O(n^1.585) cost, so Karatsuba pulls further
# ahead for large numbers. This matches the recurrence relations:
#   Traditional: T(n) = 4*T(n/2) + O(n)   -> O(n^2)
#   Karatsuba:   T(n) = 3*T(n/2) + O(n)   -> O(n^log2(3)) ~= O(n^1.585)
# The saving comes entirely from cutting 4 recursive multiplications
# down to 3, since multiplication is the expensive operation and
# addition is comparatively cheap (O(n)).
