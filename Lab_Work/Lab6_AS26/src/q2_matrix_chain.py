"""
CSF302 Lab 6 - Q2: Matrix Chain Multiplication

Matrix A_i has dimensions p[i-1] x p[i], i = 1..n.

  1. Minimum number of scalar multiplications by bottom-up DP   Theta(n^3)
  2. Optimal parenthesisation, e.g. ((A1(A2A3))A4)
  3. Verified by brute-force recursive search (no memo) for up to 8 matrices
  Test chains: <30,35,15,5,10,20,25> (expected 15,125), <5,4,6,2,7> and
  5 random chains (seed 42). The left-to-right cost ((A1A2)A3)... is
  reported next to the optimal cost.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q2_matrix_chain.py
"""
import random
import time

from timing_utils import markdown_table


# ---------------------------------------------------------------------------
# 1. Bottom-up DP (CLRS MATRIX-CHAIN-ORDER)
# ---------------------------------------------------------------------------
def matrix_chain_order(p):
    """Return (m, s) where m[i][j] = min cost of A_i..A_j and s[i][j] = the
    split k of an optimal (A_i..A_k)(A_{k+1}..A_j). 1-based indices."""
    n = len(p) - 1
    if n < 1:
        raise ValueError("need at least one matrix (two dimensions)")
    m = [[0] * (n + 1) for _ in range(n + 1)]
    s = [[0] * (n + 1) for _ in range(n + 1)]
    for length in range(2, n + 1):                 # chain length
        for i in range(1, n - length + 2):
            j = i + length - 1
            m[i][j] = float("inf")
            for k in range(i, j):
                cost = m[i][k] + m[k + 1][j] + p[i - 1] * p[k] * p[j]
                if cost < m[i][j]:
                    m[i][j] = cost
                    s[i][j] = k
    return m, s


# ---------------------------------------------------------------------------
# 2. Parenthesisation from the split table
# ---------------------------------------------------------------------------
def parenthesise(s, i, j):
    if i == j:
        return f"A{i}"
    k = s[i][j]
    return f"({parenthesise(s, i, k)}{parenthesise(s, k + 1, j)})"


def min_cost(p):
    """Convenience: (min cost, parenthesisation string)."""
    n = len(p) - 1
    m, s = matrix_chain_order(p)
    return m[1][n], parenthesise(s, 1, n)


def left_to_right_cost(p):
    """Cost of ((A1A2)A3)...An: the running product is p0 x p_k."""
    return sum(p[0] * p[k] * p[k + 1] for k in range(1, len(p) - 1))


def left_to_right_string(n):
    out = "A1"
    for k in range(2, n + 1):
        out = f"({out}A{k})"
    return out


def cost_of_parenthesisation(p, expr):
    """Independent check: evaluate the cost of a parenthesisation string."""
    pos = 0

    def parse():                       # returns (rows, cols, cost)
        nonlocal pos
        if expr[pos] == "(":
            pos += 1
            r1, c1, x = parse()
            r2, c2, y = parse()
            assert expr[pos] == ")" and c1 == r2
            pos += 1
            return r1, c2, x + y + r1 * c1 * c2
        pos += 1                       # 'A'
        start = pos
        while pos < len(expr) and expr[pos].isdigit():
            pos += 1
        i = int(expr[start:pos])
        return p[i - 1], p[i], 0

    return parse()[2]


# ---------------------------------------------------------------------------
# 3. Brute force: try every split recursively, no memoization
# ---------------------------------------------------------------------------
def brute_force(p, i=None, j=None):
    """Return (min cost, parenthesisation) by trying every split k of every
    sub-chain. Exponential: explores all Catalan(n-1) bracketings."""
    if i is None:
        i, j = 1, len(p) - 1
    if i == j:
        return 0, f"A{i}"
    best = (float("inf"), "")
    for k in range(i, j):
        lc, ls = brute_force(p, i, k)
        rc, rs = brute_force(p, k + 1, j)
        cost = lc + rc + p[i - 1] * p[k] * p[j]
        if cost < best[0]:
            best = (cost, f"({ls}{rs})")
    return best


def catalan(n):
    c = 1
    for i in range(n):
        c = c * 2 * (2 * i + 1) // (i + 2)
    return c


def print_table(m, n, title):
    print(title)
    print("      " + "".join(f"{j:>9}" for j in range(1, n + 1)))
    for i in range(1, n + 1):
        print(f"  i={i:<2}" + "".join(
            f"{m[i][j]:>9,}" if j >= i else f"{'':>9}" for j in range(1, n + 1)))


