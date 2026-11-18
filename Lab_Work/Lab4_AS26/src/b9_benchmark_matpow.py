"""
CSF302 Lab 4 - Part B, Question 9
Benchmark naive and binary matrix exponentiation for dimensions
d = 2, 4, 8, 16, 32 and exponents n = 2^4, ..., 2^12.

Method: time.perf_counter(), random matrices generated outside the timed
region (seed 42), median of 3 runs, m = 10^9 + 7. Results go to
../results/b9_benchmark.{csv,md} and ../results/b9_*.png (log-log plots).

Note: the full run takes a few minutes because naive d = 32, n = 4096 does
4096 multiplications of 32x32 matrices. Use --quick for a 1-repeat run.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python b9_benchmark_matpow.py [--quick]
"""
import csv
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from b3_naive_matpow import naive_mat_pow
from b4_binary_matpow import binary_mat_pow
from timing_utils import markdown_table, time_call

MOD = 10**9 + 7
DIMS = [2, 4, 8, 16, 32]
EXPS = [2**k for k in range(4, 13)]


def main(repeats: int):
    rng = random.Random(42)
    mats = {d: [[rng.randrange(MOD) for _ in range(d)] for _ in range(d)] for d in DIMS}
    rows = []
    for d in DIMS:
        A = mats[d]
        assert naive_mat_pow(A, 20, MOD) == binary_mat_pow(A, 20, MOD)   # verify first
        for n in EXPS:
            tn = time_call(naive_mat_pow, A, n, MOD, repeats=repeats)
            tb = time_call(binary_mat_pow, A, n, MOD, repeats=repeats)
            rows.append((d, n, tn, tb, tn / tb))
            print(f"d={d:>2} n={n:>5}  naive={tn:.4e}s  binary={tb:.4e}s  speed-up={tn / tb:,.1f}x",
                  flush=True)

    with open("../results/b9_benchmark.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["d", "n", "naive_s", "binary_s", "speedup"])
        w.writerows(rows)
    table = markdown_table(
        ["d", "n", "naive (s)", "binary (s)", "speed-up"],
        [(d, n, f"{tn:.3e}", f"{tb:.3e}", f"{s:,.1f}x") for d, n, tn, tb, s in rows])
    with open("../results/b9_benchmark.md", "w") as f:
        f.write(f"# Part B Q9 - matrix exponentiation benchmark "
                f"(m = 10^9+7, median of {repeats})\n\n{table}\n")

    # Plot 1: time vs n, one line per d (naive solid, binary dashed)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.8))
    ax = axes[0]
    for d in DIMS:
        sub = [r for r in rows if r[0] == d]
        line, = ax.loglog([r[1] for r in sub], [r[2] for r in sub], "o-", label=f"naive d={d}")
        ax.loglog([r[1] for r in sub], [r[3] for r in sub], "s--", color=line.get_color(),
                  label=f"binary d={d}")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("exponent n")
    ax.set_ylabel("time (s)")
    ax.set_title("Time vs exponent (naive solid, binary dashed)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=7, ncol=2)

    # Plot 2: time vs d at the largest n
    ax = axes[1]
    nmax = EXPS[-1]
    sub = [r for r in rows if r[1] == nmax]
    ax.loglog([r[0] for r in sub], [r[2] for r in sub], "o-", label=f"naive, n={nmax}")
    ax.loglog([r[0] for r in sub], [r[3] for r in sub], "s-", label=f"binary, n={nmax}")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("dimension d")
    ax.set_ylabel("time (s)")
    ax.set_title(f"Time vs dimension (n = {nmax})")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("../results/b9_benchmark.png", dpi=150)
    print("\nSaved ../results/b9_benchmark.{csv,md,png}")


if __name__ == "__main__":
    main(repeats=1 if "--quick" in sys.argv else 3)

# ---------------------------------------------------------------------------
# Analysis / conclusion  (numbers from one run on my machine; exact times will differ, but the trend should match). Full table in
# ../results/b9_benchmark.md.
#
# Selected results (seconds):
# | d  | n=16 naive | n=4096 naive | n=16 binary | n=4096 binary | speed-up @4096 |
# |----|------------|--------------|-------------|---------------|----------------|
# | 2  | 4.60e-05   | 1.12e-02     | 1.62e-05    | 3.88e-05      | 289x           |
# | 4  | 1.44e-04   | 3.64e-02     | 4.85e-05    | 1.08e-04      | 337x           |
# | 8  | 7.26e-04   | 2.07e-01     | 2.60e-04    | 4.39e-04      | 471x           |
# | 16 | 3.26e-03   | 1.30e+00     | 1.05e-03    | 4.17e-03      | 312x           |
# | 32 | 3.87e-02   | 9.11e+00     | 9.51e-03    | 3.66e-02      | 249x           |
#
# 1. Growth in n. Naive time doubles each time n doubles (e.g. d = 32:
#    1.06 s -> 1.96 s -> 4.57 s -> 9.11 s), a slope of ~1 on the log-log
#    plot: Theta(n). Binary time grows by only a small constant per
#    doubling, because n = 2^k needs k squarings + 1 multiply, i.e.
#    k + 1 = 5 .. 13 products: Theta(log n).
# 2. Growth in d. At n = 4096 the naive time rises by 3.3x, 5.7x, 6.3x,
#    7.0x as d doubles, approaching the theoretical factor 2^3 = 8 for
#    Theta(d^3). For small d the per-call Python overhead (list creation,
#    function calls) is a large share of the cost, so the ratio is below 8.
# 3. Speed-up. Because n = 2^k has a single set bit, binary does about
#    log2(n) + 1 products against n for naive, so the theoretical speed-up
#    at n = 4096 is 4096 / 13 = 315x. The measured 249x - 471x is close.
#    Small irregularities (e.g. d = 8, n = 4096 binary faster than n = 2048)
#    are timing noise from the machine; they don't change the trend.
# The measurements match the theory: naive Theta(n d^3), binary
# Theta(d^3 log n).
# ---------------------------------------------------------------------------
