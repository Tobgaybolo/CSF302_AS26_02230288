"""
CSF302 Lab 6 - Q1: Rod Cutting

Price table for lengths 1..10: 1, 5, 8, 9, 10, 17, 17, 20, 24, 30,
extended with p[i] = 3*i for i > 10.

  1. Naive recursive solution                         Theta(2^n) calls
  2. Top-down memoized solution                        Theta(n^2) work
  3. Bottom-up tabulated solution                      Theta(n^2) work
  4. Maximum revenue and piece lengths for n = 1..10
  5. Calls and time for n = 5, 10, 15, 20, 25
  6. Table in ../results/q1_rod_cutting.md, explanation at the end

Method: time.perf_counter(), median of 3 runs. The call counter is kept in
all versions, so its small overhead is included in every timing.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q1_rod_cutting.py          (about 1 minute: naive n = 25 makes 33 million calls)
"""
import csv
import sys

from timing_utils import markdown_table, time_call

BASE_PRICES = [1, 5, 8, 9, 10, 17, 17, 20, 24, 30]


def price_table(n):
    """p[0..n] with p[0] = 0, the given prices for 1..10, and 3*i after that."""
    return [0] + [BASE_PRICES[i - 1] if i <= 10 else 3 * i for i in range(1, n + 1)]


# ---------------------------------------------------------------------------
# 1. Naive recursion:  r(n) = max_{1<=i<=n} (p[i] + r(n - i)),  r(0) = 0
# ---------------------------------------------------------------------------
def cut_rod_naive(p, n):
    """Return (max revenue, number of calls). Solves the same subproblems
    again and again: T(n) = 1 + sum_{j<n} T(j) = 2^n calls."""
    calls = 0

    def rec(k):
        nonlocal calls
        calls += 1
        if k == 0:
            return 0
        best = float("-inf")
        for i in range(1, k + 1):
            best = max(best, p[i] + rec(k - i))
        return best

    return rec(n), calls


# ---------------------------------------------------------------------------
# 2. Top-down with memoization
# ---------------------------------------------------------------------------
def cut_rod_memo(p, n):
    """Return (max revenue, number of calls). Each subproblem k is computed
    once and stored in memo[k]; later calls return immediately."""
    memo = [None] * (n + 1)
    calls = 0

    def rec(k):
        nonlocal calls
        calls += 1
        if memo[k] is not None:
            return memo[k]
        if k == 0:
            best = 0
        else:
            best = float("-inf")
            for i in range(1, k + 1):
                best = max(best, p[i] + rec(k - i))
        memo[k] = best
        return best

    return rec(n), calls


# ---------------------------------------------------------------------------
# 3. Bottom-up tabulation (with the first-cut table for reconstruction)
# ---------------------------------------------------------------------------
def cut_rod_bottom_up(p, n):
    """Return (r, s, inner_iterations).
    r[j] = best revenue for a rod of length j,
    s[j] = size of the first piece in an optimal cut of length j.
    No recursion at all: subproblems are solved in order j = 1..n."""
    r = [0] * (n + 1)
    s = [0] * (n + 1)
    iterations = 0
    for j in range(1, n + 1):
        best = float("-inf")
        for i in range(1, j + 1):
            iterations += 1
            if p[i] + r[j - i] > best:
                best = p[i] + r[j - i]
                s[j] = i
        r[j] = best
    return r, s, iterations


def pieces(s, n):
    """Follow the first-cut table to list the piece lengths."""
    out = []
    while n > 0:
        out.append(s[n])
        n -= s[n]
    return out


# ---------------------------------------------------------------------------
# 4-6
# ---------------------------------------------------------------------------
def part4():
    p = price_table(10)
    r, s, _ = cut_rod_bottom_up(p, 10)
    rows = []
    for n in range(1, 11):
        cuts = pieces(s, n)
        assert sum(p[c] for c in cuts) == r[n] == cut_rod_naive(p, n)[0] == cut_rod_memo(p, n)[0]
        rows.append((n, r[n], " + ".join(map(str, cuts))))
    table = markdown_table(["n", "max revenue", "piece lengths"], rows)
    print(table)
    return table


