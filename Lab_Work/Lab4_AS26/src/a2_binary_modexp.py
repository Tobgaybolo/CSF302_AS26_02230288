"""
CSF302 Lab 4 - Part A, Question 2
Binary (square-and-multiply) modular exponentiation: a^b mod m.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python a2_binary_modexp.py
"""


def binary_mod_pow(a: int, b: int, m: int) -> int:
    """Compute a^b mod m with right-to-left square-and-multiply.

    Idea: write b in binary. a^b = product of a^(2^i) over the set bits i.
    At each step: if the current lowest bit of b is 1, multiply the result by
    the current power of a; then square the base and halve b.
    Time: O(log b) multiplications.
    """
    result = 1 % m
    base = a % m
    while b > 0:
        if b % 2 == 1:                  # lowest bit is 1 -> b is odd
            result = (result * base) % m
        base = (base * base) % m        # a^(2^i) -> a^(2^(i+1))
        b //= 2                         # drop the lowest bit
    return result


if __name__ == "__main__":
    # Trace for 3^13 mod 7 (13 = 1101 in binary)
    a, b, m = 3, 13, 7
    print(f"Trace of {a}^{b} mod {m}  (b in binary = {bin(b)[2:]})")
    result, base, e = 1, a % m, b
    step = 0
    while e > 0:
        bit = e % 2
        if bit:
            result = result * base % m
        print(f"  step {step}: bit={bit} result={result} base={base}")
        base = base * base % m
        e //= 2
        step += 1
    print(f"  final = {result}, pow() = {pow(a, b, m)}\n")

    for a, b, m in [(2, 10, 1000), (5, 0, 13), (7, 128, 13), (2, 10**18, 1_000_000_007)]:
        got = binary_mod_pow(a, b, m)
        print(f"{a}^{b} mod {m} = {got}")
        assert got == pow(a, b, m)
    print("All binary results match pow() (used only as a checker).")

# ---------------------------------------------------------------------------
# Analysis / conclusion
# The loop runs once per bit of b, i.e. floor(log2 b) + 1 times, with at most
# two modular multiplications per iteration: Theta(log b) time, O(1) space.
# That is why even b = 10^18 finishes instantly (about 60 iterations), while
# the naive method would need 10^18 multiplications. Outputs match pow().
# ---------------------------------------------------------------------------
