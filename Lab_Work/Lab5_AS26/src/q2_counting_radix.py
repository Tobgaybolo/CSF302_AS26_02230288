"""
CSF302 Lab 5 - Q2: Counting Sort and Radix Sort

  1. Stable counting sort for integers in 0..k
  2. LSD radix sort using a stable counting sort on each digit
     (base 10, then base 256)
  3. Comparison with merge sort from Lab 1 (merge_sort.py)
  4. n = 100,000 fixed, k = 10, 10^3, 10^5, 10^7          (counting sort)
  5. k = 10^9 fixed, n = 10,000 ... 1,000,000             (radix vs merge)
  6. Plots in ../results/q2_*.png, explanation at the end of this file
  7. Stability demo: sort (key, original index) pairs by key

Method: time.perf_counter(), inputs generated outside the timed region
(fixed seed 42), median of 3 runs. Outputs are checked against sorted()
(used only as a checker) before timing.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q2_counting_radix.py            (about 2-3 minutes)
      python q2_counting_radix.py --quick    (1 repeat)
"""
import csv
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from merge_sort import merge_sort
from timing_utils import markdown_table, time_sort


# ---------------------------------------------------------------------------
# 1. Stable counting sort
# ---------------------------------------------------------------------------
def counting_sort(a, k):
    """Return a new list with the integers of `a` (each in 0..k) in sorted order.

    1. count[v] = how many times v occurs                     Theta(n)
    2. prefix sums: count[v] = number of elements <= v        Theta(k)
    3. scan a from RIGHT to LEFT, put each x at position
       count[x]-1 and decrement count[x]                     Theta(n)
    Scanning right-to-left puts the last copy of each value in the last slot
    for that value, so equal keys keep their original order -> STABLE.
    Time Theta(n + k), extra space Theta(n + k).
    """
    if k < 0:
        raise ValueError("k must be >= 0")
    count = [0] * (k + 1)
    for x in a:
        if not 0 <= x <= k:
            raise ValueError(f"value {x} is outside 0..{k}")
        count[x] += 1
    for v in range(1, k + 1):
        count[v] += count[v - 1]
    out = [0] * len(a)
    for x in reversed(a):
        count[x] -= 1
        out[count[x]] = x
    return out


def counting_sort_by_key(items, k, key):
    """Same algorithm, but sorts arbitrary records by key(record) in 0..k.
    Used for the stability demo and by radix sort."""
    count = [0] * (k + 1)
    keys = [key(it) for it in items]
    for kv in keys:
        count[kv] += 1
    for v in range(1, k + 1):
        count[v] += count[v - 1]
    out = [None] * len(items)
    for idx in range(len(items) - 1, -1, -1):
        kv = keys[idx]
        count[kv] -= 1
        out[count[kv]] = items[idx]
    return out


