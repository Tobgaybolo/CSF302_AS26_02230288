"""
test_sorts.py - Part B tests for sorts.py

Run with:   python -m pytest -v test_sorts.py
   or:      python test_sorts.py

sorted() is used here ONLY as the trusted "brute-force" reference answer.
"""

import random
import sys

import pytest

from sorts import quicksort_basic, quicksort_improved, insertion_sort

# quicksort_improved is tested with several cutoffs, including 1 (no
# insertion sort at all) and a cutoff bigger than the list.
SORTS = {
    "basic": quicksort_basic,
    "improved_c1": lambda a: quicksort_improved(a, cutoff=1),
    "improved_c4": lambda a: quicksort_improved(a, cutoff=4),
    "improved_c16": lambda a: quicksort_improved(a),
    "improved_c64": lambda a: quicksort_improved(a, cutoff=64),
    "improved_c1000": lambda a: quicksort_improved(a, cutoff=1000),
}


def check(sort, data):
    """Sort a copy in place and compare with sorted(). Also check the
    function sorts IN PLACE (returns None, same list object)."""
    expected = sorted(data)
    a = list(data)
    ident = id(a)
    result = sort(a)
    assert result is None, "sort should work in place and return None"
    assert id(a) == ident
    assert a == expected, f"wrong answer for input {data[:20]}..."


# --------------------------------------------------------------------------
# 1. Brute-force check on at least 500 random lists (per sort)
# --------------------------------------------------------------------------

@pytest.mark.parametrize("name", SORTS)
def test_500_random_lists(name):
    rng = random.Random(2026)            # fixed seed: repeatable tests
    for trial in range(600):
        n = rng.randint(0, 300)
        lo = rng.choice([-1000, -10, 0])
        hi = rng.choice([5, 100, 10**6])
        data = [rng.randint(lo, hi) for _ in range(n)]
        check(SORTS[name], data)


# --------------------------------------------------------------------------
# 2. Required special cases
# --------------------------------------------------------------------------

SPECIAL = {
    "empty": [],
    "one_element": [42],
    "two_elements": [2, 1],
    "all_equal": [7] * 200,
    "already_sorted": list(range(300)),
    "reverse_sorted": list(range(300, 0, -1)),
    "negative_numbers": [-5, -1, -100, 0, -3, 7, -100, -42, 3],
    "all_negative": list(range(-1, -250, -1)),
    "few_distinct": [500, 100, 100, 500, 100, 1000, 100, 500] * 25,
    "large_values": [10**12, -10**12, 0, 2**63, -(2**63)],
}


@pytest.mark.parametrize("case", SPECIAL)
@pytest.mark.parametrize("name", SORTS)
def test_special_cases(name, case):
    check(SORTS[name], SPECIAL[case])


# --------------------------------------------------------------------------
# 3. The cases that broke the textbook version, at realistic size.
#    quicksort_improved must handle them without RecursionError.
# --------------------------------------------------------------------------

@pytest.mark.parametrize("kind", ["sorted", "reverse", "dups_0_9", "all_equal"])
def test_improved_large_bad_inputs(kind):
    n = 50_000
    rng = random.Random(1)
    data = {
        "sorted": list(range(n)),
        "reverse": list(range(n, 0, -1)),
        "dups_0_9": [rng.randint(0, 9) for _ in range(n)],
        "all_equal": [100] * n,
    }[kind]
    check(quicksort_improved, data)


def test_basic_crashes_on_large_sorted_input():
    """Documents the bug we are fixing: with Python's default recursion
    limit, the textbook version cannot sort 5,000 already-sorted items."""
    old = sys.getrecursionlimit()
    sys.setrecursionlimit(1000)
    try:
        with pytest.raises(RecursionError):
            quicksort_basic(list(range(5000)))
    finally:
        sys.setrecursionlimit(old)


def test_insertion_sort_helper():
    rng = random.Random(3)
    for _ in range(200):
        data = [rng.randint(-50, 50) for _ in range(rng.randint(0, 40))]
        a = list(data)
        insertion_sort(a)
        assert a == sorted(data)
    # sorting only a sub-range leaves the rest untouched
    a = [9, 8, 5, 3, 4, 1, 0]
    insertion_sort(a, 2, 4)
    assert a == [9, 8, 3, 4, 5, 1, 0]


if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
