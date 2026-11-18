"""
CSF302 Lab 6 - Q3: Longest Common Subsequence

  1. Fill the LCS table bottom-up and print it for X = ABCBDAB, Y = BDCABA
  2. Reconstruct one LCS from the table
  3. Space-optimised length-only version using two rows
  4. Time DP vs brute force (try every subsequence of X), lengths 5..18
  5. Line-by-line diff of two text files using LCS on lines

Method: time.perf_counter(), random strings over {A,C,G,T} generated
outside the timed region (seed 42), median of 5 runs.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q3_lcs.py                         (parts 1-4, then diff of the sample files)
      python q3_lcs.py diff FILE1 FILE2         (diff of your own files)
"""
import csv
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from timing_utils import markdown_table, time_call


# ---------------------------------------------------------------------------
# 1. Bottom-up table (works for strings or lists of lines)
# ---------------------------------------------------------------------------
def lcs_table(X, Y):
    """c[i][j] = LCS length of X[:i] and Y[:j];  b[i][j] = arrow used:
    '↖' match (diagonal), '↑' from c[i-1][j], '←' from c[i][j-1].
    Theta(mn) time and space."""
    m, n = len(X), len(Y)
    c = [[0] * (n + 1) for _ in range(m + 1)]
    b = [[" "] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if X[i - 1] == Y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
                b[i][j] = "↖"
            elif c[i - 1][j] >= c[i][j - 1]:
                c[i][j] = c[i - 1][j]
                b[i][j] = "↑"
            else:
                c[i][j] = c[i][j - 1]
                b[i][j] = "←"
    return c, b


def print_table(X, Y, c, b):
    print("        " + "".join(f"{'j=' + str(j):>6}" for j in range(len(Y) + 1)))
    print("        " + f"{'':>6}" + "".join(f"{y:>6}" for y in Y))
    for i in range(len(X) + 1):
        label = f"i={i} {X[i - 1] if i else ' '}"
        print(f"{label:<8}" + "".join(f"{b[i][j] + str(c[i][j]):>6}" for j in range(len(Y) + 1)))


# ---------------------------------------------------------------------------
# 2. Reconstruction
# ---------------------------------------------------------------------------
def reconstruct(X, b, i=None, j=None):
    """Follow the arrows from b[m][n] back to an edge; diagonal = LCS item.
    Iterative, O(m + n)."""
    i = len(X) if i is None else i
    j = len(b[0]) - 1 if j is None else j
    out = []
    while i > 0 and j > 0:
        if b[i][j] == "↖":
            out.append(X[i - 1])
            i, j = i - 1, j - 1
        elif b[i][j] == "↑":
            i -= 1
        else:
            j -= 1
    out.reverse()
    return "".join(out) if isinstance(X, str) else out


def lcs(X, Y):
    c, b = lcs_table(X, Y)
    return reconstruct(X, b)


# ---------------------------------------------------------------------------
# 3. Two-row length-only version
# ---------------------------------------------------------------------------
def lcs_length_two_rows(X, Y):
    """Only rows i-1 and i of c are needed, so keep two rows of length
    min(m, n) + 1. Theta(mn) time, Theta(min(m, n)) space."""
    if len(Y) > len(X):
        X, Y = Y, X                        # make Y the shorter string
    prev = [0] * (len(Y) + 1)
    for x in X:
        cur = [0] * (len(Y) + 1)
        for j in range(1, len(Y) + 1):
            if x == Y[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = prev[j] if prev[j] >= cur[j - 1] else cur[j - 1]
        prev = cur
    return prev[-1]


# ---------------------------------------------------------------------------
# 4. Brute force: every subsequence of X
# ---------------------------------------------------------------------------
def is_subsequence(s, Y):
    it = iter(Y)
    return all(ch in it for ch in s)       # consumes Y left to right: O(len(Y))


def lcs_brute_force(X, Y):
    """Try all 2^m subsequences of X (bitmask = which positions are kept),
    keep the longest one that is also a subsequence of Y.
    Theta(2^m * (m + n)) time."""
    m = len(X)
    best = ""
    for mask in range(1 << m):             # every subsequence is generated
        s = "".join(X[i] for i in range(m) if mask >> i & 1)
        if len(s) > len(best) and is_subsequence(s, Y):
            best = s
    return best


def timing():
    rng = random.Random(42)
    rows = []
    for L in range(5, 19):
        X = "".join(rng.choice("ACGT") for _ in range(L))
        Y = "".join(rng.choice("ACGT") for _ in range(L))
        t_dp, (_, b) = time_call(lcs_table, X, Y, repeats=5)
        dp = reconstruct(X, b)
        t_bf, bf = time_call(lcs_brute_force, X, Y, repeats=5)
        assert len(dp) == len(bf) == lcs_length_two_rows(X, Y)
        assert is_subsequence(dp, X) and is_subsequence(dp, Y)
        rows.append((L, len(dp), t_dp, t_bf, t_bf / t_dp))
        print(f"len={L:>2}  LCS length={len(dp):>2}  DP={t_dp * 1e6:>8.1f} us  "
              f"brute={t_bf:>9.4f} s  ratio={t_bf / t_dp:>10,.0f}x", flush=True)

    with open("../results/q3_lcs_timing.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["length", "lcs_length", "dp_s", "brute_s", "ratio"])
        w.writerows(rows)
    with open("../results/q3_lcs_timing.md", "w") as f:
        f.write("# Q3 - LCS: DP vs brute force (alphabet ACGT, median of 5)\n\n" +
                markdown_table(["length", "LCS length", "DP (s)", "brute force (s)", "brute / DP"],
                               [(L, k, f"{a:.3e}", f"{bb:.3e}", f"{r:,.0f}x")
                                for L, k, a, bb, r in rows]) + "\n")
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.semilogy([r[0] for r in rows], [r[2] for r in rows], "o-", label="DP  Θ(mn)")
    ax.semilogy([r[0] for r in rows], [r[3] for r in rows], "s-", label="brute force  Θ(2^m (m+n))")
    ax.set_xlabel("string length (m = n)")
    ax.set_ylabel("time (s, log scale)")
    ax.set_title("LCS: dynamic programming vs brute force")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("../results/q3_lcs_timing.png", dpi=140)
    print("Saved ../results/q3_lcs_timing.{csv,md,png}")


# ---------------------------------------------------------------------------
# 5. Line diff
# ---------------------------------------------------------------------------
def diff_lines(a, b):
    """Return a list of (tag, line) with tag ' ' (in the LCS, unchanged),
    '-' (only in a, removed) or '+' (only in b, added).
    Walk the table from the top-left using the suffix form of the LCS so the
    output comes out in file order."""
    m, n = len(a), len(b)
    # s[i][j] = LCS length of a[i:] and b[j:]
    s = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            s[i][j] = s[i + 1][j + 1] + 1 if a[i] == b[j] else max(s[i + 1][j], s[i][j + 1])
    out, i, j = [], 0, 0
    while i < m and j < n:
        if a[i] == b[j]:
            out.append((" ", a[i]))
            i, j = i + 1, j + 1
        elif s[i + 1][j] >= s[i][j + 1]:
            out.append(("-", a[i]))
            i += 1
        else:
            out.append(("+", b[j]))
            j += 1
    out += [("-", x) for x in a[i:]] + [("+", y) for y in b[j:]]
    return out


def diff_files(path1, path2):
    with open(path1, encoding="utf-8") as f:
        a = f.read().splitlines()
    with open(path2, encoding="utf-8") as f:
        b = f.read().splitlines()
    result = diff_lines(a, b)
    print(f"--- {path1}\n+++ {path2}")
    for tag, line in result:
        print(f"{tag} {line}")
    kept = sum(1 for t, _ in result if t == " ")
    print(f"\n{kept} unchanged (LCS length = {len(lcs(a, b))}), "
          f"{sum(t == '-' for t, _ in result)} removed, {sum(t == '+' for t, _ in result)} added")
    # check: applying the diff to file 1 gives file 2
    assert [l for t, l in result if t != "-"] == b and [l for t, l in result if t != "+"] == a
    return result


def main():
    X, Y = "ABCBDAB", "BDCABA"
    print(f"=== Q3.1  LCS table for X = {X}, Y = {Y}  (arrow + length) ===")
    c, b = lcs_table(X, Y)
    print_table(X, Y, c, b)
    one = reconstruct(X, b)
    print(f"\n=== Q3.2  One LCS: {one} (length {c[-1][-1]})")
    print(f"=== Q3.3  Two-row length: {lcs_length_two_rows(X, Y)}")
    print(f"           brute-force check: {lcs_brute_force(X, Y)} (length {len(lcs_brute_force(X, Y))})")
    print("\n=== Q3.4  Timing DP vs brute force ===")
    timing()
    print("\n=== Q3.5  Diff of data/old.txt and data/new.txt ===")
    diff_files("../data/old.txt", "../data/new.txt")


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "diff":
        diff_files(sys.argv[2], sys.argv[3])
    else:
        main()

# ---------------------------------------------------------------------------
# Analysis / conclusion  (one run on my machine; exact times will differ, but the trends should match)
#
# Q3.1-3.3: For X = ABCBDAB, Y = BDCABA the table gives c[7][6] = 4. Following
# the arrows gives the LCS "BCBA" (the same as CLRS). The two-row version and
# the brute force also return length 4. Ties (c[i-1][j] == c[i][j-1]) are
# broken towards "↑"; breaking them towards "←" gives a different but equally
# long LCS (e.g. BDAB). An LCS is not unique.
#
# Q3.4 timing (alphabet ACGT, m = n, median of 5):
# | length | LCS | DP (us) | brute force (s) | brute / DP |
# |--------|-----|---------|-----------------|------------|
# | 5      | 2   | 4.6     | 0.00002         | 5x         |
# | 8      | 4   | 9.2     | 0.0002          | 25x        |
# | 10     | 6   | 12.5    | 0.0009          | 74x        |
# | 12     | 7   | 23.1    | 0.0049          | 213x       |
# | 14     | 6   | 26.2    | 0.0288          | 1,102x     |
# | 16     | 7   | 39.0    | 0.1332          | 3,412x     |
# | 18     | 8   | 34.9    | 0.4647          | 13,320x    |
# (all 14 lengths in ../results/q3_lcs_timing.md and the plot)
# Brute force generates all 2^m subsequences and checks each in O(m + n):
# Theta(2^m (m + n)). Each +1 in length roughly doubles the time (about 2.1x
# on average; from length 10 to 18 it grew 516x, against the predicted
# 2^8 * 36/20 = 460x). It is a straight line on the semilog plot.
# DP fills (m+1)(n+1) cells: Theta(mn), which is only microseconds here and
# grows gently (quadratically). At length 18 DP is ~13,000x faster, and at
# length 40 brute force would need 2^40 ~ 10^12 subsequences (days).
# Small irregularities are timing noise at the microsecond scale.
#
# Two-row version: row i only needs row i-1, so space drops from Theta(mn) to
# Theta(min(m, n)). The time is the same, but the arrows are gone, so it can
# return only the length and not the subsequence itself.
#
# Q3.5 diff: each line is treated as one symbol. Lines in the LCS are
# printed as unchanged ("  "), other lines of file 1 as removed ("- "), other
# lines of file 2 as added ("+ "). For the sample files: 7 unchanged (= LCS
# length), 2 removed, 3 added. The program also checks that keeping the
# ' '/'+' lines rebuilds file 2 and keeping the ' '/'-' lines rebuilds file 1.
# Maximising the unchanged lines (the LCS) minimises the number of added and
# removed lines, which is the same idea Unix diff is built on.
# ---------------------------------------------------------------------------
