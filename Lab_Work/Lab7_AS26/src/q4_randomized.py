"""
CSF302 Lab 7 - Q4: Randomized Algorithms

  1. Randomized quickselect for the k-th smallest element, compared with
     "sort and index" for n = 10^4 .. 10^6. Two sorts are compared: the
     merge sort from Lab 1 (same language, so a fair algorithm comparison)
     and Python's built-in sorted() (C code, as a practical reference).
  2. Miller-Rabin vs trial division (up to sqrt n) on 20 random 12-digit
     numbers; the two must agree
  3. Miller-Rabin with 1 round on the Carmichael number 561, 1,000 times:
     how often does it answer "prime"?

Modular exponentiation is our own square-and-multiply from Lab 4 (pow() is
used only as a checker).

Method: time.perf_counter(), inputs generated outside the timed region
(fixed seed 42), median of 3 runs.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q4_randomized.py        (about 1 minute)
"""
import math
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from timing_utils import markdown_table, time_call


# ---------------------------------------------------------------------------
# 1. Randomized quickselect
# ---------------------------------------------------------------------------
def quickselect(a, k, rng=random):
    """Return the k-th smallest element of a (k = 1..n). Works on a copy.
    Iterative, in-place three-way partition around a random pivot, then keep
    only the part that contains position k-1. Expected Theta(n): the
    expected sizes shrink geometrically (n + 3n/4 + ... = O(n)).
    Worst case Theta(n^2) if pivots are always bad (very unlikely)."""
    if not 1 <= k <= len(a):
        raise ValueError(f"k must be in 1..{len(a)}")
    a = list(a)
    lo, hi, target = 0, len(a) - 1, k - 1
    while True:
        if lo == hi:
            return a[lo]
        pivot = a[rng.randint(lo, hi)]
        lt, i, gt = lo, lo, hi                       # Dutch national flag
        while i <= gt:
            x = a[i]
            if x < pivot:
                a[lt], a[i] = x, a[lt]
                lt += 1
                i += 1
            elif x > pivot:
                a[i], a[gt] = a[gt], x
                gt -= 1
            else:
                i += 1
        if target < lt:
            hi = lt - 1
        elif target > gt:
            lo = gt + 1
        else:
            return pivot


def merge_sort(arr):
    """Lab 1 merge sort (top-down, stable)."""
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def select_by_merge_sort(a, k):
    return merge_sort(a)[k - 1]


def select_by_builtin_sort(a, k):
    return sorted(a)[k - 1]


def part1():
    rng = random.Random(42)
    for _ in range(500):                              # correctness first
        a = [rng.randint(0, 20) for _ in range(rng.randint(1, 60))]
        k = rng.randint(1, len(a))
        assert quickselect(a, k, rng) == sorted(a)[k - 1]
    print("quickselect == sorted(a)[k-1] on 500 random arrays (with duplicates).")

    rows = []
    for n in [10_000, 30_000, 100_000, 300_000, 1_000_000]:
        a = [rng.randint(0, 10**9) for _ in range(n)]
        k = n // 2                                       # the median: hardest k
        tq, vq = time_call(quickselect, a, k, rng)
        tm, vm = time_call(select_by_merge_sort, a, k)
        tb, vb = time_call(select_by_builtin_sort, a, k)
        assert vq == vm == vb
        rows.append((n, tq, tm, tb))
        print(f"n={n:>9,}  quickselect={tq:.4f}s  merge sort+index={tm:.4f}s "
              f"({tm / tq:.1f}x)  sorted()+index={tb:.4f}s", flush=True)

    table = markdown_table(["n", "quickselect (s)", "merge sort + index (s)",
                            "speed-up vs merge sort", "built-in sorted() + index (s)"],
                           [(f"{n:,}", f"{q:.4f}", f"{m:.4f}", f"{m / q:.1f}x", f"{b:.4f}")
                            for n, q, m, b in rows])
    with open("../results/q4_quickselect.md", "w") as f:
        f.write("# Q4.1 - quickselect vs sort+index, k = n/2 (median of 3, seed 42)\n\n"
                + table + "\n")
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ns = [r[0] for r in rows]
    ax.loglog(ns, [r[1] for r in rows], "o-", label="randomized quickselect  E[Θ(n)]")
    ax.loglog(ns, [r[2] for r in rows], "s-", label="merge sort + index  Θ(n log n)")
    ax.loglog(ns, [r[3] for r in rows], "^--", label="built-in sorted() + index (C code)")
    ax.set_xlabel("n")
    ax.set_ylabel("time (s)")
    ax.set_title("k-th smallest (k = n/2), log-log")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig("../results/q4_quickselect.png", dpi=140)
    print("Saved ../results/q4_quickselect.{md,png}")


