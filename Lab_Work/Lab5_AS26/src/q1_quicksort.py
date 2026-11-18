"""
CSF302 Lab 5 - Q1: Quicksort Variants

  1. Lomuto partition (last element as pivot)
  2. Hoare partition (first element as pivot, as in CLRS)
  3. Randomised quicksort (random pivot, Lomuto partition)
  4. Three-way / Dutch national flag quicksort (random pivot)
  5-6. Count comparisons and time each variant on random, sorted,
       reverse-sorted and many-duplicates (values 0..9) inputs,
       n = 1,000 ... 16,000
  7. Every variant recurses on the SMALLER part and loops on the LARGER
     part, so the recursion depth is at most log2(n) even when the
     algorithm degrades to Theta(n^2) work. No recursion-limit change needed.
  8. Results are written to ../results/q1_*.md / .csv / .png; the
     explanation is in the analysis comment at the end of this file.

A "comparison" is one comparison between an array element and the pivot.

Method: time.perf_counter(), inputs generated outside the timed region
(fixed seed 42), median of 3 runs. Every variant's output is checked
against sorted() (used only as a checker) before timing.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q1_quicksort.py            (full run, several minutes)
      python q1_quicksort.py --quick    (1 repeat, faster)
      python q1_quicksort.py --plot-only (redraw the graph from the saved CSV)
"""
import csv
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from timing_utils import markdown_table, time_sort

_rng = random.Random(42)          # pivot RNG for randomised variants (fixed seed)


# ---------------------------------------------------------------------------
# 1. Lomuto partition, last element as pivot
# ---------------------------------------------------------------------------
def lomuto_partition(a, lo, hi):
    """Partition a[lo..hi] around a[hi]. Returns (pivot_index, comparisons).
    After the call: a[lo..p-1] <= pivot = a[p] < a[p+1..hi]."""
    pivot = a[hi]
    i = lo
    comps = 0
    for j in range(lo, hi):
        comps += 1
        if a[j] <= pivot:
            a[i], a[j] = a[j], a[i]
            i += 1
    a[i], a[hi] = a[hi], a[i]
    return i, comps


def _quicksort_lomuto(a, lo, hi):
    comps = 0
    while lo < hi:
        p, c = lomuto_partition(a, lo, hi)
        comps += c
        if p - lo < hi - p:                       # left part is smaller
            comps += _quicksort_lomuto(a, lo, p - 1)
            lo = p + 1                            # loop on the larger right part
        else:
            comps += _quicksort_lomuto(a, p + 1, hi)
            hi = p - 1
    return comps


def quicksort_lomuto(a):
    """Sort a in place. Returns the number of comparisons."""
    return _quicksort_lomuto(a, 0, len(a) - 1)


# ---------------------------------------------------------------------------
# 2. Hoare partition, first element as pivot
# ---------------------------------------------------------------------------
def hoare_partition(a, lo, hi):
    """CLRS Hoare partition with pivot a[lo]. Returns (j, comparisons) with
    every element of a[lo..j] <= every element of a[j+1..hi], lo <= j < hi."""
    pivot = a[lo]
    i, j = lo - 1, hi + 1
    comps = 0
    while True:
        j -= 1
        comps += 1
        while a[j] > pivot:
            j -= 1
            comps += 1
        i += 1
        comps += 1
        while a[i] < pivot:
            i += 1
            comps += 1
        if i >= j:
            return j, comps
        a[i], a[j] = a[j], a[i]


def _quicksort_hoare(a, lo, hi):
    comps = 0
    while lo < hi:
        p, c = hoare_partition(a, lo, hi)
        comps += c
        if p - lo < hi - p:                       # parts are [lo..p] and [p+1..hi]
            comps += _quicksort_hoare(a, lo, p)
            lo = p + 1
        else:
            comps += _quicksort_hoare(a, p + 1, hi)
            hi = p
    return comps


def quicksort_hoare(a):
    return _quicksort_hoare(a, 0, len(a) - 1)


# ---------------------------------------------------------------------------
# 3. Randomised quicksort: random pivot moved to the end, then Lomuto
# ---------------------------------------------------------------------------
def _quicksort_random(a, lo, hi, rng):
    comps = 0
    while lo < hi:
        r = rng.randint(lo, hi)
        a[r], a[hi] = a[hi], a[r]
        p, c = lomuto_partition(a, lo, hi)
        comps += c
        if p - lo < hi - p:
            comps += _quicksort_random(a, lo, p - 1, rng)
            lo = p + 1
        else:
            comps += _quicksort_random(a, p + 1, hi, rng)
            hi = p - 1
    return comps


def quicksort_random(a, rng=None):
    return _quicksort_random(a, 0, len(a) - 1, rng or _rng)


