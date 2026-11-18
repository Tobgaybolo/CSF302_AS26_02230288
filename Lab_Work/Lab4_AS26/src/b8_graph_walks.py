"""
CSF302 Lab 4 - Part B, Question 8
Count walks of exactly k edges between two vertices of a directed graph,
modulo m, using the adjacency matrix.

Fact: if A is the adjacency matrix (A[i][j] = number of edges i -> j), then
(A^k)[u][v] = number of walks of length k from u to v.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python b8_graph_walks.py
"""
from b4_binary_matpow import binary_mat_pow


def adjacency_matrix(n_vertices: int, edges: list[tuple[int, int]]) -> list[list[int]]:
    """Build an adjacency matrix; repeated edges (multigraph) are counted."""
    A = [[0] * n_vertices for _ in range(n_vertices)]
    for u, v in edges:
        if not (0 <= u < n_vertices and 0 <= v < n_vertices):
            raise ValueError(f"edge ({u}, {v}) uses a vertex outside 0..{n_vertices - 1}")
        A[u][v] += 1
    return A


def count_walks(A, u: int, v: int, k: int, m: int) -> int:
    """Number of walks with exactly k edges from u to v, mod m. Theta(d^3 log k)."""
    if k < 0:
        raise ValueError("k must be >= 0")
    d = len(A)
    if not (0 <= u < d and 0 <= v < d):
        raise ValueError("vertex out of range")
    return binary_mat_pow(A, k, m)[u][v]


def count_walks_brute(A, u: int, v: int, k: int) -> int:
    """Brute-force check: explore every walk of length k by DFS (exponential)."""
    if k == 0:
        return 1 if u == v else 0
    return sum(A[u][w] * count_walks_brute(A, w, v, k - 1)
               for w in range(len(A)) if A[u][w])


if __name__ == "__main__":
    # Example directed graph (vertices 0..3):
    #   0 -> 1, 0 -> 2, 1 -> 2, 2 -> 0, 2 -> 3, 3 -> 0
    edges = [(0, 1), (0, 2), (1, 2), (2, 0), (2, 3), (3, 0)]
    A = adjacency_matrix(4, edges)
    print("Edges:", edges)
    print("Adjacency matrix:")
    for row in A:
        print("   ", row)

    MOD = 10**9 + 7
    print("\nWalks from 0 to 3 (matrix vs brute-force DFS):")
    for k in range(0, 11):
        fast = count_walks(A, 0, 3, k, MOD)
        slow = count_walks_brute(A, 0, 3, k) % MOD
        print(f"  k={k:>2}: matrix={fast:>4}  brute={slow:>4}  {'ok' if fast == slow else 'MISMATCH'}")
        assert fast == slow

    # Check every (u, v) pair for small k
    for k in range(0, 8):
        for u in range(4):
            for v in range(4):
                assert count_walks(A, u, v, k, MOD) == count_walks_brute(A, u, v, k) % MOD
    print("All (u, v, k <= 7) pairs match brute force.")

    # Hand-checkable: walks of length 2 from 0 to 0 are 0->2->0 only -> 1
    print("\nwalks(0 -> 0, k=2) =", count_walks(A, 0, 0, 2, MOD), "(only 0->2->0)")
    print("walks(0 -> 3, k=2) =", count_walks(A, 0, 3, 2, MOD), "(only 0->2->3)")
    print("walks(0 -> 3, k=3) =", count_walks(A, 0, 3, 3, MOD), "(only 0->1->2->3)")

    # Large k: impossible by brute force, instant with matrix powers
    for k in (10**3, 10**9, 10**18):
        print(f"walks(0 -> 3, k={k}) mod 10^9+7 = {count_walks(A, 0, 3, k, MOD)}")

# ---------------------------------------------------------------------------
# Analysis / conclusion
# (A^k)[u][v] = sum_w (A^(k-1))[u][w] * A[w][v]: every walk of length k to v
# is a walk of length k-1 to some w followed by an edge w -> v, so induction
# on k proves the formula. Matrix results matched an exhaustive DFS count
# for every vertex pair with k <= 7 and for 0 -> 3 up to k = 10. The DFS is
# exponential in k (it lists every walk), while the matrix method costs
# Theta(d^3 log k), so k = 10^18 still runs instantly. The modulus is needed
# because the true counts grow exponentially in k.
# ---------------------------------------------------------------------------
