"""
Part C: timing experiments.   Run with:   python benchmark.py

1. Times both functions for n = 1,000, 2,000, 4,000, ..., 64,000.
   Brute force runs in a separate process and is stopped after 60 seconds;
   once it times out, larger n are skipped.
2. Finds the crossover: the smallest n where divide and conquer is faster.
3. Writes timings.csv, crossover.csv and timing_loglog.png.
"""

import csv
import multiprocessing as mp
import platform
import random
import statistics
import time
import timeit

from closest import closest_pair, closest_pair_brute

LIMIT = 60.0          # seconds allowed for one brute-force run
GRID = 1_000_000      # map grid size (coordinates 0..GRID)


def make_points(n, seed):
    rng = random.Random(seed)
    return [(rng.randint(0, GRID), rng.randint(0, GRID)) for _ in range(n)]


def _brute_worker(n, seed, q):
    pts = make_points(n, seed)
    t0 = time.perf_counter()
    res = closest_pair_brute(pts)
    q.put((time.perf_counter() - t0, res[0]))


def time_brute(n, seed):
    """Return (seconds, distance) or (None, None) if it ran past LIMIT."""
    q = mp.Queue()
    p = mp.Process(target=_brute_worker, args=(n, seed, q))
    p.start()
    p.join(LIMIT + 5)          # +5 s for process start-up and point generation
    if p.is_alive():
        p.terminate(); p.join()
        return None, None
    t, d = q.get()
    return (t, d) if t <= LIMIT else (None, None)


def time_dc(n, seed, repeats=5):
    pts = make_points(n, seed)
    times = []
    for _ in range(repeats):
        t0 = time.perf_counter()
        res = closest_pair(pts)
        times.append(time.perf_counter() - t0)
    return min(times), res[0]


def main_timing():
    sizes = [1000 * 2 ** k for k in range(7)]          # 1,000 .. 64,000
    rows, brute_alive = [], True
    for n in sizes:
        seed = n
        t_dc, d_dc = time_dc(n, seed)
        if brute_alive:
            t_bf, d_bf = time_brute(n, seed)
            if t_bf is None:
                brute_alive = False
            else:
                assert d_bf == d_dc, "results disagree at n=%d" % n
        else:
            t_bf = None
        rows.append((n, t_bf, t_dc))
        print("n=%6d  brute=%s  d&c=%.4f s" %
              (n, "%.3f s" % t_bf if t_bf else "> 60 s (stopped)", t_dc), flush=True)
    with open("timings.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "brute_seconds", "dc_seconds"])
        for n, tb, td in rows:
            w.writerow([n, "" if tb is None else "%.6f" % tb, "%.6f" % td])
    return rows


def median_time(func, pts, number):
    return statistics.median(timeit.repeat(lambda: func(pts), number=number,
                                           repeat=7)) / number


def main_crossover():
    rows = []
    for n in list(range(2, 41)) + list(range(45, 151, 5)):
        tb, td = [], []
        for s in range(5):                          # 5 different random inputs
            pts = make_points(n, 1000 + 31 * n + s)
            number = max(20, 20000 // (n * n))
            tb.append(median_time(closest_pair_brute, pts, number))
            td.append(median_time(closest_pair, pts, number))
        rows.append((n, statistics.median(tb), statistics.median(td)))
    with open("crossover.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "brute_us", "dc_us"])
        for n, b, d in rows:
            w.writerow([n, "%.3f" % (b * 1e6), "%.3f" % (d * 1e6)])
    # crossover: smallest n from which d&c is faster for every larger n tested
    cross = None
    for k in range(len(rows)):
        if all(r[2] < r[1] for r in rows[k:]):
            cross = rows[k][0]
            break
    first = next((r[0] for r in rows if r[2] < r[1]), None)
    print("first n where d&c faster:", first, "| faster from then on:", cross)
    return rows, first, cross


def plot(rows, cross_rows, cross=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (ax, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))
    n_bf = [r[0] for r in rows if r[1] is not None]
    t_bf = [r[1] for r in rows if r[1] is not None]
    n_dc = [r[0] for r in rows]
    t_dc = [r[2] for r in rows]
    ax.loglog(n_bf, t_bf, "o-", color="#c0392b", label="Brute force (measured)")
    ax.loglog(n_dc, t_dc, "s-", color="#1f6fb2", label="Divide & conquer (measured)")
    # reference slopes anchored at the first point
    import math
    ref = [t_bf[0] * (n / n_bf[0]) ** 2 for n in n_dc]
    ax.loglog(n_dc, ref, ":", color="#c0392b", alpha=.6, label=r"$c\,n^2$ reference")
    ref2 = [t_dc[0] * (n * math.log2(n)) / (n_dc[0] * math.log2(n_dc[0])) for n in n_dc]
    ax.loglog(n_dc, ref2, ":", color="#1f6fb2", alpha=.6, label=r"$c\,n\log n$ reference")
    ax.axhline(LIMIT, color="grey", lw=.8, ls="--")
    ax.text(n_dc[0], LIMIT * 1.15, "60 s cut-off", color="grey", fontsize=8)
    ax.set_xlabel("number of camera traps n (log scale)")
    ax.set_ylabel("running time, seconds (log scale)")
    ax.set_title("Figure 1. Running time vs n (log-log)")
    ax.grid(True, which="both", alpha=.25)
    ax.legend(fontsize=8)

    cross_rows = [r for r in cross_rows if r[0] <= 60]     # zoom on small n
    ns = [r[0] for r in cross_rows]
    ax2.plot(ns, [r[1] * 1e6 for r in cross_rows], "o-", ms=3, color="#c0392b",
             label="Brute force")
    ax2.plot(ns, [r[2] * 1e6 for r in cross_rows], "s-", ms=3, color="#1f6fb2",
             label="Divide & conquer")
    if cross:
        ax2.axvline(cross, color="grey", lw=.8, ls="--")
        ax2.text(cross + 1, max(r[1] for r in cross_rows) * 1e6 * 0.9,
                 "D&C always faster\nfrom n = %d" % cross, fontsize=8, color="grey")
    ax2.set_xlabel("number of camera traps n")
    ax2.set_ylabel("running time, microseconds")
    ax2.set_title("Figure 2. Small n: finding the crossover")
    ax2.grid(True, alpha=.25)
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig("timing_loglog.png", dpi=200)


def plot_from_csv():
    """Redraw the graph from timings.csv / crossover.csv without re-timing."""
    with open("timings.csv") as f:
        rows = [(int(r["n"]), float(r["brute_seconds"]) if r["brute_seconds"] else None,
                 float(r["dc_seconds"])) for r in csv.DictReader(f)]
    with open("crossover.csv") as f:
        cr = [(int(r["n"]), float(r["brute_us"]) / 1e6, float(r["dc_us"]) / 1e6)
              for r in csv.DictReader(f)]
    cross = next(cr[k][0] for k in range(len(cr)) if all(r[2] < r[1] for r in cr[k:]))
    plot(rows, cr, cross)


if __name__ == "__main__":
    import sys
    if "--plot-only" in sys.argv:
        plot_from_csv()
        sys.exit()
    print(platform.platform(), "| Python", platform.python_version(),
          "|", platform.processor() or platform.machine())
    rows = main_timing()
    cross_rows, first, cross = main_crossover()
    plot(rows, cross_rows, cross)

