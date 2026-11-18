"""
CSF302 Lab 4 - Part B, Question 5
Compare naive and binary matrix exponentiation for different matrices,
exponents and moduli.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python b5_compare_matpow.py
"""
import random

from b3_naive_matpow import naive_mat_pow
from b4_binary_matpow import binary_mat_pow
from timing_utils import markdown_table

FIXED = [
    ("Fibonacci Q", [[1, 1], [1, 0]], 50, 10**9 + 7),
    ("identity 3x3", [[1, 0, 0], [0, 1, 0], [0, 0, 1]], 17, 13),
    ("zero matrix", [[0, 0], [0, 0]], 5, 97),
    ("any A, n = 0", [[4, 5], [6, 7]], 0, 11),
    ("any A, n = 1", [[4, 5], [6, 7]], 1, 3),
    ("modulus 1", [[4, 5], [6, 7]], 9, 1),
    ("nilpotent", [[0, 1], [0, 0]], 2, 100),
    ("negative entries", [[-1, 2], [3, -4]], 7, 1000),
    ("1x1 = scalar", [[3]], 13, 7),
    ("Tribonacci 3x3", [[1, 1, 1], [1, 0, 0], [0, 1, 0]], 30, 10**9 + 7),
]


def run(seed: int = 42, n_random: int = 10):
    rng = random.Random(seed)
    cases = list(FIXED)
    for i in range(n_random):
        d = rng.randint(2, 5)
        A = [[rng.randint(-50, 50) for _ in range(d)] for _ in range(d)]
        cases.append((f"random {d}x{d} #{i + 1}", A, rng.randint(0, 200), rng.randint(2, 10**9)))
    rows, all_ok = [], True
    for label, A, n, m in cases:
        naive = naive_mat_pow(A, n, m)
        binary = binary_mat_pow(A, n, m)
        ok = naive == binary
        all_ok &= ok
        shown = str(binary) if len(A) <= 2 else f"{binary[0]} ..."
        rows.append((label, len(A), n, m, shown, "yes" if ok else "NO"))
    return rows, all_ok


if __name__ == "__main__":
    rows, ok = run()
    table = markdown_table(["case", "d", "n", "m", "A^n mod m (binary)", "naive == binary"], rows)
    print(table)
    print(f"\nAll {len(rows)} cases agree: {ok}")
    with open("../results/b5_comparison.md", "w") as f:
        f.write("# Part B Q5 - naive vs binary matrix exponentiation\n\n" + table + "\n")

# ---------------------------------------------------------------------------
# Analysis / conclusion
# 20 cases (10 special matrices + 10 random 2x2..5x5 with negative entries,
# seed 42) were compared. Special cases include I, the zero matrix, n = 0
# (result I), n = 1 (result A mod m), m = 1 (all zeros), a nilpotent matrix
# (A^2 = 0) and a 1x1 matrix (reduces to scalar modular exponentiation).
# Naive and binary results were identical in every case, so repeated
# squaring is a correct replacement for repeated multiplication.
# ---------------------------------------------------------------------------
