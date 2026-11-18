"""
CSF302 Lab 4 - Part A, Question 5
Binary modular exponentiation with input validation:
  * zero exponent      -> return 1 mod m
  * negative exponent  -> raise ValueError
  * negative base      -> reduce a mod m first (Python's % gives 0..m-1)
  * modulus m < 1      -> raise ValueError

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python a5_validated_modexp.py
"""


def mod_pow(a: int, b: int, m: int) -> int:
    """Validated a^b mod m using bitwise square-and-multiply."""
    for name, v in (("a", a), ("b", b), ("m", m)):
        if not isinstance(v, int) or isinstance(v, bool):
            raise TypeError(f"{name} must be an int, got {type(v).__name__}")
    if m < 1:
        raise ValueError(f"modulus must be >= 1, got m={m}")
    if b < 0:
        raise ValueError(f"negative exponent not supported, got b={b}")
    if b == 0:
        return 1 % m                     # a^0 = 1, and 1 mod 1 = 0
    a %= m                               # also maps a negative base into [0, m)
    result = 1
    while b:
        if b & 1:
            result = (result * a) % m
        a = (a * a) % m
        b >>= 1
    return result


if __name__ == "__main__":
    cases = [
        ("zero exponent", (7, 0, 13)),
        ("zero exponent, m=1", (7, 0, 1)),
        ("negative base", (-2, 3, 7)),     # (-8) mod 7 = 6
        ("negative base, even exp", (-3, 4, 10)),
        ("normal", (2, 10, 1000)),
        ("negative exponent", (2, -1, 7)),
        ("modulus 0", (2, 3, 0)),
        ("negative modulus", (2, 3, -5)),
        ("non-int base", (2.5, 3, 7)),
    ]
    for label, (a, b, m) in cases:
        try:
            out = mod_pow(a, b, m)
            print(f"{label:<26} mod_pow{(a, b, m)} = {out}")
        except (ValueError, TypeError) as e:
            print(f"{label:<26} mod_pow{(a, b, m)} -> {type(e).__name__}: {e}")

# ---------------------------------------------------------------------------
# Analysis / conclusion
# Validation adds only O(1) checks before the O(log b) loop, so complexity is
# unchanged. Design choices:
#  - b == 0 returns 1 % m rather than 1, so m = 1 correctly gives 0.
#  - A negative base is reduced with Python's %, which always returns a value
#    in [0, m) for m > 0, e.g. -2 % 7 = 5 and 5^3 mod 7 = 6 = (-8) mod 7.
#  - Negative exponents would need a modular inverse (which exists only when
#    gcd(a, m) = 1), so they are rejected with ValueError as the lab asks.
#  - m < 1 has no meaningful residue system and raises ValueError.
# ---------------------------------------------------------------------------