# ---------------------------------------------------------------------------
# 2. Miller-Rabin vs trial division
# ---------------------------------------------------------------------------
def mod_pow(a, b, m):
    """Square-and-multiply from Lab 4."""
    result, a = 1 % m, a % m
    while b:
        if b & 1:
            result = result * a % m
        a = a * a % m
        b >>= 1
    return result


def miller_rabin(n, rounds=20, rng=random):
    """Probabilistic primality test. Write n-1 = 2^s * d with d odd. For a
    random base a, n passes if a^d = 1 or a^(d*2^r) = -1 (mod n) for some
    0 <= r < s. A prime always passes. For a composite, at most 1/4 of
    bases pass, so error <= 4^-rounds. Each round costs O(log n)
    multiplications."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0:
        return False
    # No trial division by small primes here on purpose: Q4.3 must test the
    # Miller-Rabin rounds themselves (561 = 3 * 187 would otherwise be caught
    # by "divisible by 3" before any round runs).
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = rng.randint(2, n - 2)
        if not strong_probable_prime(n, a, d, s):
            return False                  # a is a witness: definitely composite
    return True                           # probably prime


def strong_probable_prime(n, a, d=None, s=None):
    """One Miller-Rabin round with base a."""
    if d is None:
        d, s = n - 1, 0
        while d % 2 == 0:
            d //= 2
            s += 1
    x = mod_pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False


def trial_division(n):
    """Deterministic: try 2, then odd divisors up to floor(sqrt n).
    Theta(sqrt n) for a prime: ~500,000 divisions for a 12-digit prime."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    limit = math.isqrt(n)
    f = 3
    while f <= limit:
        if n % f == 0:
            return False
        f += 2
    return True


def part2():
    rng = random.Random(42)
    numbers = [rng.randint(10**11, 10**12 - 1) for _ in range(20)]
    rows = []
    total_mr = total_td = 0.0
    for n in numbers:
        t_mr, r_mr = time_call(miller_rabin, n, 20, rng)
        t_td, r_td = time_call(trial_division, n)
        assert r_mr == r_td, f"disagree on {n}"
        total_mr += t_mr
        total_td += t_td
        rows.append((f"{n:,}", "prime" if r_td else "composite", "prime" if r_mr else "composite",
                     f"{t_mr * 1e6:.1f}", f"{t_td * 1e6:,.1f}"))
    print(markdown_table(["n (12 digits)", "trial division", "Miller-Rabin (20 rounds)",
                          "MR time (us)", "trial time (us)"], rows))
    n_primes = sum(r[1] == "prime" for r in rows)
    print(f"\nBoth methods agree on all 20 numbers ({n_primes} prime). "
          f"Total time: Miller-Rabin {total_mr * 1000:.2f} ms, trial division {total_td * 1000:.2f} ms")

    # Random 12-digit numbers are mostly composite with small factors, so add
    # the hard case for trial division: 12-digit primes (found with MR, then
    # confirmed by trial division).
    primes = []
    while len(primes) < 5:
        c = rng.randint(10**11, 10**12 - 1) | 1
        if miller_rabin(c, 20, rng):
            primes.append(c)
    prows = []
    for p in primes:
        t_mr, r_mr = time_call(miller_rabin, p, 20, rng)
        t_td, r_td = time_call(trial_division, p)
        assert r_mr and r_td
        prows.append((f"{p:,}", f"{t_mr * 1e6:.1f}", f"{t_td * 1e3:.1f}", f"{t_td / t_mr:,.0f}x"))
    ptable = markdown_table(["12-digit prime", "Miller-Rabin (us)", "trial division (ms)",
                             "trial / MR"], prows)
    print("\nExtra: worst case for trial division, 5 random 12-digit primes")
    print(ptable)
    with open("../results/q4_primality.md", "w") as f:
        f.write("# Q4.2 - Miller-Rabin vs trial division (seed 42)\n\n## 20 random 12-digit numbers\n\n"
                + markdown_table(["n", "trial division", "Miller-Rabin", "MR (us)", "trial (us)"], rows)
                + "\n\n## Extra: 12-digit primes (worst case for trial division)\n\n" + ptable + "\n")


