"""
benchmark.py - Part C timings for Assignment 3.

Produces results/*.csv and results/*.png. Run:  python benchmark.py
Each time is the median of REPEATS runs, each on a fresh copy of the same
input. Python's default recursion limit (1000) is kept for the main
experiment, so a RecursionError is recorded as "CRASH", exactly as the bank
would have seen it.
"""

import csv
import os
import platform
import random
import statistics
import sys
import threading
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sorts import quicksort_basic, quicksort_improved, quicksort_random_lomuto

random.seed(12345)
OUT = "results"
os.makedirs(OUT, exist_ok=True)
REPEATS = 3
SIZES = [1000 * 2**k for k in range(7)]          # 1,000 ... 64,000
TIME_LIMIT = 30.0                                  # skip larger n after this


def make_input(kind, n):
    if kind == "random":
        return [random.randint(0, 10**6) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "dups":
        return [random.randint(0, 9) for _ in range(n)]
    raise ValueError(kind)


def time_sort(fn, data, repeats=REPEATS):
    """Median wall time in seconds, or 'CRASH' on RecursionError."""
    times = []
    for _ in range(repeats):
        a = list(data)
        t0 = time.perf_counter()
        try:
            fn(a)
        except RecursionError:
            return "CRASH"
        times.append(time.perf_counter() - t0)
        assert a == sorted(data)          # brute-force correctness check
    return statistics.median(times)


def run_in_big_stack(fn):
    """Run fn() in a thread with a 512 MB stack and a high recursion limit
    (used only for the supplementary 'what if it didn't crash' run)."""
    box = {}
    threading.stack_size(512 * 1024 * 1024)
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(200_000)
    t = threading.Thread(target=lambda: box.setdefault("r", fn()))
    t.start(); t.join()
    sys.setrecursionlimit(old)
    threading.stack_size(0)
    return box["r"]


def fmt(x):
    return x if isinstance(x, str) else f"{x:.4f}"


# ---------------------------------------------------------------------------
# Experiment 1: basic vs improved vs sorted() on three input types
# ---------------------------------------------------------------------------
def experiment_main():
    algos = {
        "quicksort_basic": quicksort_basic,
        "quicksort_improved": lambda a: quicksort_improved(a, cutoff=BEST_CUTOFF),
        "sorted()": lambda a: a.__setitem__(slice(None), sorted(a)),
    }
    rows = []
    for kind in ["random", "sorted", "dups"]:
        for n in SIZES:
            data = make_input(kind, n)
            row = {"input": kind, "n": n}
            for name, fn in algos.items():
                row[name] = time_sort(fn, data)
            rows.append(row)
            print(kind, n, {k: fmt(v) for k, v in row.items() if k not in ("input", "n")}, flush=True)
    with open(f"{OUT}/main_timings.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["input", "n", *algos])
        w.writeheader()
        for r in rows:
            w.writerow({k: fmt(v) if k not in ("input", "n") else v for k, v in r.items()})
    return rows


# ---------------------------------------------------------------------------
# Experiment 2: what basic quicksort costs if it is NOT stopped by the
# recursion limit (shows the Theta(n^2) growth predicted by the recurrence)
# plus the random-pivot Lomuto variant on duplicates
# ---------------------------------------------------------------------------
def experiment_quadratic():
    rows = []
    for kind, fn_name, fn in [
        ("sorted", "quicksort_basic", quicksort_basic),
        ("dups", "quicksort_basic", quicksort_basic),
        ("dups", "random_pivot_lomuto", lambda a: quicksort_random_lomuto(a, 16)),
    ]:
        for n in SIZES:
            data = make_input(kind, n)
            t = run_in_big_stack(lambda: time_sort(fn, data, repeats=1))
            rows.append({"input": kind, "algorithm": fn_name, "n": n, "seconds": t})
            print("quad", kind, fn_name, n, fmt(t), flush=True)
            if not isinstance(t, str) and t > TIME_LIMIT:
                break
    with open(f"{OUT}/no_limit_timings.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["input", "algorithm", "n", "seconds"])
        w.writeheader()
        for r in rows:
            w.writerow({**r, "seconds": fmt(r["seconds"])})
    return rows


# ---------------------------------------------------------------------------
# Experiment 3: cutoff tuning, n = 100,000 random
# ---------------------------------------------------------------------------
def experiment_cutoff():
    data = make_input("random", 100_000)
    rows = []
    for c in [1, 4, 8, 16, 32, 64]:
        t = time_sort(lambda a: quicksort_improved(a, cutoff=c), data, repeats=7)
        rows.append({"cutoff": c, "seconds": t})
        print("cutoff", c, fmt(t), flush=True)
    with open(f"{OUT}/cutoff_timings.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["cutoff", "seconds"])
        w.writeheader()
        for r in rows:
            w.writerow({**r, "seconds": fmt(r["seconds"])})
    return rows


# ---------------------------------------------------------------------------
# Graphs
# ---------------------------------------------------------------------------
COLORS = {"quicksort_basic": "#c0392b", "quicksort_improved": "#1f6fb2",
          "sorted()": "#2e8b57", "random_pivot_lomuto": "#8e6bbf"}
TITLES = {"random": "Random values", "sorted": "Already sorted",
          "dups": "Many duplicates (0–9)"}


def plot_main(rows):
    fig, axes = plt.subplots(1, 3, figsize=(12, 3.8), sharey=True)
    for ax, kind in zip(axes, ["random", "sorted", "dups"]):
        sub = [r for r in rows if r["input"] == kind]
        for name in ["quicksort_basic", "quicksort_improved", "sorted()"]:
            xs = [r["n"] for r in sub if not isinstance(r[name], str)]
            ys = [r[name] for r in sub if not isinstance(r[name], str)]
            if xs:
                ax.plot(xs, ys, "o-", color=COLORS[name], label=name, lw=2, ms=4)
            crashes = [r["n"] for r in sub if r[name] == "CRASH"]
            if crashes:
                ax.scatter(crashes, [2e-4] * len(crashes),
                           marker="x", s=60, color=COLORS[name],
                           label=f"{name}: RecursionError", zorder=5)
        ax.set_xscale("log", base=2); ax.set_yscale("log")
        ax.set_title(TITLES[kind]); ax.set_xlabel("n (list size)")
        ax.set_xticks(SIZES); ax.set_xticklabels([f"{n//1000}k" for n in SIZES])
        ax.grid(True, which="both", alpha=0.3)
    axes[0].set_ylabel("time (seconds, log scale)")
    axes[0].legend(fontsize=7, loc="upper left")
    for ax in axes[1:]:
        ax.legend(fontsize=7, loc="upper left")
    fig.suptitle("Figure 1. Sorting time vs n (crashes plotted as × at the bottom)", fontsize=10)
    fig.tight_layout()
    fig.savefig(f"{OUT}/fig1_main.png", dpi=200)
    plt.close(fig)


def plot_quadratic(rows, main_rows):
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    series = [("sorted", "quicksort_basic", "basic, sorted input"),
              ("dups", "quicksort_basic", "basic, duplicates 0–9"),
              ("dups", "random_pivot_lomuto", "random pivot + Lomuto, duplicates")]
    cols = ["#c0392b", "#e67e22", "#8e6bbf"]
    for (kind, algo, label), c in zip(series, cols):
        sub = [r for r in rows if r["input"] == kind and r["algorithm"] == algo
               and not isinstance(r["seconds"], str)]
        ax.plot([r["n"] for r in sub], [r["seconds"] for r in sub], "o-", color=c, label=label, lw=2, ms=4)
    imp = [r for r in main_rows if r["input"] == "sorted"]
    ax.plot([r["n"] for r in imp], [r["quicksort_improved"] for r in imp], "o-",
            color=COLORS["quicksort_improved"], label="improved, sorted input", lw=2, ms=4)
    # reference slope n^2
    sub = [r for r in rows if r["input"] == "sorted" and r["algorithm"] == "quicksort_basic"]
    n0, t0 = sub[0]["n"], sub[0]["seconds"]
    ax.plot(SIZES, [t0 * (n / n0) ** 2 for n in SIZES], "k--", lw=1, label="slope of n² (reference)")
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    ax.set_xticks(SIZES); ax.set_xticklabels([f"{n//1000}k" for n in SIZES])
    ax.set_xlabel("n (list size)"); ax.set_ylabel("time (seconds, log scale)")
    ax.set_ylim(top=200)
    ax.set_title("Figure 2. Bad cases with the recursion limit removed", fontsize=10)
    ax.grid(True, which="both", alpha=0.3); ax.legend(fontsize=7)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig2_quadratic.png", dpi=200); plt.close(fig)


def plot_cutoff(rows):
    fig, ax = plt.subplots(figsize=(5.4, 3.2))
    xs = [str(r["cutoff"]) for r in rows]
    ys = [r["seconds"] for r in rows]
    best = min(range(len(ys)), key=ys.__getitem__)
    bars = ax.bar(xs, ys, color=["#1f6fb2" if i == best else "#9ebfdc" for i in range(len(ys))])
    for b, y in zip(bars, ys):
        ax.text(b.get_x() + b.get_width() / 2, y, f"{y:.3f}", ha="center", va="bottom", fontsize=8)
    ax.set_xlabel("cutoff"); ax.set_ylabel("median time (s)")
    ax.set_ylim(0, max(ys) * 1.15)
    ax.set_title("Figure 3. quicksort_improved, n = 100,000 random", fontsize=10)
    fig.tight_layout(); fig.savefig(f"{OUT}/fig3_cutoff.png", dpi=200); plt.close(fig)


if __name__ == "__main__":
    print("Python", platform.python_version(), platform.machine(), platform.system())
    cut_rows = experiment_cutoff()
    BEST_CUTOFF = min(cut_rows, key=lambda r: r["seconds"])["cutoff"]
    print("best cutoff", BEST_CUTOFF)
    main_rows = experiment_main()
    quad_rows = experiment_quadratic()
    plot_cutoff(cut_rows)
    plot_main(main_rows)
    plot_quadratic(quad_rows, main_rows)
    with open(f"{OUT}/environment.txt", "w") as f:
        f.write(f"Python {platform.python_version()} on {platform.system()} {platform.machine()}\n")
        f.write(f"best cutoff {BEST_CUTOFF}\n")
