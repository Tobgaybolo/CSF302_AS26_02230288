"""
CSF302 Lab 4 - Part B, Question 2
Generate an identity matrix of a given dimension.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python b2_identity.py
"""
from b1_matmul_mod import mat_mult_mod


def identity(d: int) -> list[list[int]]:
    """Return the d x d identity matrix I (1 on the diagonal, 0 elsewhere)."""
    if d < 1:
        raise ValueError("dimension must be >= 1")
    return [[1 if i == j else 0 for j in range(d)] for i in range(d)]


if __name__ == "__main__":
    for d in (1, 2, 4):
        print(f"I_{d} =")
        for row in identity(d):
            print("   ", row)
    A = [[2, 3, 1], [4, 0, 5], [7, 6, 8]]
    I = identity(3)
    print("A x I == A:", mat_mult_mod(A, I, 10**9) == A)
    print("I x A == A:", mat_mult_mod(I, A, 10**9) == A)

# ---------------------------------------------------------------------------
# Analysis / conclusion
# Building I_d fills d^2 entries: Theta(d^2). I is the multiplicative
# identity (A x I = I x A = A), which is why it is the starting value
# (A^0 = I) for both naive and binary matrix exponentiation - the matrix
# version of starting the scalar result at 1.
# ---------------------------------------------------------------------------
