"""
CSF302 Lab 5 - Q3: Counting Inversions

An inversion is a pair of positions (i, j) with i < j and a[i] > a[j].

  1. Brute force: check every pair                       Theta(n^2)
  2. Merge-sort-based count                              Theta(n log n)
  3. Verify both agree on random arrays of size up to 2,000
  4. Time both for n = 1,000 ... 1,000,000; brute force is stopped as soon
     as one run exceeds 60 seconds, and is not run for larger n
  5. Kendall tau distance between two users' rankings of 10 movies,
     entered from the keyboard

Method: time.perf_counter(), inputs generated outside the timed region
(fixed seed 42), median of 3 runs. Exception: a brute-force run longer than
10 s is measured once (a single run of that length is already stable, and
3 runs would take minutes).

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q3_inversions.py              menu: verify / timing / Kendall tau
      python q3_inversions.py verify
      python q3_inversions.py timing        (about 3-4 minutes)
      python q3_inversions.py kendall       (asks for two rankings)
"""
import csv
import random
import statistics
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from timing_utils import markdown_table

TIME_LIMIT = 60.0


# ---------------------------------------------------------------------------
# 1. Brute force
# ---------------------------------------------------------------------------
def count_inversions_brute(a, time_limit=None):
    """Check every pair (i, j), i < j. Theta(n^2).
    If time_limit (seconds) is given, raise TimeoutError once it is exceeded."""
    n = len(a)
    count = 0
    start = time.perf_counter()
    for i in range(n):
        ai = a[i]
        for j in range(i + 1, n):
            if ai > a[j]:
                count += 1
        if time_limit is not None and time.perf_counter() - start > time_limit:
            raise TimeoutError(f"brute force passed {time_limit} s at i = {i} of {n}")
    return count


def inversion_pairs_brute(a):
    """List every inversion (i, j). Used for small inputs (Kendall tau)."""
    return [(i, j) for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j]]


# ---------------------------------------------------------------------------
# 2. Merge-sort-based count
# ---------------------------------------------------------------------------
def _sort_count(a):
    """Return (sorted copy of a, number of inversions in a)."""
    n = len(a)
    if n <= 1:
        return list(a), 0
    mid = n // 2
    left, inv_left = _sort_count(a[:mid])
    right, inv_right = _sort_count(a[mid:])
    merged = []
    i = j = 0
    split = 0
    nl, nr = len(left), len(right)
    while i < nl and j < nr:
        if left[i] <= right[j]:            # <= : equal values are NOT inversions
            merged.append(left[i])
            i += 1
        else:
            # right[j] is smaller than left[i] and therefore smaller than all of
            # left[i:], which all come before it: nl - i split inversions at once
            merged.append(right[j])
            split += nl - i
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged, inv_left + inv_right + split


def count_inversions_merge(a):
    """Number of inversions using merge sort. Theta(n log n). a is not modified."""
    return _sort_count(a)[1]


# ---------------------------------------------------------------------------
# 3. Verification
# ---------------------------------------------------------------------------
def verify(trials=300, seed=42):
    rng = random.Random(seed)
    fixed = [[], [1], [1, 2], [2, 1], [3, 3, 3], [1, 2, 3, 4, 5], [5, 4, 3, 2, 1],
             [2, 4, 1, 3, 5], list(range(2000, 0, -1))]
    for a in fixed:
        assert count_inversions_brute(a) == count_inversions_merge(a), a
    sizes = [rng.randint(0, 2000) for _ in range(trials)] + [2000] * 5
    for n in sizes:
        hi = rng.choice([5, 100, 10**6])              # include many-duplicate arrays
        a = [rng.randint(0, hi) for _ in range(n)]
        assert count_inversions_brute(a) == count_inversions_merge(a)
    print(f"Brute force and merge-based counts agree on {len(fixed) + len(sizes)} arrays "
          f"(sizes 0..2000, with and without duplicates).")
    print(f"Example: [2, 4, 1, 3, 5] has {count_inversions_merge([2, 4, 1, 3, 5])} inversions "
          f"{inversion_pairs_brute([2, 4, 1, 3, 5])} (index pairs)")
    print(f"Reverse-sorted n = 2000: {count_inversions_merge(list(range(2000, 0, -1))):,} "
          f"= 2000*1999/2 = {2000 * 1999 // 2:,}")


# ---------------------------------------------------------------------------
# 4. Timing
# ---------------------------------------------------------------------------
SIZES = [1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000]


