"""
matrix_mult.py
---------------
Q1: Matrix Multiplication - Traditional vs Strassen's Algorithm

This program:
  1. Multiplies matrices using the Traditional method (triple nested loop, O(n^3))
  2. Multiplies the same matrices using Strassen's Algorithm (imported from strassen.py)
  3. Verifies both methods give the same result
  4. Times both methods for increasing matrix sizes (powers of 2)
  5. Prints a comparison table
  6. Plots a graph of time vs matrix size

Run this file directly: python3 matrix_mult.py
(strassen.py must be in the same folder)
"""

import random
import time
import matplotlib.pyplot as plt
from importlib import import_module


# Load the sibling module without requiring the editor to resolve its import path.
strassen_multiply = import_module("strassen").strassen_multiply


def traditional_multiply(A, B):
    """Multiply two n x n matrices using the standard triple nested loop. O(n^3)."""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            total = 0
            for k in range(n):
                total += A[i][k] * B[k][j]
            C[i][j] = total
    return C


def generate_random_matrix(n, low=0, high=9):
    """Generate an n x n matrix filled with random integers."""
    return [[random.randint(low, high) for _ in range(n)] for _ in range(n)]


def print_matrix(M, name="Matrix"):
    print(f"{name}:")
    for row in M:
        print(row)
    print()


# ---------------------------------------------------------
# PART 1: Small demo - show the actual matrices and verify
# ---------------------------------------------------------
print("=" * 60)
print("DEMO: 4x4 matrices")
print("=" * 60)

demo_A = generate_random_matrix(4)
demo_B = generate_random_matrix(4)

print_matrix(demo_A, "Matrix A")
print_matrix(demo_B, "Matrix B")

trad_result = traditional_multiply(demo_A, demo_B)
strassen_result = strassen_multiply(demo_A, demo_B)

print_matrix(trad_result, "Traditional Result")
print_matrix(strassen_result, "Strassen Result")

print("Do both methods match?", trad_result == strassen_result)
print()


# ---------------------------------------------------------
# PART 2: Performance comparison across sizes
# ---------------------------------------------------------
print("=" * 60)
print("PERFORMANCE COMPARISON")
print("=" * 60)

sizes = [2, 4, 8, 16, 32, 64, 128]   # remove 128 if it takes too long on your machine
traditional_times = []
strassen_times = []

print(f"{'n':>5} | {'Traditional (s)':>16} | {'Strassen (s)':>13} | {'Match?':>6}")
print("-" * 50)

for n in sizes:
    A = generate_random_matrix(n)
    B = generate_random_matrix(n)

    start = time.perf_counter()
    trad = traditional_multiply(A, B)
    t_time = time.perf_counter() - start

    start = time.perf_counter()
    strass = strassen_multiply(A, B)
    s_time = time.perf_counter() - start

    match = (trad == strass)

    traditional_times.append(t_time)
    strassen_times.append(s_time)

    print(f"{n:>5} | {t_time:>16.6f} | {s_time:>13.6f} | {str(match):>6}")

# ---------------------------------------------------------
# PART 3: Plot the graph
# ---------------------------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(sizes, traditional_times, marker='o', label='Traditional O(n^3)')
plt.plot(sizes, strassen_times, marker='o', label="Strassen O(n^2.807)")
plt.xlabel('Matrix size (n)')
plt.ylabel('Time (seconds)')
plt.title('Traditional vs Strassen Matrix Multiplication')
plt.legend()
plt.grid(True)
plt.savefig('Q1.png')
print("\nGraph saved as Q1.png")

# ---------------------------------------------------------
# Analysis / Conclusion
# ---------------------------------------------------------
# For small matrices, the Traditional method is often just as fast, or
# even faster, than Strassen's Algorithm. This is because Strassen's
# algorithm carries extra overhead: recursive function calls and many
# matrix additions/subtractions performed at every level of recursion.
#
# As n grows large, Strassen's O(n^2.807) growth rate should eventually
# win over Traditional's O(n^3) growth rate. In pure Python, though,
# function-call and list-handling overhead push this crossover point
# much higher than it would be in a compiled language - in this lab's
# size range (up to 128x128), Traditional is usually still competitive
# or faster in wall-clock time, even though Strassen does asymptotically
# fewer multiplications. This is a good illustration of the difference
# between asymptotic complexity and real, measured performance.
