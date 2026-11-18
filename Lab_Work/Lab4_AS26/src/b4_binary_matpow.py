"""
CSF302 Lab 4 - Part B, Question 4
Binary matrix exponentiation (repeated squaring): A^n mod m.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python b4_binary_matpow.py
"""
from b1_matmul_mod import check_square, mat_mult_mod
from b2_identity import identity


def binary_mat_pow(A, n: int, m: int):
    """Return A^n mod m by repeated squaring. Time: Theta(d^3 log n).

    Same square-and-multiply idea as for integers, with matrix
    multiplication instead of integer multiplication and I instead of 1.
    """
    if n < 0:
        raise ValueError("exponent must be >= 0")
    if m < 1:
        raise ValueError("modulus must be >= 1")
    d = check_square(A)
    base = [[x % m for x in row] for row in A]
    result = [[x % m for x in row] for row in identity(d)]
    while n:
        if n & 1:
            result = mat_mult_mod(result, base, m)
        n >>= 1
        if n:                                  # skip the final useless square
            base = mat_mult_mod(base, base, m)
    return result


if __name__ == "__main__":
    F = [[1, 1], [1, 0]]
    print("F^10 mod 10^9+7  =", binary_mat_pow(F, 10, 10**9 + 7))   # [[89,55],[55,34]]
    print("F^100 mod 10^9+7 =", binary_mat_pow(F, 100, 10**9 + 7))
    A = [[2, 1], [0, 3]]
    print("[[2,1],[0,3]]^5 mod 100 =", binary_mat_pow(A, 5, 100))

# ---------------------------------------------------------------------------
# Analysis / conclusion
# The loop runs floor(log2 n) + 1 times with at most two matrix products per
# iteration, so the cost is Theta(d^3 log n) instead of Theta(d^3 n). Matrix
# multiplication is associative, so A^n can be split into products of
# A^(2^i) exactly as for integers (even though it is not commutative, all
# factors are powers of the same A, so they commute with each other).
# ---------------------------------------------------------------------------