# ---------------------------------------------------------------------------
# 2. LSD radix sort
# ---------------------------------------------------------------------------
def radix_sort(a, base=10):
    """LSD radix sort of non-negative integers.

    For each digit position, from least to most significant, do a stable
    counting sort on that digit (digit values 0..base-1). Stability makes
    the order from earlier (less significant) digits survive among equal
    digits, so after the last pass the list is fully sorted.
    Time Theta(d * (n + base)) with d = number of base-`base` digits of max(a).
    """
    if base < 2:
        raise ValueError("base must be >= 2")
    if not a:
        return []
    if min(a) < 0:
        raise ValueError("radix_sort needs non-negative integers")
    out = list(a)
    biggest = max(out)
    exp = 1
    while biggest // exp > 0:
        # --- stable counting sort on digit (x // exp) % base ---
        count = [0] * base
        digits = [(x // exp) % base for x in out]
        for dgt in digits:
            count[dgt] += 1
        for v in range(1, base):
            count[v] += count[v - 1]
        nxt = [0] * len(out)
        for idx in range(len(out) - 1, -1, -1):
            dgt = digits[idx]
            count[dgt] -= 1
            nxt[count[dgt]] = out[idx]
        out = nxt
        exp *= base
    return out


def radix_sort_10(a):
    return radix_sort(a, 10)


def radix_sort_256(a):
    return radix_sort(a, 256)


def number_of_passes(max_value, base):
    d, exp = 0, 1
    while max_value // exp > 0:
        d += 1
        exp *= base
    return d


# ---------------------------------------------------------------------------
# 7. Stability demonstration
# ---------------------------------------------------------------------------
def stability_demo():
    rng = random.Random(42)
    keys = [rng.randint(0, 4) for _ in range(15)]
    pairs = [(k, i) for i, k in enumerate(keys)]           # (key, original index)
    result = counting_sort_by_key(pairs, 4, key=lambda p: p[0])
    print("Input  (key, original index):", pairs)
    print("Output (key, original index):", result)
    stable = all(result[i][1] < result[i + 1][1]
                 for i in range(len(result) - 1) if result[i][0] == result[i + 1][0])
    print("Within each key, original indices are increasing ->",
          "STABLE" if stable else "NOT stable")
    # Larger check
    keys = [rng.randint(0, 50) for _ in range(20_000)]
    pairs = [(k, i) for i, k in enumerate(keys)]
    assert counting_sort_by_key(pairs, 50, key=lambda p: p[0]) == sorted(pairs)
    print("20,000 random (key, index) pairs: output == sorted by (key, index) -> stable")
    return stable


def verify():
    rng = random.Random(1)
    for n in [0, 1, 2, 10, 1000]:
        for k in [0, 1, 9, 1000, 10**6]:
            a = [rng.randint(0, k) for _ in range(n)]
            s = sorted(a)
            assert counting_sort(a, k) == s
            assert radix_sort_10(a) == s and radix_sort_256(a) == s
            assert merge_sort(a) == s
    print("counting sort, radix (10, 256) and merge sort all agree with sorted().")


# ---------------------------------------------------------------------------
# 4-6. Experiments
# ---------------------------------------------------------------------------
def experiment_vary_k(repeats):
    n, rng = 100_000, random.Random(42)
    ks = [10, 10**3, 10**5, 10**7]
    rows = []
    for k in ks:
        data = [rng.randint(0, k) for _ in range(n)]
        t_cnt, out = time_sort(lambda a: counting_sort(a, k), data, repeats)
        assert out == sorted(data)
        t_r10, _ = time_sort(radix_sort_10, data, repeats)
        t_r256, _ = time_sort(radix_sort_256, data, repeats)
        t_ms, _ = time_sort(merge_sort, data, repeats)
        rows.append((k, t_cnt, t_r10, t_r256, t_ms))
        print(f"[vary k] n={n:,} k={k:>10,}  counting={t_cnt:.4f}s  radix10={t_r10:.4f}s "
              f"radix256={t_r256:.4f}s  merge={t_ms:.4f}s", flush=True)
    return rows


def experiment_vary_n(repeats):
    k, rng = 10**9, random.Random(43)
    ns = [10_000, 30_000, 100_000, 300_000, 1_000_000]
    rows = []
    for n in ns:
        data = [rng.randint(0, k) for _ in range(n)]
        t_r10, out = time_sort(radix_sort_10, data, repeats)
        assert out == sorted(data)
        t_r256, _ = time_sort(radix_sort_256, data, repeats)
        t_ms, _ = time_sort(merge_sort, data, repeats)
        rows.append((n, t_r10, t_r256, t_ms))
        print(f"[vary n] k=10^9 n={n:>9,}  radix10={t_r10:.4f}s  radix256={t_r256:.4f}s  "
              f"merge={t_ms:.4f}s", flush=True)
    return rows


def main(repeats):
    print("=== Q2.7 Stability ===")
    stability_demo()
    print("\n=== Verification ===")
    verify()
    print(f"\nPasses for k = 10^9: base 10 -> {number_of_passes(10**9, 10)}, "
          f"base 256 -> {number_of_passes(10**9, 256)}\n")

    rk = experiment_vary_k(repeats)
    rn = experiment_vary_n(repeats)

    with open("../results/q2_vary_k.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["k", "counting_s", "radix10_s", "radix256_s", "merge_s"])
        w.writerows(rk)
    with open("../results/q2_vary_n.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "radix10_s", "radix256_s", "merge_s"])
        w.writerows(rn)
    md = [f"# Q2 - Counting sort, radix sort, merge sort (median of {repeats} runs)\n",
          "## n = 100,000, varying k\n",
          markdown_table(["k", "counting (s)", "radix b10 (s)", "radix b256 (s)", "merge (s)"],
                         [(f"{k:,}", *(f"{t:.4f}" for t in r)) for k, *r in rk]),
          "\n\n## k = 10^9, varying n (counting sort skipped: count array would need 10^9 entries)\n",
          markdown_table(["n", "radix b10 (s)", "radix b256 (s)", "merge (s)"],
                         [(f"{n:,}", *(f"{t:.4f}" for t in r)) for n, *r in rn]), "\n"]
    with open("../results/q2_results.md", "w") as f:
        f.write("\n".join(md))

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    ax = axes[0]
    ks = [r[0] for r in rk]
    for idx, label, style in [(1, "counting sort", "o-"), (2, "radix base 10", "s-"),
                              (3, "radix base 256", "^-"), (4, "merge sort", "d-")]:
        ax.loglog(ks, [r[idx] for r in rk], style, label=label)
    ax.set_xlabel("key range k")
    ax.set_ylabel("time (s)")
    ax.set_title("n = 100,000, varying k")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    ax = axes[1]
    ns = [r[0] for r in rn]
    for idx, label, style in [(1, "radix base 10", "s-"), (2, "radix base 256", "^-"),
                              (3, "merge sort", "d-")]:
        ax.loglog(ns, [r[idx] for r in rn], style, label=label)
    ax.set_xlabel("n")
    ax.set_ylabel("time (s)")
    ax.set_title("k = 10^9, varying n")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("../results/q2_linear_sorts.png", dpi=140)
    print("\nSaved ../results/q2_results.md, q2_vary_k.csv, q2_vary_n.csv, q2_linear_sorts.png")


if __name__ == "__main__":
    main(repeats=1 if "--quick" in sys.argv else 3)

# ---------------------------------------------------------------------------
# Analysis / conclusion  (one run on my machine; exact times will differ, but the trends should match)
#
# n = 100,000, varying k (seconds):
# | k          | counting | radix b10 | radix b256 | merge  |
# |------------|----------|-----------|------------|--------|
# | 10         | 0.0102   | 0.0398    | 0.0230     | 0.2582 |
# | 1,000      | 0.0150   | 0.1008    | 0.0454     | 0.2841 |
# | 100,000    | 0.0422   | 0.1663    | 0.0690     | 0.2282 |
# | 10,000,000 | 0.9943   | 0.1509    | 0.0704     | 0.2406 |
#
# k = 10^9, varying n (seconds):
# | n         | radix b10 | radix b256 | merge  |
# |-----------|-----------|------------|--------|
# | 10,000    | 0.0187    | 0.0083     | 0.0213 |
# | 30,000    | 0.0660    | 0.0275     | 0.0697 |
# | 100,000   | 0.2381    | 0.1141     | 0.2938 |
# | 300,000   | 0.9195    | 0.3801     | 0.8898 |
# | 1,000,000 | 3.3917    | 1.7565     | 3.4520 |
#
# Counting sort, Theta(n + k):
#  - When k <= n (k = 10 .. 10^5) it is the fastest method, 5-25x faster
#    than merge sort: one counting pass, one prefix-sum pass over k, one
#    placement pass, and no comparisons.
#  - When k >> n (k = 10^7 = 100n) the Theta(k) prefix-sum loop and the
#    10^7-entry count array dominate. It becomes 4x SLOWER than merge sort
#    and needs ~80 MB just for the counts. At k = 10^9 it is not usable
#    (8 GB array), which is why only radix and merge are run there.
#
# LSD radix sort, Theta(d (n + b)) with d = ceil(log_b(k+1)) passes:
#  - The time depends on the number of passes, not on k itself: base 256
#    needs 3 passes for both k = 10^5 and k = 10^7 and took the same time
#    (0.069 s vs 0.070 s).
#  - k = 10^9 needs d = 10 passes in base 10 but only d = 4 in base 256, so
#    base 256 is ~1.9-2.4x faster than base 10 at every n. A bigger base
#    means fewer passes, at the cost of a count array of size b, which is
#    tiny compared with n.
#  - Radix time grows linearly in n (about 10x per 10x n), while merge sort
#    grows as n log n. Radix-256 beat merge sort at every n (2.0-2.6x).
#  - Radix base 10 only roughly ties merge sort (slightly faster at most n,
#    slower at n = 3*10^5): 10 passes x n is close to n log2 n ~ 17-20n,
#    and each radix pass in Python costs about as much as a merge level.
#
# When linear-time sorts WIN: integer keys with a small range (k = O(n))
# for counting sort; a fixed key width with few passes (large base) for
# radix sort; large n.
# When they LOSE: k much larger than n (counting sort); many digits / a
# small base (radix base 10); small n, where fixed overheads dominate;
# keys that are not small non-negative integers (floats, strings, custom
# comparisons), where merge sort works and they need extra encoding.
#
# Stability (Q2.7): sorting (key, original index) pairs by key alone gave
# indices in increasing order within every key (15-item demo, plus 20,000
# pairs equal to sorted by (key, index)). Stability comes from the
# right-to-left placement pass, and radix sort's correctness depends on it.
# ---------------------------------------------------------------------------