# ---------------------------------------------------------------------------
# 4. Three-way (Dutch national flag) quicksort, random pivot
# ---------------------------------------------------------------------------
def three_way_partition(a, lo, hi, pivot):
    """Rearrange a[lo..hi] into  < pivot | == pivot | > pivot.
    Returns (lt, gt, comparisons) where a[lt..gt] == pivot."""
    lt, i, gt = lo, lo, hi
    comps = 0
    while i <= gt:
        x = a[i]
        comps += 1
        if x < pivot:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        else:
            comps += 1
            if x > pivot:
                a[i], a[gt] = a[gt], a[i]
                gt -= 1
            else:
                i += 1
    return lt, gt, comps


def _quicksort_3way(a, lo, hi, rng):
    comps = 0
    while lo < hi:
        pivot = a[rng.randint(lo, hi)]
        lt, gt, c = three_way_partition(a, lo, hi, pivot)
        comps += c
        if lt - lo < hi - gt:                     # recurse on smaller outer part
            comps += _quicksort_3way(a, lo, lt - 1, rng)
            lo = gt + 1
        else:
            comps += _quicksort_3way(a, gt + 1, hi, rng)
            hi = lt - 1
    return comps


def quicksort_3way(a, rng=None):
    return _quicksort_3way(a, 0, len(a) - 1, rng or _rng)


VARIANTS = {
    "Lomuto": quicksort_lomuto,
    "Hoare": quicksort_hoare,
    "Randomised": quicksort_random,
    "3-way": quicksort_3way,
}


# ---------------------------------------------------------------------------
# 5-6. Experiments
# ---------------------------------------------------------------------------
SIZES = [1_000, 2_000, 4_000, 8_000, 16_000]


def make_inputs(n, rng):
    rand = [rng.randint(0, 10**6) for _ in range(n)]
    return {
        "random": rand,
        "sorted": sorted(rand),
        "reverse": sorted(rand, reverse=True),
        "duplicates": [rng.randint(0, 9) for _ in range(n)],
    }


STYLES = {   # distinct markers/lines so overlapping curves stay visible
    "Lomuto": dict(marker="o", ls="-", ms=9, lw=2.5),
    "Hoare": dict(marker="x", ls="--", ms=9, lw=1.5),
    "Randomised": dict(marker="s", ls="-", ms=5, lw=1.5),
    "3-way": dict(marker="^", ls="-.", ms=6, lw=1.5),
}


def plot_results(rows):
    """Comparisons vs n, one panel per input type (log-log)."""
    fig, axes = plt.subplots(1, 4, figsize=(18, 4.6), sharey=True)
    for ax, kind in zip(axes, ["random", "sorted", "reverse", "duplicates"]):
        for name in VARIANTS:
            sub = [r for r in rows if r[0] == name and r[1] == kind]
            ax.loglog([r[2] for r in sub], [r[3] for r in sub], label=name,
                      mfc="none", **STYLES[name])
        ax.loglog(SIZES, [n * n / 2 for n in SIZES], "k:", alpha=0.5, label="n²/2")
        ax.loglog(SIZES, [1.39 * n * n.bit_length() for n in SIZES], color="grey",
                  ls=(0, (1, 3)), alpha=0.7, label="1.39 n log₂n")
        ax.set_title(f"{kind} input")
        ax.set_xlabel("n")
        ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("comparisons")
    axes[0].legend(fontsize=8)
    fig.suptitle("Quicksort variants: comparisons vs n (log-log). "
                 "Overlapping markers = same growth, e.g. Lomuto and Hoare on sorted input")
    fig.tight_layout()
    fig.savefig("../results/q1_comparisons.png", dpi=140)


def plot_from_csv():
    with open("../results/q1_quicksort.csv") as f:
        r = csv.reader(f)
        next(r)
        rows = [(v, k, int(n), int(c), float(t)) for v, k, n, c, t in r]
    plot_results(rows)
    print("Re-drew ../results/q1_comparisons.png from q1_quicksort.csv")


def verify():
    rng = random.Random(7)
    for n in [0, 1, 2, 3, 10, 100, 1000]:
        for kind, data in make_inputs(n, rng).items():
            for name, fn in VARIANTS.items():
                arr = list(data)
                fn(arr)
                assert arr == sorted(data), f"{name} failed on {kind} n={n}"
    print("All four variants sort correctly on every input type (checked with sorted()).")