def part5():
    rows = []
    for n in [5, 10, 15, 20, 25]:
        p = price_table(n)
        t_naive, (rv_n, calls_n) = time_call(cut_rod_naive, p, n)
        t_memo, (rv_m, calls_m) = time_call(cut_rod_memo, p, n)
        t_bu, (r, s, iters) = time_call(cut_rod_bottom_up, p, n)
        assert rv_n == rv_m == r[n]
        rows.append((n, r[n], calls_n, calls_m, 0, iters, t_naive, t_memo, t_bu))
        print(f"n={n:>2} revenue={r[n]:>3}  calls: naive={calls_n:>10,} memo={calls_m:>4} "
              f"bottom-up=0 (loop iterations {iters})  time: naive={t_naive:.4f}s "
              f"memo={t_memo * 1e6:.1f}us bottom-up={t_bu * 1e6:.1f}us", flush=True)
    return rows


def main():
    print("=== Q1.4  Maximum revenue and pieces, n = 1..10 ===")
    t4 = part4()
    print("\n=== Q1.5  Calls and time (median of 3) ===")
    rows = part5()
    t5 = markdown_table(
        ["n", "revenue", "naive calls", "memo calls", "bottom-up calls", "bottom-up loop iters",
         "naive time (s)", "memo time (s)", "bottom-up time (s)"],
        [(n, rv, f"{cn:,}", f"{cm:,}", cb, it, f"{tn:.3e}", f"{tm:.3e}", f"{tb:.3e}")
         for n, rv, cn, cm, cb, it, tn, tm, tb in rows])
    with open("../results/q1_rod_cutting.md", "w") as f:
        f.write("# Q1 - Rod cutting\n\n## Revenue and pieces, n = 1..10\n\n" + t4 +
                "\n\n## Calls and time (median of 3)\n\n" + t5 + "\n")
    with open("../results/q1_rod_cutting.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "revenue", "naive_calls", "memo_calls", "bottomup_calls",
                    "bottomup_iterations", "naive_s", "memo_s", "bottomup_s"])
        w.writerows(rows)
    print("\nSaved ../results/q1_rod_cutting.{md,csv}")


if __name__ == "__main__":
    sys.setrecursionlimit(10_000)
    main()

# ---------------------------------------------------------------------------
# Analysis / conclusion  (times from one run on my machine; exact times will differ, but call counts and trends should match)
#
# n = 1..10 revenues: 1, 5, 8, 10, 13, 17, 18, 22, 25, 30 (e.g. n = 4 -> 2+2,
# n = 7 -> 1+6, n = 10 -> uncut). All three versions agree on every n.
#
# | n  | revenue | naive calls | memo calls | bottom-up calls (loop iters) | naive (s) | memo (s) | bottom-up (s) |
# |----|---------|-------------|------------|------------------------------|-----------|----------|---------------|
# | 5  | 13      | 32          | 16         | 0 (15)                       | 7.32e-06  | 3.60e-06 | 2.66e-06      |
# | 10 | 30      | 1,024       | 56         | 0 (55)                       | 1.48e-04  | 6.32e-06 | 4.26e-06      |
# | 15 | 45      | 32,768      | 121        | 0 (120)                      | 4.78e-03  | 1.37e-05 | 8.17e-06      |
# | 20 | 60      | 1,048,576   | 211        | 0 (210)                      | 1.61e-01  | 3.55e-05 | 1.45e-05      |
# | 25 | 75      | 33,554,432  | 326        | 0 (325)                      | 6.18      | 5.26e-05 | 2.91e-05      |
#
# Naive: calls = 2^n exactly. T(n) = 1 + T(0) + T(1) + ... + T(n-1) solves to
# T(n) = 2^n, because the same subproblem r(k) is recomputed every time it is
# reached (r(0) alone is computed 2^(n-1) times). Each +5 in n multiplies the
# calls and the time by 2^5 = 32 (0.161 s -> 6.18 s, ~38x measured).
# Memoized: each of the n+1 subproblems is solved once; a call for k makes k
# child calls, so the total is 1 + (1 + 2 + ... + n) = n(n+1)/2 + 1 calls
# (326 for n = 25). After the first call for a size, the rest are O(1)
# cache hits. Theta(n^2) time, Theta(n) space.
# Bottom-up: no recursion at all. Two nested loops do n(n+1)/2 iterations
# (the same work as memo, minus the extra cache-hit call), and it is about
# 1.4-2.4x faster than memo because there is no function-call overhead.
# At n = 25 DP is ~100,000-200,000x faster than naive recursion (6.18 s vs ~29-53 us).
# Both effects come from DP's two conditions: overlapping subproblems (naive
# repeats work) and optimal substructure (r(n) is built from optimal r(n-i)).
# ---------------------------------------------------------------------------
