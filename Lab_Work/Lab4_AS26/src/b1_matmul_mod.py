"""
CSF302 Lab 4 - Part B, Question 1
Multiply two square matrices, reducing each element modulo m.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python b1_matmul_mod.py
"""

Matrix = list[list[int]]


def check_square(A: Matrix, name: str = "A") -> int:
    """Return the dimension of A, raising ValueError if A is not square."""
    d = len(A)
    if d == 0 or any(len(row) != d for row in A):
        raise ValueError(f"{name} must be a non-empty square matrix")
    return d


def mat_mult_mod(A: Matrix, B: Matrix, m: int) -> Matrix:
    """Return (A x B) mod m for d x d matrices A and B.

    C[i][j] = (sum_k A[i][k] * B[k][j]) mod m.
    The sum of d products is reduced once per element (Python ints cannot
    overflow, so one reduction per entry is enough and is faster than
    reducing after every addition). Time: Theta(d^3).
    """
    if m < 1:
        raise ValueError("modulus must be >= 1")
    d = check_square(A, "A")
    if check_square(B, "B") != d:
        raise ValueError("A and B must have the same dimension")
    C = [[0] * d for _ in range(d)]
    for i in range(d):
        Ai = A[i]
        Ci = C[i]
        for j in range(d):
            s = 0
            for k in range(d):
                s += Ai[k] * B[k][j]
            Ci[j] = s % m
    return C


if __name__ == "__main__":
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    print("A =", A, " B =", B)
    print("A x B          =", mat_mult_mod(A, B, 10**9))      # [[19,22],[43,50]]
    print("A x B mod 10   =", mat_mult_mod(A, B, 10))         # [[9,2],[3,0]]
    F = [[1, 1], [1, 0]]
    print("F x F mod 1000 =", mat_mult_mod(F, F, 1000))       # [[2,1],[1,1]]
    try:
        mat_mult_mod([[1, 2]], [[1]], 7)
    except ValueError as e:
        print("non-square input ->", e)

# ---------------------------------------------------------------------------
# Analysis / conclusion
# Three nested loops over d give d^3 scalar multiplications: Theta(d^3) time
# and Theta(d^2) space for the result. Reducing each entry mod m keeps all
# stored values below m, so later multiplications work on small numbers.
# The 2x2 examples match hand calculation ([[19,22],[43,50]]).
# ---------------------------------------------------------------------------
