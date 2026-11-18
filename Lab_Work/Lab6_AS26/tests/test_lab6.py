"""
CSF302 Lab 6 - pytest suite.

AI disclosure: Written with Claude (Anthropic) as a coding assistant. Review
and edit this note so it states how you used AI.

Run from the lab6 folder:  pytest -q
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from q1_rod_cutting import (cut_rod_bottom_up, cut_rod_memo, cut_rod_naive, pieces,
                            price_table)
from q2_matrix_chain import (brute_force, cost_of_parenthesisation, left_to_right_cost,
                             min_cost)
from q3_lcs import (diff_lines, is_subsequence, lcs, lcs_brute_force,
                    lcs_length_two_rows)
from q4_optimal_bst import P, Q, brute_force_min_cost, optimal_bst


def test_rod_known_revenues():
    p = price_table(10)
    r, s, _ = cut_rod_bottom_up(p, 10)
    assert r[1:] == [1, 5, 8, 10, 13, 17, 18, 22, 25, 30]
    for n in range(1, 11):
        assert sum(p[c] for c in pieces(s, n)) == r[n]


def test_rod_versions_agree_and_call_counts():
    for n in range(0, 16):
        p = price_table(n)
        rv_n, calls_n = cut_rod_naive(p, n)
        rv_m, calls_m = cut_rod_memo(p, n)
        assert rv_n == rv_m == cut_rod_bottom_up(p, n)[0][n]
        assert calls_n == 2 ** n
        assert calls_m == n * (n + 1) // 2 + 1


def test_matrix_chain_known():
    assert min_cost([30, 35, 15, 5, 10, 20, 25]) == (15125, "((A1(A2A3))((A4A5)A6))")
    assert min_cost([5, 4, 6, 2, 7])[0] == 158
    assert left_to_right_cost([30, 35, 15, 5, 10, 20, 25]) == 40500


def test_matrix_chain_vs_brute():
    rng = random.Random(9)
    for _ in range(30):
        p = [rng.randint(1, 40) for _ in range(rng.randint(2, 8))]
        cost, paren = min_cost(p)
        assert cost == brute_force(p)[0] == cost_of_parenthesisation(p, paren)


def test_lcs_clrs():
    assert lcs("ABCBDAB", "BDCABA") == "BCBA"
    assert lcs_length_two_rows("ABCBDAB", "BDCABA") == 4


def test_lcs_vs_brute():
    rng = random.Random(10)
    for _ in range(60):
        X = "".join(rng.choice("AB C") for _ in range(rng.randint(0, 10)))
        Y = "".join(rng.choice("ABC") for _ in range(rng.randint(0, 10)))
        s = lcs(X, Y)
        assert len(s) == len(lcs_brute_force(X, Y)) == lcs_length_two_rows(X, Y)
        assert is_subsequence(s, X) and is_subsequence(s, Y)


def test_diff_rebuilds_both_files():
    a = ["x", "a", "b", "c", "y"]
    b = ["a", "z", "c", "y", "w"]
    d = diff_lines(a, b)
    assert [l for t, l in d if t != "-"] == b
    assert [l for t, l in d if t != "+"] == a
    assert sum(t == " " for t, _ in d) == len(lcs(a, b)) == 3


def test_optimal_bst():
    e, _, root = optimal_bst(P, Q, 5)
    assert abs(e[1][5] - 2.75) < 1e-9
    assert root[1][5] == 2
    assert abs(brute_force_min_cost(P, Q, 1, 5) - 2.75) < 1e-9
