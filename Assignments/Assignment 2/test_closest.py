"""
Part B: tests for closest.py.   Run with:   python -m pytest -v test_closest.py

Every test checks the divide-and-conquer answer against the brute-force
answer. Because two different pairs can tie for the smallest distance, we
compare the DISTANCE exactly and then check that the returned indices are
valid (i < j, in range) and really are that distance apart.
"""

import math
import random

import pytest

from closest import closest_pair, closest_pair_brute


def assert_valid(points, result, expected_d):
    d, i, j = result
    assert 0 <= i < j < len(points), "bad indices %r" % ((i, j),)
    assert math.isclose(d, expected_d, rel_tol=1e-12, abs_tol=1e-12)
    assert math.isclose(math.dist(points[i], points[j]), d,
                        rel_tol=1e-12, abs_tol=1e-12)


def check_against_brute(points):
    expected = closest_pair_brute(points)
    assert_valid(points, expected, expected[0])          # brute is self-consistent
    assert_valid(points, closest_pair(points), expected[0])


# ---------------------------------------------------------------- example
def test_assignment_example():
    pts = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    for f in (closest_pair_brute, closest_pair):
        d, i, j = f(pts)
        assert (i, j) == (0, 5)
        assert math.isclose(d, math.sqrt(2))


# ---------------------------------------------------------------- random
@pytest.mark.parametrize("seed", range(500))
def test_random_integer_points(seed):
    """500 random inputs, 2 to 50 points, small grid so ties/duplicates occur."""
    rng = random.Random(seed)
    n = rng.randint(2, 50)
    pts = [(rng.randint(0, 100), rng.randint(0, 100)) for _ in range(n)]
    check_against_brute(pts)


@pytest.mark.parametrize("seed", range(200))
def test_random_float_points(seed):
    rng = random.Random(10_000 + seed)
    n = rng.randint(2, 50)
    pts = [(rng.uniform(-1000, 1000), rng.uniform(-1000, 1000)) for _ in range(n)]
    check_against_brute(pts)


def test_larger_random_inputs():
    rng = random.Random(42)
    for n in (100, 257, 1000):
        pts = [(rng.randint(0, 10**6), rng.randint(0, 10**6)) for _ in range(n)]
        check_against_brute(pts)


# ---------------------------------------------------------------- edge cases
def test_exactly_two_points():
    pts = [(0, 0), (3, 4)]
    for f in (closest_pair_brute, closest_pair):
        assert f(pts) == (5.0, 0, 1)


def test_exactly_two_points_reversed_order():
    pts = [(10, 10), (-2, 5)]                     # x-sort swaps them
    assert closest_pair(pts) == (13.0, 0, 1)      # but indices stay i < j


def test_duplicate_points_answer_zero():
    pts = [(5, 5), (1, 9), (7, 2), (1, 9), (8, 8)]
    for f in (closest_pair_brute, closest_pair):
        assert f(pts) == (0.0, 1, 3)


def test_all_points_identical():
    pts = [(4, 4)] * 20
    d, i, j = closest_pair(pts)
    assert d == 0 and 0 <= i < j < 20


def test_many_duplicates_random():
    rng = random.Random(7)
    for _ in range(50):
        base = [(rng.randint(0, 5), rng.randint(0, 5)) for _ in range(5)]
        pts = [rng.choice(base) for _ in range(rng.randint(2, 40))]
        check_against_brute(pts)


def test_all_on_one_vertical_line():
    pts = [(7, y) for y in (0, 10, 25, 26, 40, 70, 71.5, 90)]
    check_against_brute(pts)
    assert closest_pair(pts) == (1.0, 2, 3)


def test_vertical_line_random():
    rng = random.Random(3)
    for _ in range(50):
        pts = [(3, rng.randint(-500, 500)) for _ in range(rng.randint(2, 50))]
        check_against_brute(pts)


def test_all_on_one_horizontal_line():
    pts = [(x, 0) for x in (0, 9, 20, 22, 50, 80)]
    assert closest_pair(pts) == (2.0, 2, 3)


def test_closest_pair_crosses_dividing_line():
    # 8 points: the split is after the 4th point by x (x = 49 | x = 51).
    # Points inside each half are >= 30 apart; the closest pair is
    # (49, 50) on the left and (51, 50) on the right, distance 2.
    pts = [(0, 0), (0, 100), (20, 50), (49, 50),     # left half
           (51, 50), (80, 50), (100, 0), (100, 100)] # right half
    left = closest_pair_brute(pts[:4])[0]
    right = closest_pair_brute(pts[4:])[0]
    assert left > 2 and right > 2                    # not found inside a half
    assert closest_pair(pts) == (2.0, 3, 4)


def test_crossing_pair_needs_strip_y_order():
    # Crossing pair is NOT the pair with the nearest x values: the strip
    # must be searched in y order to find it.
    pts = [(0, 0), (10, 300), (45, 0), (49, 100),
           (51, 103), (55, 0), (90, 300), (100, 0)]
    check_against_brute(pts)
    assert closest_pair(pts)[1:] == (3, 4)


def test_crossing_pair_shuffled_input():
    rng = random.Random(1)
    pts = [(0, 0), (0, 100), (20, 50), (49, 50),
           (51, 50), (80, 50), (100, 0), (100, 100)]
    for _ in range(20):
        shuffled = pts[:]
        rng.shuffle(shuffled)
        check_against_brute(shuffled)


def test_negative_coordinates():
    pts = [(-5, -5), (-100, 3), (40, -60), (-4, -6), (0, 0)]
    check_against_brute(pts)


def test_input_not_modified():
    pts = [(3, 1), (1, 2), (2, 9), (0, 0)]
    copy = list(pts)
    closest_pair(pts)
    assert pts == copy


@pytest.mark.parametrize("bad", [[], [(1, 1)]])
def test_too_few_points_raises(bad):
    with pytest.raises(ValueError):
        closest_pair(bad)
    with pytest.raises(ValueError):
        closest_pair_brute(bad)
