"""
CSF302 Lab 4 - Part A, Question 1
Naive modular exponentiation: a^b mod m by repeated multiplication.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python a1_naive_modexp.py
"""


def naive_mod_pow(a: int, b: int, m: int) -> int:
    """Compute a^b mod m by multiplying `a` into the result b times.

    The result is reduced mod m after every multiplication, so intermediate
    values never grow beyond m^2. Time: O(b) multiplications.
    """
    result = 1 % m          # handles m == 1 (everything is 0 mod 1)
    a %= m                  # keep the base small
    for _ in range(b):
        result = (result * a) % m
    return result


if __name__ == "__main__":
    examples = [(2, 10, 1000), (3, 13, 7), (5, 0, 13), (7, 128, 13), (123456, 789, 1_000_000_007)]
    print(f"{'a':>8} {'b':>5} {'m':>12} {'naive':>12} {'pow()':>12}")
    for a, b, m in examples:
        got = naive_mod_pow(a, b, m)
        print(f"{a:>8} {b:>5} {m:>12} {got:>12} {pow(a, b, m):>12}")
        assert got == pow(a, b, m)
    print("All naive results match Python's built-in pow (used only as a checker).")

# ---------------------------------------------------------------------------
# Analysis / conclusion
# The loop runs exactly b times, so the algorithm performs b modular
# multiplications: Theta(b) time and O(1) extra space. Reducing after every
# step keeps each number below m, so the cost of a single multiplication stays
# constant for word-sized m. All example outputs match pow(a, b, m). The linear
# growth is confirmed by the timings in a6_timing.py.
# ---------------------------------------------------------------------------
