"""
CSF302 Lab 4 - pytest suite for Parts A and B.

AI disclosure: Written with Claude (Anthropic) as a coding assistant. Review
and edit this note so it states how you used AI.

Run from the lab4 folder:  pytest -q
"""
import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from a1_naive_modexp import naive_mod_pow
from a2_binary_modexp import binary_mod_pow
from a4_bitwise_modexp import bitwise_mod_pow
from a5_validated_modexp import mod_pow
from b1_matmul_mod import mat_mult_mod
from b2_identity import identity
from b3_naive_matpow import naive_mat_pow
from b4_binary_matpow import binary_mat_pow
from b6_fibonacci_mod import fib_mod, fib_mod_iterative
from b7_fib_huge import fib_fast_doubling
from b8_graph_walks import adjacency_matrix, count_walks, count_walks_brute


# ---------------- Part A ----------------
@pytest.mark.parametrize("fn", [naive_mod_pow, binary_mod_pow, bitwise_mod_pow, mod_pow])
def test_modpow_small_random(fn):
    rng = random.Random(1)
    for _ in range(300):
        a, b, m = rng.randint(0, 10**6), rng.randint(0, 500), rng.randint(1, 10**6)
        assert fn(a, b, m) == pow(a, b, m)


@pytest.mark.parametrize("fn", [binary_mod_pow, bitwise_mod_pow, mod_pow])
def test_modpow_huge_exponent(fn):
    assert fn(2, 10**18, 10**9 + 7) == pow(2, 10**18, 10**9 + 7)


def test_validation_zero_exponent():
    assert mod_pow(7, 0, 13) == 1
    assert mod_pow(7, 0, 1) == 0


def test_validation_negative_base():
    assert mod_pow(-2, 3, 7) == (-8) % 7
    assert mod_pow(-3, 5, 11) == pow(-3, 5, 11)


@pytest.mark.parametrize("args", [(2, -1, 7), (2, 3, 0), (2, 3, -5)])
def test_validation_errors(args):
    with pytest.raises(ValueError):
        mod_pow(*args)


# ---------------- Part B ----------------
def test_matmul():
    assert mat_mult_mod([[1, 2], [3, 4]], [[5, 6], [7, 8]], 1000) == [[19, 22], [43, 50]]
    assert mat_mult_mod([[1, 2], [3, 4]], [[5, 6], [7, 8]], 10) == [[9, 2], [3, 0]]
    with pytest.raises(ValueError):
        mat_mult_mod([[1, 2]], [[1, 2]], 5)


def test_identity():
    assert identity(3) == [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    A = [[2, 3], [4, 5]]
    assert mat_mult_mod(A, identity(2), 100) == A


def test_naive_vs_binary_matpow():
    rng = random.Random(2)
    for _ in range(40):
        d = rng.randint(1, 5)
        A = [[rng.randint(-20, 20) for _ in range(d)] for _ in range(d)]
        n, m = rng.randint(0, 120), rng.randint(1, 10**9)
        assert naive_mat_pow(A, n, m) == binary_mat_pow(A, n, m)


def test_matpow_zero_exponent_is_identity():
    assert binary_mat_pow([[5, 6], [7, 8]], 0, 11) == identity(2)
    assert binary_mat_pow([[5, 6], [7, 8]], 0, 1) == [[0, 0], [0, 0]]


def test_fibonacci():
    assert [fib_mod(n, 10**9) for n in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    for n in range(0, 500, 3):
        assert fib_mod(n, 10**9 + 7) == fib_mod_iterative(n, 10**9 + 7)


def test_fib_1e18():
    ans = fib_mod(10**18, 10**9 + 7)
    assert ans == fib_fast_doubling(10**18, 10**9 + 7)[0] == 209783453


def test_graph_walks():
    A = adjacency_matrix(4, [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 0)])
    for k in range(7):
        for u in range(4):
            for v in range(4):
                assert count_walks(A, u, v, k, 10**9 + 7) == count_walks_brute(A, u, v, k)
