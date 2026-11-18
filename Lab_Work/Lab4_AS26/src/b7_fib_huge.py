"""
CSF302 Lab 4 - Part B, Question 7
Calculate F(10^18) mod (10^9 + 7) without generating the preceding
Fibonacci numbers.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python b7_fib_huge.py
"""
import time

from b6_fibonacci_mod import fib_mod

N = 10**18
MOD = 10**9 + 7


def fib_fast_doubling(n: int, m: int) -> tuple[int, int]:
    """Independent checker: returns (F(n), F(n+1)) mod m using the identities
    F(2k)   = F(k) * (2F(k+1) - F(k))
    F(2k+1) = F(k)^2 + F(k+1)^2
    These follow from squaring the Fibonacci Q-matrix."""
    if n == 0:
        return 0, 1 % m
    a, b = fib_fast_doubling(n >> 1, m)
    c = a * ((2 * b - a) % m) % m
    d = (a * a + b * b) % m
    return (d, (c + d) % m) if n & 1 else (c, d)


if __name__ == "__main__":
    start = time.perf_counter()
    ans = fib_mod(N, MOD)
    elapsed = time.perf_counter() - start
    print(f"F(10^18) mod (10^9 + 7) = {ans}")
    print(f"time: {elapsed * 1000:.3f} ms, loop iterations: {N.bit_length()} (bits of n)")
    check = fib_fast_doubling(N, MOD)[0]
    print(f"fast-doubling check     = {check}  -> {'match' if check == ans else 'MISMATCH'}")

# ---------------------------------------------------------------------------
# Analysis / conclusion
# Result: F(10^18) mod (10^9 + 7) = 209783453.
# 10^18 has 60 bits, so binary exponentiation does at most ~120 2x2 matrix
# multiplications (about 1000 scalar operations) and finishes in well under
# a millisecond. Generating F(0..10^18) iteratively would need 10^18 steps:
# at ~10^7 Python steps per second that is over 3000 years. The answer was
# confirmed by a second, independent method (fast doubling).
# ---------------------------------------------------------------------------
