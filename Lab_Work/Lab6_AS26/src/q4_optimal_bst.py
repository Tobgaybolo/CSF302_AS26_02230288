"""
CSF302 Lab 6 - Q4 (optional): Optimal Binary Search Tree

Keys k1..k5 with p = 0.15, 0.10, 0.05, 0.10, 0.20 (successful searches) and
dummy keys d0..d5 with q = 0.05, 0.10, 0.05, 0.05, 0.05, 0.10 (unsuccessful).
Compute the minimum expected search cost (expected 2.75) and print the tree.

DP (CLRS OPTIMAL-BST), for 1 <= i <= n+1, i-1 <= j <= n:
  e[i][i-1] = q[i-1]                                    (empty: only d_{i-1})
  w[i][j]   = w[i][j-1] + p[j] + q[j]                    (total probability)
  e[i][j]   = min_{i<=r<=j} ( e[i][r-1] + e[r+1][j] ) + w[i][j]
Making a subtree one level deeper adds its total probability w[i][j] to the
cost, which is why w is added. Theta(n^3) time, Theta(n^2) space.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q4_optimal_bst.py
"""

P = [None, 0.15, 0.10, 0.05, 0.10, 0.20]          # p[1..n]  (p[0] unused)
Q = [0.05, 0.10, 0.05, 0.05, 0.05, 0.10]          # q[0..n]


def optimal_bst(p, q, n):
    """Return (e, w, root) tables, all indexed [1..n+1][0..n]."""
    e = [[0.0] * (n + 1) for _ in range(n + 2)]
    w = [[0.0] * (n + 1) for _ in range(n + 2)]
    root = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 2):
        e[i][i - 1] = q[i - 1]
        w[i][i - 1] = q[i - 1]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            e[i][j] = float("inf")
            w[i][j] = w[i][j - 1] + p[j] + q[j]
            for r in range(i, j + 1):
                t = e[i][r - 1] + e[r + 1][j] + w[i][j]
                if t < e[i][j] - 1e-12:           # strict improvement (float-safe)
                    e[i][j] = t
                    root[i][j] = r
    return e, w, root


def describe(root, i, j, parent=None, side=None, lines=None):
    """CLRS CONSTRUCT-OPTIMAL-BST: one sentence per node."""
    if lines is None:
        lines = []
    if j < i:                                        # dummy key d_j
        lines.append(f"d{j} is the {side} child of k{parent}")
        return lines
    r = root[i][j]
    lines.append(f"k{r} is the root" if parent is None else f"k{r} is the {side} child of k{parent}")
    describe(root, i, r - 1, r, "left", lines)
    describe(root, r + 1, j, r, "right", lines)
    return lines


def draw(root, i, j, prefix="", is_last=True, label="root"):
    """Sideways tree drawing (right subtree printed below left)."""
    connector = "" if label == "root" else ("└── " if is_last else "├── ")
    if j < i:
        print(f"{prefix}{connector}{label}: d{j}")
        return
    r = root[i][j]
    print(f"{prefix}{connector}{'' if label == 'root' else label + ': '}k{r}")
    child_prefix = prefix + ("" if label == "root" else ("    " if is_last else "│   "))
    draw(root, i, r - 1, child_prefix, False, "L")
    draw(root, r + 1, j, child_prefix, True, "R")


def expected_cost_of_tree(root_choice, i, j, depth, p, q):
    """Independent check: sum of (depth + 1) * probability over all nodes."""
    if j < i:
        return (depth + 1) * q[j]
    r = root_choice(i, j)
    return ((depth + 1) * p[r] + expected_cost_of_tree(root_choice, i, r - 1, depth + 1, p, q)
            + expected_cost_of_tree(root_choice, r + 1, j, depth + 1, p, q))


def brute_force_min_cost(p, q, i, j, depth=0):
    """Try every possible root at every level (exponential). Returns the cost
    contribution of the subtree on keys i..j placed at the given depth."""
    if j < i:
        return (depth + 1) * q[j]
    return min((depth + 1) * p[r] + brute_force_min_cost(p, q, i, r - 1, depth + 1)
               + brute_force_min_cost(p, q, r + 1, j, depth + 1) for r in range(i, j + 1))


def main():
    n = 5
    e, w, root = optimal_bst(P, Q, n)
    print("e table (expected cost of subtree on keys i..j):")
    print("        " + "".join(f"{'j=' + str(j):>8}" for j in range(0, n + 1)))
    for i in range(1, n + 2):
        print(f"  i={i}   " + "".join(f"{e[i][j]:>8.2f}" if j >= i - 1 else f"{'':>8}"
                                     for j in range(0, n + 1)))
    print("\nroot table:")
    print("        " + "".join(f"{'j=' + str(j):>6}" for j in range(1, n + 1)))
    for i in range(1, n + 1):
        print(f"  i={i}   " + "".join(f"{'k' + str(root[i][j]):>6}" if j >= i else f"{'':>6}"
                                     for j in range(1, n + 1)))

    cost = e[1][n]
    print(f"\nMinimum expected search cost = {cost:.2f}")
    assert abs(cost - 2.75) < 1e-9
    check = expected_cost_of_tree(lambda a, b: root[a][b], 1, n, 0, P, Q)
    brute = brute_force_min_cost(P, Q, 1, n)
    print(f"Check by summing (depth+1) x probability over the built tree = {check:.2f}")
    print(f"Check by brute force over every tree shape                 = {brute:.2f}")

    print("\nStructure of the optimal tree:")
    for line in describe(root, 1, n):
        print("  " + line)
    print("\nDrawing (L = left child, R = right child, d = dummy key / failed search):")
    draw(root, 1, n)


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Analysis / conclusion
# Result: minimum expected search cost = 2.75, the value the lab expects.
# Two independent checks agree: summing (depth + 1) x probability over the
# reconstructed tree, and a brute-force search over every possible tree
# shape (Catalan(5) = 42 trees).
# Optimal tree: k2 is the root. k1 (with d0, d1) is its left subtree. k5 is
# its right child, with k4 below k5 on the left and k3 below k4 on the left.
# This is the CLRS Figure 15.9(b) tree.
# The most likely key, k5 (p = 0.20), is NOT the root. Choosing the root
# greedily by probability is not optimal: rooting at k2 balances the
# probability mass of the two sides (w = 0.30 on the left vs 0.60 on the
# right) better than any other choice. The DP accounts for this by adding
# w[i][j] each time a subtree is pushed one level deeper.
# Complexity: Theta(n^2) subproblems x Theta(n) root choices = Theta(n^3) time,
# Theta(n^2) space (Knuth's observation root[i][j-1] <= root[i][j] <=
# root[i+1][j] would reduce this to Theta(n^2)).
# ---------------------------------------------------------------------------
