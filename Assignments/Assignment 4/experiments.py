"""
Part C: analysis experiments for the report.

    python experiments.py

Prints the counterexamples, the revenue-ratio table for 1,000 random
inputs of 50 requests, running times, and saves ratio_histogram.png.
"""

import random
import statistics
import time
from itertools import product

from booking import (best_schedule, brute_force,
                     greedy_earliest_finish, greedy_highest_fee)

SEED = 2026
TRIALS = 1000
N = 50


def make_requests(rng, n, model):
    """Random day of bookings on a 0-100 time scale (one unit ~ 10 minutes).

    model = "independent": fee is unrelated to length (Nu 1,000-10,000).
    model = "by_length":   fee grows with length (Nu 500/unit) plus noise,
                           closer to how a real hall might charge.
    """
    reqs = []
    for _ in range(n):
        start = rng.randint(0, 90)
        length = rng.randint(2, 20)
        finish = min(100, start + length)
        if model == "independent":
            fee = rng.randint(10, 100) * 100
        else:
            fee = 500 * (finish - start) + rng.randint(0, 20) * 100
        reqs.append((start, finish, fee))
    return reqs


def ratio_experiment(model):
    rng = random.Random(SEED)
    ratios = {"earliest": [], "fee": []}
    hits = {"earliest": 0, "fee": 0}
    for _ in range(TRIALS):
        reqs = make_requests(rng, N, model)
        opt = best_schedule(reqs)[0]
        for name, func in (("earliest", greedy_earliest_finish),
                           ("fee", greedy_highest_fee)):
            r = func(reqs)[0] / opt
            ratios[name].append(r)
            hits[name] += r == 1.0
    return ratios, hits


def find_small_counterexamples():
    """Exhaustive search over tiny inputs for the smallest failures."""
    times = [(s, f) for s in range(0, 4) for f in range(s + 1, 5)]
    fees = [1, 2, 3]
    found = {}
    for n in (2, 3, 4):
        for combo in product(times, repeat=n):
            if n == 4 and found.get("both"):
                break
            for fs in product(fees, repeat=n):
                reqs = [(s, f, fee) for (s, f), fee in zip(combo, fs)]
                opt = brute_force(reqs)[0]
                ef = greedy_earliest_finish(reqs)[0] < opt
                hf = greedy_highest_fee(reqs)[0] < opt
                if ef and "earliest" not in found:
                    found["earliest"] = reqs
                if hf and "fee" not in found:
                    found["fee"] = reqs
                if ef and hf and "both" not in found:
                    found["both"] = reqs
                if len(found) == 3:
                    return found
    return found


def timing():
    rng = random.Random(1)
    rows = []
    for n in (10, 15):
        reqs = make_requests(rng, n, "independent")
        row = [n]
        for f in (greedy_earliest_finish, greedy_highest_fee, best_schedule, brute_force):
            t = time.perf_counter()
            for _ in range(3):
                f(reqs)
            row.append((time.perf_counter() - t) / 3 * 1000)
        rows.append(row)
    for n in (1000, 10000, 100000):
        reqs = make_requests(random.Random(n), n, "independent")
        row = [n]
        for f in (greedy_earliest_finish, greedy_highest_fee, best_schedule):
            t = time.perf_counter()
            f(reqs)
            row.append((time.perf_counter() - t) * 1000)
        row.append(None)
        rows.append(row)
    return rows


def summarise(ratios, hits):
    out = {}
    for name in ("earliest", "fee"):
        r = ratios[name]
        out[name] = dict(mean=statistics.mean(r), worst=min(r),
                         median=statistics.median(r), optimal=hits[name])
    return out


def plot(ratios, path="ratio_histogram.png"):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6.4, 2.9), dpi=200)
    bins = [0.40 + 0.02 * k for k in range(31)]
    ax.hist(ratios["earliest"], bins=bins, alpha=0.75, color="#2b6cb0",
            label="Earliest finish", edgecolor="white", linewidth=0.4)
    ax.hist(ratios["fee"], bins=bins, alpha=0.75, color="#dd6b20",
            label="Highest fee", edgecolor="white", linewidth=0.4)
    ax.set_xlabel("Greedy revenue / optimal revenue")
    ax.set_ylabel("Number of inputs")
    ax.set_title(f"Figure 1. Revenue ratio over {TRIALS} random inputs (n = {N})",
                 fontsize=10)
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(path)


if __name__ == "__main__":
    print("== Smallest counterexamples (exhaustive search) ==")
    for k, v in find_small_counterexamples().items():
        print(f"{k:9s}", v, "EF", greedy_earliest_finish(v),
              "HF", greedy_highest_fee(v), "OPT", best_schedule(v))

    for model in ("independent", "by_length"):
        ratios, hits = ratio_experiment(model)
        print(f"\n== Ratio table, fee model = {model} ==")
        for name, s in summarise(ratios, hits).items():
            print(f"{name:9s} mean {s['mean']:.4f}  median {s['median']:.4f}  "
                  f"worst {s['worst']:.4f}  optimal in {s['optimal']}/{TRIALS}")
        if model == "independent":
            plot(ratios)

    print("\n== Timing (ms): n, EF, HF, DP, BF ==")
    for row in timing():
        print(row)
