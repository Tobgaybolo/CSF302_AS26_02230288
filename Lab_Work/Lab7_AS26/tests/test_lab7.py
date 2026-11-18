"""
CSF302 Lab 7 - pytest suite.

AI disclosure: Written with Claude (Anthropic) as a coding assistant. Review
and edit this note so it states how you used AI.

Run from the lab7 folder:  pytest -q
"""
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from q1_greedy import (dp_01, fractional_knapsack, greedy_01, max_compatible_brute,
                       select_earliest_finish, select_earliest_start, select_shortest)
from q2_huffman import build_codes, build_huffman_tree, char_frequencies, decode, encode
from q3_graphs import (bellman_ford, dijkstra, kruskal, prim, random_connected_graph,
                       undirected_adj)
from q4_randomized import miller_rabin, mod_pow, quickselect, strong_probable_prime, trial_division


def test_activity_selection_clrs():
    acts = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11), (8, 12), (2, 14), (12, 16)]
    assert select_earliest_finish(acts) == [(1, 4), (5, 7), (8, 11), (12, 16)]


def test_earliest_finish_optimal_random():
    rng = random.Random(1)
    for _ in range(300):
        acts = [(s, s + rng.randint(1, 6)) for s in (rng.randint(0, 12) for _ in range(rng.randint(1, 7)))]
        assert len(select_earliest_finish(acts)) == max_compatible_brute(acts)


def test_other_rules_can_fail():
    assert len(select_earliest_start([(5, 6), (6, 12), (4, 8)])) == 1
    assert len(select_shortest([(6, 10), (4, 7), (1, 5)])) == 1


def test_knapsack():
    items = [(60, 10), (100, 20), (120, 30)]
    assert abs(fractional_knapsack(items, 50)[0] - 240) < 1e-9
    assert greedy_01(items, 50)[0] == 160 and dp_01(items, 50) == 220


def test_huffman_round_trip():
    for text in ["abracadabra", "a", "aaaa", "the quick brown fox\njumps\tover", "ab" * 100 + "c"]:
        root = build_huffman_tree(char_frequencies(text))
        codes = build_codes(root)
        assert decode(encode(text, codes), root) == text


def test_huffman_clrs_lengths():
    freq = {"a": 45, "b": 13, "c": 12, "d": 16, "e": 9, "f": 5}
    codes = build_codes(build_huffman_tree(freq))
    assert sum(freq[c] * len(codes[c]) for c in freq) == 224       # CLRS: 224 bits per 100 chars


def test_dijkstra_vs_bellman_ford():
    rng = random.Random(2)
    for _ in range(100):
        n = rng.randint(1, 20)
        es = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 30)) for _ in range(rng.randint(0, 3 * n))]
        adj = [[] for _ in range(n)]
        for u, v, w in es:
            adj[u].append((v, w))
        assert dijkstra(adj, 0)[0] == bellman_ford(n, es, 0)


def test_dijkstra_wrong_with_negative_edge():
    es = [(0, 1, 2), (0, 2, 3), (2, 1, -2), (1, 3, 1)]
    adj = [[] for _ in range(4)]
    for u, v, w in es:
        adj[u].append((v, w))
    assert dijkstra(adj, 0)[0] != bellman_ford(4, es, 0)


def test_mst_equal():
    rng = random.Random(3)
    for _ in range(50):
        V = rng.randint(2, 40)
        edges = random_connected_graph(V, rng.randint(V - 1, V * (V - 1) // 2), rng, max_w=10)
        assert kruskal(V, edges)[0] == prim(V, undirected_adj(V, edges))[0]


def test_quickselect():
    rng = random.Random(4)
    for _ in range(200):
        a = [rng.randint(0, 50) for _ in range(rng.randint(1, 100))]
        k = rng.randint(1, len(a))
        assert quickselect(a, k, rng) == sorted(a)[k - 1]


def test_primality():
    rng = random.Random(5)
    for n in range(0, 3000):
        assert miller_rabin(n, 10, rng) == trial_division(n)
    assert mod_pow(7, 560, 561) == pow(7, 560, 561)
    liars = [a for a in range(2, 560) if strong_probable_prime(561, a)]
    assert liars == [50, 101, 103, 256, 305, 458, 460, 511]
