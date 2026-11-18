"""
CSF302 Lab 4 - Part A, Question 3
Compare the outputs of naive and binary modular exponentiation for different
bases, exponents and moduli (fixed cases plus random cases with a fixed seed).

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python a3_compare_modexp.py
"""
import random

from a1_naive_modexp import naive_mod_pow
from a2_binary_modexp import binary_mod_pow
from timing_utils import markdown_table

FIXED_CASES = [
    (2, 10, 1000),
    (3, 13, 7),
    (0, 5, 11),          # zero base
    (5, 0, 13),          # zero exponent
    (10, 3, 1),          # modulus 1 -> always 0
    (7, 1, 13),          # exponent 1
    (12, 6, 12),         # base == modulus
    (99, 99, 97),        # base > modulus
    (2, 1000, 1_000_000_007),
    (123456789, 5000, 998_244_353),
]


def run_comparison(seed: int = 42, n_random: int = 15):
    rng = random.Random(seed)
    cases = list(FIXED_CASES)
    for _ in range(n_random):
        cases.append((rng.randint(0, 10**9), rng.randint(0, 3000), rng.randint(1, 10**9)))

    rows, all_ok = [], True
    for a, b, m in cases:
        n = naive_mod_pow(a, b, m)
        bi = binary_mod_pow(a, b, m)
        ok = n == bi == pow(a, b, m)
        all_ok &= ok
        rows.append((a, b, m, n, bi, "yes" if ok else "NO"))
    return rows, all_ok


if __name__ == "__main__":
    rows, all_ok = run_comparison()
    table = markdown_table(["a", "b", "m", "naive", "binary", "match"], rows)
    print(table)
    print(f"\nAll {len(rows)} cases agree: {all_ok}")
    with open("../results/a3_comparison.md", "w") as f:
        f.write("# Part A Q3 - naive vs binary modular exponentiation\n\n" + table + "\n")

# ---------------------------------------------------------------------------
# Analysis / conclusion
# 25 cases (10 hand-picked edge cases + 15 random, seed 42) were tested,
# covering zero base, zero exponent, m = 1, base >= m and large primes such as
# 10^9+7 and 998244353. The naive and binary methods produced identical
# results in every case, and both matched Python's pow(a, b, m), which was
# used only as an independent checker. The two algorithms compute the same
# function; they differ only in how many multiplications they perform.
# ---------------------------------------------------------------------------