def main():
    chains = [("CLRS", [30, 35, 15, 5, 10, 20, 25]), ("small", [5, 4, 6, 2, 7])]
    rng = random.Random(42)
    for r in range(5):
        n = rng.randint(3, 8)                      # 3..8 matrices
        chains.append((f"random {r + 1}", [rng.randint(2, 50) for _ in range(n + 1)]))

    m, s = matrix_chain_order(chains[0][1])
    print_table(m, 6, "m table for <30,35,15,5,10,20,25> (row i, column j):")
    print()

    rows = []
    for name, p in chains:
        n = len(p) - 1
        cost, paren = min_cost(p)
        t0 = time.perf_counter()
        bf_cost, bf_paren = brute_force(p)
        t_bf = time.perf_counter() - t0
        assert cost == bf_cost, (name, cost, bf_cost)
        assert cost_of_parenthesisation(p, paren) == cost
        ltr = left_to_right_cost(p)
        assert cost_of_parenthesisation(p, left_to_right_string(n)) == ltr
        rows.append((name, n, "<" + ",".join(map(str, p)) + ">", paren, f"{cost:,}",
                     f"{bf_cost:,}", f"{ltr:,}", f"{ltr / cost:.2f}x", catalan(n - 1)))
        print(f"{name:<9} n={n}  p={p}")
        print(f"   optimal {paren} = {cost:,}   brute force = {bf_cost:,} "
              f"({catalan(n - 1)} bracketings, {t_bf * 1000:.2f} ms)")
        print(f"   left-to-right {left_to_right_string(n)} = {ltr:,}  "
              f"({ltr / cost:.2f}x the optimum)")
    assert min_cost([30, 35, 15, 5, 10, 20, 25])[0] == 15125
    table = markdown_table(["chain", "n", "dimensions", "optimal order", "DP cost",
                            "brute-force cost", "left-to-right cost", "LTR / optimal",
                            "bracketings"], rows)
    with open("../results/q2_matrix_chain.md", "w") as f:
        f.write("# Q2 - Matrix chain multiplication\n\n" + table + "\n")
    print("\nDP == brute force for every chain. Saved ../results/q2_matrix_chain.md")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Analysis / conclusion
#
# | chain    | n | optimal order                    | optimal | left-to-right | LTR/opt |
# |----------|---|----------------------------------|---------|---------------|---------|
# | CLRS     | 6 | ((A1(A2A3))((A4A5)A6))           | 15,125  | 40,500        | 2.68x   |
# | small    | 4 | ((A1(A2A3))A4)                   | 158     | 250           | 1.58x   |
# | random 1 | 8 | (A1((((((A2A3)A4)A5)A6)A7)A8))   | 7,920   | 24,435        | 3.09x   |
# | random 2 | 8 | ((A1(A2(A3(A4(A5A6)))))(A7A8))   | 13,128  | 93,590        | 7.13x   |
# | random 3 | 4 | ((A1A2)(A3A4))                   | 7,062   | 25,466        | 3.61x   |
# | random 4 | 8 | (A1(A2(A3(A4(A5(A6(A7A8)))))))   | 14,962  | 238,263       | 15.92x  |
# | random 5 | 4 | (A1(A2(A3A4)))                   | 26,818  | 60,398        | 2.25x   |
#
# - The CLRS chain gives the expected 15,125 with ((A1(A2A3))((A4A5)A6)).
# - DP cost equals the brute-force minimum for all 7 chains (up to 8
#   matrices = 429 bracketings). Each printed bracketing was also re-costed by
#   an independent evaluator, and it gives exactly the DP cost.
# - Order matters a lot: left-to-right was 1.6x to 15.9x worse. random 4
#   ends with a 19x2 matrix; multiplying from the right keeps every
#   intermediate result only 2 columns wide, while left-to-right builds
#   43-row intermediates.
# - Complexity: the DP fills n(n-1)/2 cells and tries up to n-1 splits for
#   each, so Theta(n^3) time and Theta(n^2) space. Brute force tries all
#   Catalan(n-1) = Omega(4^n / n^1.5) bracketings (429 for n = 8, already
#   ~0.5 ms vs microseconds for DP), so it is only usable as a checker for
#   short chains.
# ---------------------------------------------------------------------------
