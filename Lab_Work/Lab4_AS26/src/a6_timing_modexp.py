"""
CSF302 Lab 4 - Part A, Question 6
Measure and compare execution times of naive and binary modular
exponentiation for b = 10, 100, ..., 10^6.

Method: time.perf_counter(), inputs generated outside the timed region,
median of 3 runs, fixed random seed. Results are saved to
../results/a6_timing.csv, ../results/a6_timing.md and a log-log plot
../results/a6_timing.png.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python a6_timing_modexp.py
"""
import csv
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from a1_naive_modexp import naive_mod_pow
from a5_validated_modexp import mod_pow as binary_mod_pow
from timing_utils import markdown_table, time_call

M = 1_000_000_007
EXPONENTS = [10**k for k in range(1, 7)]
REPEATS = 3


def main():
    rng = random.Random(42)
    a = rng.randint(2, M - 1)            # input generated outside the timer
    rows = []
    for b in EXPONENTS:
        assert naive_mod_pow(a, b, M) == binary_mod_pow(a, b, M)   # verify first
        t_naive = time_call(naive_mod_pow, a, b, M, repeats=REPEATS)
        # binary is very fast: time 1000 calls and divide to get a stable value
        t_bin = time_call(lambda: [binary_mod_pow(a, b, M) for _ in range(1000)],
                          repeats=REPEATS) / 1000
        rows.append((b, t_naive, t_bin, t_naive / t_bin))

    headers = ["b", "naive (s)", "binary (s)", "speed-up"]
    fmt = [(f"{b:,}", f"{tn:.3e}", f"{tb:.3e}", f"{s:,.0f}x") for b, tn, tb, s in rows]
    table = markdown_table(headers, fmt)
    print(f"a = {a}, m = {M}, median of {REPEATS} runs\n")
    print(table)

    with open("../results/a6_timing.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["b", "naive_s", "binary_s", "speedup"])
        w.writerows(rows)
    with open("../results/a6_timing.md", "w") as f:
        f.write(f"# Part A Q6 - timing (a={a}, m={M}, median of {REPEATS})\n\n{table}\n")

    bs = [r[0] for r in rows]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.loglog(bs, [r[1] for r in rows], "o-", label="naive  O(b)")
    ax.loglog(bs, [r[2] for r in rows], "s-", label="binary  O(log b)")
    ax.set_xlabel("exponent b")
    ax.set_ylabel("time (s)")
    ax.set_title("Modular exponentiation: naive vs binary (log-log)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("../results/a6_timing.png", dpi=150)
    print("\nSaved ../results/a6_timing.{csv,md,png}")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Analysis / conclusion  (numbers from one run on my machine; exact times will differ, but the trend should match)
#
# | b         | naive (s) | binary (s) |
# |-----------|-----------|------------|
# | 10        | 1.199e-06 | 7.229e-07  |
# | 100       | 4.111e-06 | 9.376e-07  |
# | 1,000     | 4.336e-05 | 1.228e-06  |
# | 10,000    | 4.190e-04 | 1.496e-06  |
# | 100,000   | 4.295e-03 | 1.781e-06  |
# | 1,000,000 | 4.360e-02 | 2.108e-06  |
#
# Naive: each 10x increase in b gives roughly a 10x increase in time, so on
# the log-log plot it is a straight line of slope ~1 -> Theta(b), as expected.
# Small b (10, 100) is dominated by fixed function-call overhead, so the
# first points sit slightly above the line.
# Binary: time grows only slightly (about log2(10) = 3.3 more loop iterations
# per 10x in b), so the curve is almost flat -> Theta(log b), as expected.
# The speed-up grows from single digits at b = 10 to tens of thousands at
# b = 10^6. The measurements match the theoretical complexities.
# ---------------------------------------------------------------------------
