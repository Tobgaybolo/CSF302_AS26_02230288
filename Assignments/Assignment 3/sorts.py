"""
sorts.py - Assignment 3: Fixing a Slow Quicksort (Unit 5, Sorting)

Two in-place quicksorts for lists of integers:

    quicksort_basic(a)              textbook quicksort, Lomuto partition,
                                    last element as pivot
    quicksort_improved(a, cutoff)   random pivot + 3-way partition +
                                    insertion sort for small parts +
                                    recurse-on-smaller / loop-on-larger
                                    (recursion depth O(log n))

Neither function uses sorted() or list.sort().
"""

import random


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _lomuto_partition(a, lo, hi):
    """Partition a[lo..hi] around the pivot a[hi] (Lomuto scheme).

    After the call, every element of a[lo..p-1] is <= pivot, a[p] is the
    pivot, and every element of a[p+1..hi] is > pivot. Returns p.
    Cost: exactly hi - lo comparisons, i.e. Theta(n) for a part of size n.
    """
    pivot = a[hi]
    i = lo - 1
    for j in range(lo, hi):
        if a[j] <= pivot:
            i += 1
            a[i], a[j] = a[j], a[i]
    a[i + 1], a[hi] = a[hi], a[i + 1]
    return i + 1


def insertion_sort(a, lo=0, hi=None):
    """Sort a[lo..hi] (inclusive) in place with insertion sort."""
    if hi is None:
        hi = len(a) - 1
    for i in range(lo + 1, hi + 1):
        key = a[i]
        j = i - 1
        while j >= lo and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key


# ---------------------------------------------------------------------------
# Part A (1): basic quicksort
# ---------------------------------------------------------------------------

def quicksort_basic(a):
    """Sort list a in place. Lomuto partition, last element as pivot.

    Average case Theta(n log n) on random data, but Theta(n^2) time and
    Theta(n) recursion depth on sorted input or input with many repeats,
    which raises RecursionError for large n.
    """
    _quicksort_basic(a, 0, len(a) - 1)


def _quicksort_basic(a, lo, hi):
    if lo < hi:
        p = _lomuto_partition(a, lo, hi)
        _quicksort_basic(a, lo, p - 1)
        _quicksort_basic(a, p + 1, hi)


# ---------------------------------------------------------------------------
# Part A (2): improved quicksort
# ---------------------------------------------------------------------------

def _three_way_partition(a, lo, hi):
    """Partition a[lo..hi] around a random pivot into three bands
    (Dijkstra's "Dutch national flag"):

        a[lo..lt-1] < pivot,  a[lt..gt] == pivot,  a[gt+1..hi] > pivot

    Returns (lt, gt). All copies of the pivot are put in their final place
    at once, so a part made only of equal keys is finished in ONE pass
    instead of n passes. Cost: Theta(n) for a part of size n.
    """
    r = random.randint(lo, hi)
    pivot = a[r]
    lt, i, gt = lo, lo, hi
    while i <= gt:
        x = a[i]
        if x < pivot:
            a[lt], a[i] = x, a[lt]
            lt += 1
            i += 1
        elif x > pivot:
            a[gt], a[i] = x, a[gt]
            gt -= 1
        else:
            i += 1
    return lt, gt


def quicksort_improved(a, cutoff=16):
    """Sort list a in place.

    Improvements over quicksort_basic:
      1. Random pivot - expected Theta(n log n) for EVERY input order, so
         already-sorted input is no longer a bad case.
      2. Three-way partition - equal keys (e.g. many Nu 100 / Nu 500
         top-ups) are grouped round the pivot and never touched again.
      3. Parts of size <= cutoff are finished with insertion sort, which
         has much lower overhead than recursion on tiny parts.
      4. Recurse on the smaller part, loop on the larger part. The smaller
         part has at most half the elements, so the recursion depth is at
         most log2(n) whatever pivots are chosen.
    """
    if cutoff < 1:
        cutoff = 1
    _quicksort_improved(a, 0, len(a) - 1, cutoff)


def _quicksort_improved(a, lo, hi, cutoff):
    while hi - lo + 1 > cutoff:
        lt, gt = _three_way_partition(a, lo, hi)
        # recurse on the smaller part, loop on the larger part
        if lt - lo < hi - gt:
            _quicksort_improved(a, lo, lt - 1, cutoff)
            lo = gt + 1
        else:
            _quicksort_improved(a, gt + 1, hi, cutoff)
            hi = lt - 1
    insertion_sort(a, lo, hi)


# ---------------------------------------------------------------------------
# Comparison variant (for the report only): the three listed improvements
# but keeping the 2-way Lomuto partition. Shows why 3-way partitioning is
# needed for many duplicates.
# ---------------------------------------------------------------------------

def quicksort_random_lomuto(a, cutoff=16):
    """Random pivot + insertion-sort cutoff + smaller-side recursion,
    but with Lomuto (2-way) partitioning."""
    if cutoff < 1:
        cutoff = 1
    _qs_rl(a, 0, len(a) - 1, cutoff)


def _qs_rl(a, lo, hi, cutoff):
    while hi - lo + 1 > cutoff:
        r = random.randint(lo, hi)
        a[r], a[hi] = a[hi], a[r]
        p = _lomuto_partition(a, lo, hi)
        if p - lo < hi - p:
            _qs_rl(a, lo, p - 1, cutoff)
            lo = p + 1
        else:
            _qs_rl(a, p + 1, hi, cutoff)
            hi = p - 1
    insertion_sort(a, lo, hi)


# ---------------------------------------------------------------------------
# Depth-measuring versions (used only by the report, to show the depth)
# ---------------------------------------------------------------------------

def max_depth_basic(a):
    """Return the maximum recursion depth quicksort_basic reaches on a copy
    of a, simulated with an explicit stack (so it never crashes)."""
    a = list(a)
    best = 0
    stack = [(0, len(a) - 1, 1)]
    while stack:
        lo, hi, d = stack.pop()
        if lo < hi:
            best = max(best, d)
            p = _lomuto_partition(a, lo, hi)
            stack.append((lo, p - 1, d + 1))
            stack.append((p + 1, hi, d + 1))
    return best


def max_depth_improved(a, cutoff=16):
    """Return the maximum recursion depth quicksort_improved reaches."""
    a = list(a)
    best = [0]

    def rec(lo, hi, d):
        best[0] = max(best[0], d)
        while hi - lo + 1 > cutoff:
            lt, gt = _three_way_partition(a, lo, hi)
            if lt - lo < hi - gt:
                rec(lo, lt - 1, d + 1)
                lo = gt + 1
            else:
                rec(gt + 1, hi, d + 1)
                hi = lt - 1

    rec(0, len(a) - 1, 1)
    return best[0]
