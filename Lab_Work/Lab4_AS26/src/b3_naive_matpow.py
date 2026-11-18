"""
CSF302 Lab 4 - Part B, Question 3
Naive matrix exponentiation: A^n mod m by repeated multiplication.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python b3_naive_matpow.py
"""
from b1_matmul_mod import check_square, mat_mult_mod
from b2_identity import identity


def naive_mat_pow(A, n: int, m: int):
    """Return A^n mod m using n matrix multiplications. Time: Theta(n d^3)."""
    if n < 0:
        raise ValueError("exponent must be >= 0")
    if m < 1:
        raise ValueError("modulus must be >= 1")
    d = check_square(A)
    A = [[x % m for x in row] for row in A]
    result = [[x % m for x in row] for row in identity(d)]   # A^0 = I (mod m)
    for _ in range(n):
        result = mat_mult_mod(result, A, m)
    return result


if __name__ == "__main__":
    F = [[1, 1], [1, 0]]
    for n in range(0, 8):
        print(f"F^{n} mod 1000 = {naive_mat_pow(F, n, 1000)}")
    A = [[2, 1], [0, 3]]
    print("[[2,1],[0,3]]^5 mod 100 =", naive_mat_pow(A, 5, 100))   # [[32,211],[0,243]] mod 100

# ---------------------------------------------------------------------------
# Analysis / conclusion
# The loop does n multiplications of d x d matrices, each Theta(d^3), so the
# total is Theta(n * d^3). F^n contains Fibonacci numbers
# ([[F(n+1), F(n)], [F(n), F(n-1)]]), which the output shows, confirming the
# implementation. Linear growth in n is measured in b9_benchmark_matpow.py.
# ---------------------------------------------------------------------------