# ---------------------------------------------------------------------------
# 3. Carmichael number 561 = 3 * 11 * 17
# ---------------------------------------------------------------------------
def part3(trials=1000):
    n = 561
    rng = random.Random(42)
    says_prime = sum(miller_rabin(n, rounds=1, rng=rng) for _ in range(trials))
    print(f"Miller-Rabin, 1 round, on 561 x {trials}: answered 'prime' {says_prime} times "
          f"({says_prime / trials:.1%}), 'composite' {trials - says_prime} times")

    bases = range(2, n - 1)                              # the bases MR draws from
    liars = [a for a in bases if strong_probable_prime(n, a)]
    fermat_liars = [a for a in bases if mod_pow(a, n - 1, n) == 1]
    print(f"Exact: strong liars for 561 among a = 2..559: {liars}")
    print(f"  -> {len(liars)}/{len(bases)} = {len(liars) / len(bases):.2%} chance per round "
          f"(theory bound: at most 25%)")
    print(f"For comparison, the Fermat test a^(n-1) = 1 is fooled by {len(fermat_liars)}/"
          f"{len(bases)} = {len(fermat_liars) / len(bases):.1%} of bases "
          f"(every base coprime to 561, because 561 is a Carmichael number)")
    print(f"Probability that k rounds all say 'prime': 1 round {len(liars) / len(bases):.4f}, "
          f"5 rounds {(len(liars) / len(bases)) ** 5:.2e}, "
          f"20 rounds {(len(liars) / len(bases)) ** 20:.2e}")
    assert all(mod_pow(a, n - 1, n) == pow(a, n - 1, n) for a in bases)
    with open("../results/q4_carmichael.txt", "w") as f:
        f.write(f"561, 1 round x {trials}: 'prime' {says_prime} times ({says_prime / trials:.1%})\n"
                f"strong liars: {liars} ({len(liars)}/{len(bases)})\n"
                f"Fermat liars: {len(fermat_liars)}/{len(bases)}\n")


def main():
    print("=== Q4.1 Randomized quickselect ===")
    part1()
    print("\n=== Q4.2 Miller-Rabin vs trial division ===")
    part2()
    print("\n=== Q4.3 Carmichael number 561 ===")
    part3()


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Analysis / conclusion  (times from one run on my machine; exact times will differ, but the trends should match)
#
# Q4.1 k-th smallest with k = n/2 (median of 3):
# | n         | quickselect | merge sort + index | speed-up | sorted() + index |
# |-----------|-------------|--------------------|----------|------------------|
# | 10,000    | 0.0027 s    | 0.0200 s           | 7.3x     | 0.0012 s         |
# | 30,000    | 0.0080 s    | 0.0533 s           | 6.6x     | 0.0055 s         |
# | 100,000   | 0.0233 s    | 0.2216 s           | 9.5x     | 0.0166 s         |
# | 300,000   | 0.0993 s    | 0.8681 s           | 8.7x     | 0.0550 s         |
# | 1,000,000 | 0.3660 s    | 3.1447 s           | 8.6x     | 0.3190 s         |
# - Quickselect recurses into only ONE side, so its expected work is
#   n + 3n/4 + (3/4)^2 n + ... = O(n), against Theta(n log n) for sorting.
#   Against our own merge sort (both pure Python) it is 6.6-9.5x faster.
#   From 10^4 to 10^5 its time grows ~9x for 10x more n (linear). From 10^5
#   to 10^6 it grows ~16x: at 10^6 elements the list no longer fits in the
#   CPU cache, and each run's random pivots add variance. Merge sort slows
#   down by a similar factor there, which is why the speed-up stays ~9x
#   instead of growing with log n.
# - Python's built-in sorted() is written in C (Timsort) and is about as fast
#   as, or faster than, pure-Python quickselect. This shows that constant
#   factors (C vs interpreted Python, ~20-50x) can outweigh the log n
#   advantage at these sizes. Compared like for like, the linear-time
#   selection wins.
#
# Q4.2 Miller-Rabin (20 rounds) vs trial division on 20 random 12-digit
# numbers: both agree on all 20 (3 primes, 17 composites). For composites
# trial division is often as fast or faster, because most random numbers
# have a small factor (2, 3, 5, ...) and it stops at once. For PRIMES trial
# division must try all odd numbers up to sqrt(n) ~ 10^6 (~500,000
# divisions, 19-37 ms), while Miller-Rabin needs 20 rounds x ~40 modular
# squarings (~0.25 ms). Over the 20 numbers: MR 0.88 ms total vs trial
# division 77 ms. On 5 extra 12-digit primes MR was 55-156x faster. Trial
# division is Theta(sqrt n) = Theta(2^(b/2)) for b-bit numbers (exponential
# in the number of digits), while MR is O(k b^3), polynomial. For the
# 300-digit numbers used in RSA only MR is usable.
#
# Q4.3 Carmichael number 561 = 3 x 11 x 17, Miller-Rabin with 1 round, 1,000
# runs: it answered "prime" 13 times (1.3%). Counting exactly: only 8 of the
# 558 possible bases (50, 101, 103, 256, 305, 458, 460, 511) are strong liars,
# 1.43% per round, so 13 is in line with the expected 14.3. This is far
# below the worst-case 1/4 bound. By contrast the plain Fermat test is fooled
# by 318/558 = 57% of bases, every base coprime to 561, which is what makes
# 561 a Carmichael number. MR catches it because 561 has a non-trivial
# square root of 1 that shows up in the squaring chain. With k rounds the
# chance of a wrong "prime" is (8/558)^k: 6e-10 for 5 rounds.
# Note: the function deliberately does no trial division by small primes
# before the rounds. Otherwise 561 (divisible by 3) would never reach them.
# ---------------------------------------------------------------------------
