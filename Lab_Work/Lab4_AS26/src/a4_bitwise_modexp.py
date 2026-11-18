"""
CSF302 Lab 4 - Part A, Question 4
Binary modular exponentiation using bitwise operations:
  b & 1   tests whether b is odd (lowest bit set)
  b >>= 1 halves b (shifts off the lowest bit)

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python a4_bitwise_modexp.py
"""
import random

from a2_binary_modexp import binary_mod_pow


def bitwise_mod_pow(a: int, b: int, m: int) -> int:
    """Square-and-multiply using b & 1 and b >>= 1. Time: O(log b)."""
    result = 1 % m
    base = a % m
    while b:
        if b & 1:                       # odd exponent
            result = (result * base) % m
        base = (base * base) % m
        b >>= 1                         # halve the exponent
    return result


if __name__ == "__main__":
    rng = random.Random(42)
    checked = 0
    for _ in range(1000):
        a, b, m = rng.randint(0, 10**12), rng.randint(0, 10**12), rng.randint(1, 10**9)
        assert bitwise_mod_pow(a, b, m) == binary_mod_pow(a, b, m) == pow(a, b, m)
        checked += 1
    print(f"bitwise == arithmetic binary == pow() on {checked} random cases (seed 42)")
    print("Examples:")
    for a, b, m in [(2, 10, 1000), (3, 13, 7), (2, 10**18, 1_000_000_007)]:
        print(f"  {a}^{b} mod {m} = {bitwise_mod_pow(a, b, m)}")
    # b & 1 vs b % 2, b >> 1 vs b // 2 for a sample
    for b in [13, 12, 1, 0]:
        print(f"  b={b:>2} ({b:04b}): b&1={b & 1} b%2={b % 2}  b>>1={b >> 1} b//2={b // 2}")

# ---------------------------------------------------------------------------
# Analysis / conclusion
# For non-negative integers, b & 1 == b % 2 and b >> 1 == b // 2, so this
# version computes exactly the same values as Q2 (verified on 1000 random
# cases). The number of loop iterations is still floor(log2 b) + 1, so the
# complexity is unchanged at Theta(log b). Bitwise operations make the
# "look at the binary digits of b" idea explicit; in CPython the speed
# difference from % and // is small because interpreter overhead dominates.
# ---------------------------------------------------------------------------
