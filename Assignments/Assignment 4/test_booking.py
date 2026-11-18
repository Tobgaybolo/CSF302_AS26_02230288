"""
Part B: tests for booking.py

Run with:   python -m pytest test_booking.py -v
"""

import random

import pytest

from booking import (
    best_schedule,
    brute_force,
    greedy_earliest_finish,
    greedy_highest_fee,
    is_valid_schedule,
)

ALL_FUNCS = [greedy_earliest_finish, greedy_highest_fee, best_schedule, brute_force]
EXAMPLE = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000),
           (12, 14, 2500), (16, 18, 2000)]


def random_requests(rng, n, horizon=24, max_len=8, fee_values=None):
    """n random requests with integer times in [0, horizon]."""
    reqs = []
    for _ in range(n):
        start = rng.randint(0, horizon - 1)
        finish = min(horizon, start + rng.randint(1, max_len))
        fee = rng.choice(fee_values) if fee_values else rng.randint(1, 100) * 100
        reqs.append((start, finish, fee))
    return reqs


def check_result(requests, result):
    """The returned total must equal the fees of the returned schedule,
    and the schedule must be feasible."""
    total, chosen = result
    assert is_valid_schedule(requests, chosen)
    assert total == sum(requests[i][2] for i in chosen)


# --------------------------------------------------------------------------
# The worked example from the brief
# --------------------------------------------------------------------------

def test_example_from_brief():
    assert greedy_earliest_finish(EXAMPLE) == (7500, [0, 3, 4])
    assert best_schedule(EXAMPLE) == (10000, [1, 4])
    assert brute_force(EXAMPLE) == (10000, [1, 4])


# --------------------------------------------------------------------------
# Main correctness check: DP against brute force on 500+ random inputs
# --------------------------------------------------------------------------

def test_dp_matches_brute_force_random():
    rng = random.Random(2026)
    for trial in range(1000):              # at least 500 required
        n = rng.randint(0, 10)
        reqs = random_requests(rng, n)
        dp_total, dp_chosen = best_schedule(reqs)
        bf_total, _ = brute_force(reqs)
        assert dp_total == bf_total, f"trial {trial}: {reqs}"
        check_result(reqs, (dp_total, dp_chosen))


def test_dp_matches_brute_force_with_zero_length_and_ties():
    """Harder random inputs: many shared endpoints, zero-length events,
    duplicate requests and equal fees."""
    rng = random.Random(7)
    for trial in range(500):
        n = rng.randint(0, 10)
        reqs = []
        for _ in range(n):
            s = rng.randint(0, 6)
            f = s + rng.randint(0, 3)      # length 0 allowed
            reqs.append((s, f, rng.choice([1, 2, 3, 5])))
        assert best_schedule(reqs)[0] == brute_force(reqs)[0], f"trial {trial}: {reqs}"
        check_result(reqs, best_schedule(reqs))


@pytest.mark.parametrize("func", ALL_FUNCS)
def test_every_function_returns_a_feasible_schedule(func):
    rng = random.Random(99)
    for _ in range(300):
        reqs = random_requests(rng, rng.randint(0, 10))
        check_result(reqs, func(reqs))


def test_greedy_never_beats_optimum():
    rng = random.Random(5)
    for _ in range(500):
        reqs = random_requests(rng, rng.randint(0, 10))
        best = brute_force(reqs)[0]
        assert greedy_earliest_finish(reqs)[0] <= best
        assert greedy_highest_fee(reqs)[0] <= best


# --------------------------------------------------------------------------
# Required edge cases
# --------------------------------------------------------------------------

@pytest.mark.parametrize("func", ALL_FUNCS)
def test_no_requests(func):
    assert func([]) == (0, [])


@pytest.mark.parametrize("func", ALL_FUNCS)
def test_one_request(func):
    assert func([(8, 10, 1500)]) == (1500, [0])


def test_all_overlapping():
    # Every request covers 11-12, so only one can be accepted.
    reqs = [(9, 13, 2000), (10, 12, 5000), (11, 15, 3000), (8, 12, 1000)]
    assert best_schedule(reqs) == (5000, [1])
    assert brute_force(reqs) == (5000, [1])
    assert greedy_highest_fee(reqs) == (5000, [1])
    total, chosen = greedy_earliest_finish(reqs)
    assert len(chosen) == 1                 # earliest finish takes (10,12) or (8,12)
    check_result(reqs, (total, chosen))


@pytest.mark.parametrize("func", ALL_FUNCS)
def test_none_overlapping(func):
    # Gaps between every pair: every function should accept everything.
    reqs = [(14, 15, 400), (6, 8, 1000), (10, 12, 700), (1, 3, 200)]
    assert func(reqs) == (2300, [0, 1, 2, 3])


@pytest.mark.parametrize("func", ALL_FUNCS)
def test_back_to_back(func):
    # Each event ends exactly when the next starts, which is allowed.
    reqs = [(9, 12, 3000), (12, 14, 2500), (14, 18, 4000), (18, 20, 1000)]
    assert func(reqs) == (10500, [0, 1, 2, 3])


def test_back_to_back_off_by_one_is_rejected():
    # Ending at 12 and starting at 11 do NOT fit.
    reqs = [(9, 12, 3000), (11, 14, 2500)]
    assert best_schedule(reqs) == (3000, [0])
    assert greedy_earliest_finish(reqs) == (3000, [0])


def test_input_is_not_modified():
    reqs = list(EXAMPLE)
    for func in ALL_FUNCS:
        func(reqs)
    assert reqs == EXAMPLE


def test_invalid_request_rejected():
    with pytest.raises(ValueError):
        best_schedule([(10, 9, 100)])


# --------------------------------------------------------------------------
# Equal fees: earliest-finish greedy is optimal
# --------------------------------------------------------------------------

def test_equal_fees_greedy_earliest_finish_is_optimal():
    rng = random.Random(11)
    for trial in range(1000):
        n = rng.randint(0, 10)
        reqs = random_requests(rng, n, fee_values=[1000])
        assert greedy_earliest_finish(reqs)[0] == brute_force(reqs)[0], f"trial {trial}: {reqs}"


def test_equal_fees_large_inputs_match_dp():
    """Beyond brute-force size, compare against the (already verified) DP."""
    rng = random.Random(12)
    for _ in range(300):
        reqs = random_requests(rng, rng.randint(11, 60), horizon=100, max_len=20,
                               fee_values=[500])
        assert greedy_earliest_finish(reqs)[0] == best_schedule(reqs)[0]


# --------------------------------------------------------------------------
# Part C counterexamples, kept as regression tests
# --------------------------------------------------------------------------

def test_counterexample_earliest_finish():
    reqs = [(0, 5, 1000), (1, 10, 6000)]
    assert greedy_earliest_finish(reqs) == (1000, [0])
    assert best_schedule(reqs) == (6000, [1])


def test_counterexample_highest_fee():
    reqs = [(0, 10, 5000), (0, 5, 3000), (5, 10, 3000)]
    assert greedy_highest_fee(reqs) == (5000, [0])
    assert best_schedule(reqs) == (6000, [1, 2])


def test_counterexample_both_rules_fail():
    reqs = [(0, 3, 1000), (1, 6, 5000), (6, 9, 3000), (3, 9, 6000)]
    best = best_schedule(reqs)
    assert best == brute_force(reqs) == (8000, [1, 2])
    assert greedy_earliest_finish(reqs)[0] < best[0]
    assert greedy_highest_fee(reqs)[0] < best[0]