def main(repeats):
    verify()
    rng = random.Random(42)
    inputs = {n: make_inputs(n, rng) for n in SIZES}
    rows = []            # (variant, input, n, comparisons, time)
    for kind in ["random", "sorted", "reverse", "duplicates"]:
        for name, fn in VARIANTS.items():
            for n in SIZES:
                t, comps = time_sort(fn, inputs[n][kind], repeats=repeats)
                rows.append((name, kind, n, comps, t))
                print(f"{kind:<10} {name:<10} n={n:>6}  comparisons={comps:>12,}  "
                      f"time={t:.4f}s  comps/(n log2 n)={comps / (n * n.bit_length()):.2f}  "
                      f"comps/n^2={comps / n**2:.3f}", flush=True)

    with open("../results/q1_quicksort.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["variant", "input", "n", "comparisons", "time_s"])
        w.writerows(rows)

    md = [f"# Q1 - Quicksort variants (median of {repeats} runs, seed 42)\n"]
    for kind in ["random", "sorted", "reverse", "duplicates"]:
        md.append(f"\n## Input: {kind}\n\n### Comparisons\n")
        md.append(markdown_table(["n"] + list(VARIANTS),
                  [[f"{n:,}"] + [f"{r[3]:,}" for r in rows if r[1] == kind and r[2] == n]
                   for n in SIZES]))
        md.append("\n\n### Time (s)\n")
        md.append(markdown_table(["n"] + list(VARIANTS),
                  [[f"{n:,}"] + [f"{r[4]:.4f}" for r in rows if r[1] == kind and r[2] == n]
                   for n in SIZES]))
        md.append("\n")
    with open("../results/q1_quicksort.md", "w") as f:
        f.write("\n".join(md))

    plot_results(rows)
    print("\nSaved ../results/q1_quicksort.{csv,md} and q1_comparisons.png")


if __name__ == "__main__":
    if "--plot-only" in sys.argv:
        plot_from_csv()
    else:
        main(repeats=1 if "--quick" in sys.argv else 3)

# ---------------------------------------------------------------------------
# Analysis / conclusion  (one run on my machine; exact times will differ, but
# the trends should match and comparison counts for fixed pivots are identical)
#
# Comparisons at n = 16,000 (full tables in ../results/q1_quicksort.md):
# | input      | Lomuto      | Hoare       | Randomised | 3-way   |
# |------------|-------------|-------------|------------|---------|
# | random     | 259,559     | 354,227     | 250,240    | 396,764 |
# | sorted     | 127,992,000 | 128,024,125 | 258,579    | 449,876 |
# | reverse    | 127,087,790 | 127,518,897 | 259,571    | 388,287 |
# | duplicates | 12,848,664  | 272,866     | 12,858,565 | 78,679  |
# Time at n = 16,000: Lomuto sorted 11.3 s, Hoare sorted 7.6 s, versus
# 0.02-0.04 s for every Theta(n log n) case.
#
# How to read it: Theta(n log n) rows grow ~2.1x when n doubles and stay at
# ~1-2 x n log2 n comparisons. Theta(n^2) rows grow 4x when n doubles and
# sit at comps/n^2 = 0.5 (that is n(n-1)/2) - see the comps/n^2 column in
# the log and the n^2/2 reference line in q1_comparisons.png.
#
# Which variant degrades to Theta(n^2), and why:
# * Lomuto (last pivot) on SORTED input: the pivot is the maximum, so every
#   partition puts n-1 elements on the left and 0 on the right.
#   (n-1)+(n-2)+...+1 = n(n-1)/2 = 127,992,000 for n = 16,000, exactly
#   what was measured.
# * Lomuto on REVERSE input: the pivot is the minimum, so the split is again
#   0 / n-1 (after the first swap the pattern repeats), giving ~n^2/2.
# * Hoare (first pivot) on SORTED and REVERSE input: the first element is
#   the minimum (sorted) or maximum (reverse), so the partition splits off
#   just one element each time, giving ~n^2/2 comparisons.
# * Lomuto AND Randomised on MANY DUPLICATES (0..9): Lomuto sends every
#   element equal to the pivot to the same side. With only 10 distinct
#   values, each group of ~n/10 equal keys eventually forms a subarray where
#   every split is n-1 / 0, so the cost is about 10 * (n/10)^2 / 2 =
#   n^2/20 - comps/n^2 = 0.050 measured. A random pivot does not help,
#   because the problem is equal keys, not a bad pivot choice.
#
# Which variants do NOT degrade:
# * Hoare on duplicates: both pointers stop on keys EQUAL to the pivot and
#   swap them, so equal keys are split evenly between the two sides ->
#   balanced, Theta(n log n).
# * Randomised on sorted/reverse: a random pivot is a good pivot with high
#   probability whatever the input order -> expected Theta(n log n).
# * 3-way on every input: a random pivot avoids the sorted/reverse problem,
#   and the "== pivot" middle band is removed from all further recursion,
#   so duplicates make it FASTER (78,679 comparisons, well below
#   n log2 n = 224,000). With only 10 distinct values it is about
#   Theta(n log 10), i.e. linear in n.
#
# Recursion depth: every variant recurses only on the smaller part and loops
# on the larger one, so even the n^2/2 cases used depth <= log2(16,000) ~ 14
# and Python's default recursion limit (1000) was never reached.
# The measurements match the theory. Note: part of this run shared the
# 2-core machine with the Q2/Q3 benchmarks, so a few times are slightly
# noisy; the comparison counts are unaffected.
# ---------------------------------------------------------------------------
