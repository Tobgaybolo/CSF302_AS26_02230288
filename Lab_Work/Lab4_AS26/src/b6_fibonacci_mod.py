"""
CSF302 Lab 4 - Part B, Question 6
nth Fibonacci number modulo m using matrix exponentiation.

  [[1, 1],   ^ n     [[F(n+1), F(n)  ],
   [1, 0]]        =   [F(n),   F(n-1)]]       with F(0) = 0, F(1) = 1.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python b6_fibonacci_mod.py
"""
from b4_binary_matpow import binary_mat_pow

Q = [[1, 1], [1, 0]]


def fib_mod(n: int, m: int) -> int:
    """Return F(n) mod m in Theta(log n) 2x2 matrix multiplications."""
    if n < 0:
        raise ValueError("n must be >= 0")
    if m < 1:
        raise ValueError("modulus must be >= 1")
    return binary_mat_pow(Q, n, m)[0][1]


def fib_mod_iterative(n: int, m: int) -> int:
    """Brute-force check: generate F(0..n) one by one. Theta(n)."""
    a, b = 0, 1 % m
    for _ in range(n):
        a, b = b, (a + b) % m
    return a % m


if __name__ == "__main__":
    print("First 15 Fibonacci numbers (m = 10^9):",
          [fib_mod(n, 10**9) for n in range(15)])
    for m in (10, 1000, 10**9 + 7):
        for n in range(0, 2001, 7):
            assert fib_mod(n, m) == fib_mod_iterative(n, m)
    print("Matrix method matches iterative method for n = 0..2000, m in {10, 1000, 10^9+7}")
    for n, m in [(10, 1000), (90, 10**19), (1000, 10**9 + 7), (10**6, 10**9 + 7)]:
        print(f"F({n}) mod {m} = {fib_mod(n, m)}")
    print("Pisano period check, m = 10: F(60) mod 10 =", fib_mod(60, 10),
          "F(61) mod 10 =", fib_mod(61, 10))

# ---------------------------------------------------------------------------
# Analysis / conclusion
# fib_mod uses binary matrix exponentiation on a fixed 2x2 matrix, so the
# cost is Theta(log n) (d = 2 is constant). It was verified against the
# simple Theta(n) iterative recurrence for 286 values of n and three moduli.
# F(90) < 10^19, so F(90) mod 10^19 = F(90) = 2880067194370816120 exactly.
# The Pisano period for m = 10 is 60, confirmed by F(60) = 0 and F(61) = 1
# (mod 10).
# ---------------------------------------------------------------------------
