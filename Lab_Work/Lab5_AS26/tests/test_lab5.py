"""
CSF302 Lab 5 - pytest suite.

AI disclosure: Written with Claude (Anthropic) as a coding assistant. Review
and edit this note so it states how you used AI.

Run from the lab5 folder:  pytest -q
"""
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from merge_sort import merge_sort
from q1_quicksort import VARIANTS, quicksort_lomuto, quicksort_hoare
from q2_counting_radix import counting_sort, counting_sort_by_key, radix_sort
from q3_inversions import (count_inversions_brute, count_inversions_merge,
                           kendall_tau_distance)

INPUT_KINDS = ["random", "sorted", "reverse", "duplicates", "empty", "single", "all_equal"]


def make(kind, n, rng):
    if kind == "empty":
        return []
    if kind == "single":
        return [5]
    if kind == "all_equal":
        return [7] * n
    if kind == "duplicates":
        return [rng.randint(0, 9) for _ in range(n)]
    a = [rng.randint(0, 10**6) for _ in range(n)]
    return sorted(a) if kind == "sorted" else sorted(a, reverse=True) if kind == "reverse" else a


@pytest.mark.parametrize("name", list(VARIANTS))
@pytest.mark.parametrize("kind", INPUT_KINDS)
def test_quicksort_variants(name, kind):
    rng = random.Random(3)
    data = make(kind, 500, rng)
    arr = list(data)
    VARIANTS[name](arr)
    assert arr == sorted(data)


def test_sorted_input_is_quadratic_but_no_recursion_error():
    n = 3000                                   # > default recursion limit of 1000
    a = list(range(n))
    assert quicksort_lomuto(a) == n * (n - 1) // 2
    b = list(range(n))
    quicksort_hoare(b)
    assert b == list(range(n))


def test_counting_sort():
    rng = random.Random(4)
    for k in [0, 1, 10, 1000]:
        a = [rng.randint(0, k) for _ in range(300)]
        assert counting_sort(a, k) == sorted(a)
    with pytest.raises(ValueError):
        counting_sort([1, 11], 10)


def test_counting_sort_is_stable():
    rng = random.Random(5)
    pairs = [(rng.randint(0, 5), i) for i in range(1000)]
    assert counting_sort_by_key(pairs, 5, key=lambda p: p[0]) == sorted(pairs)


@pytest.mark.parametrize("base", [2, 10, 256])
def test_radix_sort(base):
    rng = random.Random(6)
    a = [rng.randint(0, 10**9) for _ in range(2000)] + [0, 0, 10**9]
    assert radix_sort(a, base) == sorted(a)
    assert radix_sort([], base) == []


def test_merge_sort():
    rng = random.Random(7)
    a = [rng.randint(-100, 100) for _ in range(1000)]
    assert merge_sort(a) == sorted(a)


def test_inversions_agree():
    rng = random.Random(8)
    for _ in range(100):
        a = [rng.randint(0, rng.choice([3, 1000])) for _ in range(rng.randint(0, 400))]
        assert count_inversions_brute(a) == count_inversions_merge(a)
    assert count_inversions_merge([2, 4, 1, 3, 5]) == 3
    assert count_inversions_merge(list(range(100, 0, -1))) == 4950
    assert count_inversions_merge([1, 1, 1]) == 0


def test_kendall_tau():
    r = list("ABCDEFGHIJ")
    assert kendall_tau_distance(r, r) == 0
    assert kendall_tau_distance(r, r[::-1]) == 45
    assert kendall_tau_distance(r, ["B", "A"] + r[2:]) == 1
    with pytest.raises(ValueError):
        kendall_tau_distance(r, r[:-1] + ["Z"])