def timing():
    rng = random.Random(42)
    rows = []
    brute_stopped = False
    for n in SIZES:
        data = [rng.randint(0, 10**9) for _ in range(n)]      # outside the timer

        samples = []
        for _ in range(3):
            start = time.perf_counter()
            inv = count_inversions_merge(data)
            samples.append(time.perf_counter() - start)
        t_merge = statistics.median(samples)

        t_brute, note = None, ""
        if brute_stopped:
            note = "skipped (a smaller n already exceeded 60 s)"
        else:
            try:
                start = time.perf_counter()
                inv_b = count_inversions_brute(data, time_limit=TIME_LIMIT)
                first = time.perf_counter() - start
                assert inv_b == inv
                if first > 10:
                    t_brute, note = first, "1 run"
                else:
                    more = [first]
                    for _ in range(2):
                        start = time.perf_counter()
                        count_inversions_brute(data)
                        more.append(time.perf_counter() - start)
                    t_brute = statistics.median(more)
            except TimeoutError:
                brute_stopped = True
                note = f"stopped: exceeded {TIME_LIMIT:.0f} s"
        rows.append((n, inv, t_brute, t_merge, note))
        bs = f"{t_brute:.4f}s" if t_brute is not None else note
        print(f"n={n:>9,}  inversions={inv:>15,}  brute={bs:<35} merge={t_merge:.4f}s", flush=True)

    with open("../results/q3_timing.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["n", "inversions", "brute_s", "merge_s", "note"])
        w.writerows(rows)
    table = markdown_table(
        ["n", "inversions", "brute force (s)", "merge-based (s)", "note"],
        [(f"{n:,}", f"{inv:,}", f"{tb:.4f}" if tb is not None else "—", f"{tm:.4f}", note)
         for n, inv, tb, tm, note in rows])
    with open("../results/q3_timing.md", "w") as f:
        f.write("# Q3 - inversion counting timing (seed 42)\n\n" + table + "\n")

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    bx = [r for r in rows if r[2] is not None]
    ax.loglog([r[0] for r in bx], [r[2] for r in bx], "o-", label="brute force  Θ(n²)")
    ax.loglog([r[0] for r in rows], [r[3] for r in rows], "s-", label="merge-based  Θ(n log n)")
    ax.axhline(TIME_LIMIT, color="grey", ls=":", label="60 s limit")
    ax.set_xlabel("n")
    ax.set_ylabel("time (s)")
    ax.set_title("Counting inversions (log-log)")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("../results/q3_timing.png", dpi=140)
    print("\nSaved ../results/q3_timing.{csv,md,png}")


# ---------------------------------------------------------------------------
# 5. Kendall tau distance from keyboard input
# ---------------------------------------------------------------------------
DEFAULT_MOVIES = ["Inception", "Interstellar", "The Matrix", "Parasite", "Spirited Away",
                  "The Godfather", "Titanic", "Avatar", "Coco", "Up"]


def kendall_tau_distance(rank1, rank2):
    """Number of movie pairs that the two users order differently.

    rank1, rank2: lists of the same 10 items, best first.
    Relabel each movie by its position in rank1; then rank2 becomes a
    permutation, and each pair the users disagree on is exactly one
    inversion of that permutation. Theta(n log n) via merge-based counting.
    """
    if sorted(rank1) != sorted(rank2) or len(set(rank1)) != len(rank1):
        raise ValueError("both rankings must contain the same distinct items")
    pos = {item: i for i, item in enumerate(rank1)}
    return count_inversions_merge([pos[item] for item in rank2])


def read_ranking(user, movies):
    n = len(movies)
    while True:
        raw = input(f"\n{user}: enter the {n} movie numbers from favourite to least favourite\n"
                    f"(space or comma separated): ")
        parts = raw.replace(",", " ").split()
        try:
            nums = [int(p) for p in parts]
        except ValueError:
            print("  Please enter whole numbers only.")
            continue
        if sorted(nums) != list(range(1, n + 1)):
            print(f"  Each number 1..{n} must appear exactly once (you gave {len(nums)} numbers).")
            continue
        return [movies[x - 1] for x in nums]


def kendall_interactive():
    print("Kendall tau distance between two users' movie rankings")
    raw = input("Press Enter to use the default 10 movies, or type 10 titles separated by commas:\n> ")
    movies = [t.strip() for t in raw.split(",") if t.strip()] if raw.strip() else DEFAULT_MOVIES
    if len(movies) != 10 or len(set(movies)) != 10:
        print("Need exactly 10 distinct titles; using the default list.")
        movies = DEFAULT_MOVIES
    for i, m in enumerate(movies, 1):
        print(f"  {i:>2}. {m}")
    r1 = read_ranking("User 1", movies)
    r2 = read_ranking("User 2", movies)
    report(r1, r2)


def report(r1, r2):
    n = len(r1)
    total = n * (n - 1) // 2
    d = kendall_tau_distance(r1, r2)
    pos = {m: i for i, m in enumerate(r1)}
    perm = [pos[m] for m in r2]
    assert d == count_inversions_brute(perm)                 # cross-check
    print("\n  Rank | User 1             | User 2")
    for i in range(n):
        print(f"  {i + 1:>4} | {r1[i]:<18} | {r2[i]}")
    print(f"\nKendall tau distance       = {d} disagreeing pairs out of {total}")
    print(f"Normalised distance        = {d / total:.3f}   (0 = identical, 1 = reversed)")
    print(f"Similarity (1 - d/{total})      = {1 - d / total:.3f}")
    print(f"Kendall tau coefficient    = {1 - 2 * d / total:+.3f}   (+1 agree, -1 opposite)")
    if 0 < d <= 12:
        print("Disagreeing pairs:")
        for i, j in inversion_pairs_brute(perm):
            a, b = r1[perm[i]], r1[perm[j]]
            print(f"  User 1 prefers {b!r} over {a!r}, User 2 prefers {a!r} over {b!r}")


def menu():
    while True:
        print("\n--- Q3 Counting Inversions ---")
        print("1. Verify brute force vs merge-based")
        print("2. Timing experiment (n = 1,000 .. 1,000,000)")
        print("3. Kendall tau distance between two movie rankings")
        print("0. Exit")
        ch = input("Choice: ").strip()
        if ch == "1":
            verify()
        elif ch == "2":
            timing()
        elif ch == "3":
            kendall_interactive()
        elif ch == "0":
            break


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    {"verify": verify, "timing": timing, "kendall": kendall_interactive}.get(cmd, menu)()

# ---------------------------------------------------------------------------
# Analysis / conclusion  (one run on my machine; exact times will differ, but the trends should match)
#
# | n         | inversions      | brute force (s)        | merge-based (s) |
# |-----------|-----------------|------------------------|-----------------|
# | 1,000     | 243,362         | 0.0225                 | 0.0011          |
# | 2,000     | 1,005,397       | 0.0902                 | 0.0032          |
# | 5,000     | 6,195,597       | 0.5924                 | 0.0084          |
# | 10,000    | 25,151,963      | 2.1102                 | 0.0190          |
# | 20,000    | 100,683,842     | 8.0908                 | 0.0313          |
# | 50,000    | 625,213,658     | 53.6768 (1 run)        | 0.1291          |
# | 100,000   | 2,502,994,930   | stopped: > 60 s        | 0.2557          |
# | 200,000   | 10,001,098,705  | skipped                | 0.4945          |
# | 500,000   | 62,467,515,644  | skipped                | 1.4579          |
# | 1,000,000 | 249,971,295,182 | skipped                | 3.2192          |
#
# Correctness: both methods gave identical counts on 314 arrays (sizes up to
# 2,000, including many-duplicate and reverse-sorted arrays), and on every
# timed array where brute force finished.
#
# Brute force: doubling n multiplies the time by ~4 (2.11 s -> 8.09 s for
# 10k -> 20k), and 2.5x n gives ~6.6x time (20k -> 50k), close to
# 2.5^2 = 6.25. That is Theta(n^2), slope 2 on the log-log plot. Extending
# the trend gives ~215 s for n = 100,000 and ~6 hours for n = 10^6, so it
# was stopped at the 60 s limit.
# Merge-based: doubling n roughly doubles the time (slightly more, because
# of the log n factor): Theta(n log n). It counts 2.5 * 10^11 inversions
# for n = 10^6 in about 3 s, because each merge step adds (nl - i)
# inversions at once instead of finding them one by one.
#
# Sanity check: a random array has on average n(n-1)/4 inversions (each
# pair is inverted with probability 1/2). For n = 10^6 that is 2.49999 *
# 10^11, and 2.4997 * 10^11 was measured.
#
# Kendall tau: relabel movies by their position in user 1's list; user 2's
# list becomes a permutation, and each pair the users order differently is
# one inversion. Distance 0 means identical rankings and 45 = C(10, 2) means
# fully reversed. Similarity = 1 - d/45, Kendall tau coefficient =
# 1 - 2d/45. Example: rankings 3 1 2 4 5 6 7 8 9 10 and
# 1 2 3 4 5 6 7 8 10 9 give d = 3, similarity 0.933.
# ---------------------------------------------------------------------------
