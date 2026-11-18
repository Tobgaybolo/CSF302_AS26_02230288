"""
CSF302 Lab 7 - Q3: Shortest Paths and Minimum Spanning Trees

  1. Dijkstra with a binary heap (heapq). Reads a weighted directed graph
     from a file and prints the distance and path from a source to every vertex.
     File format: first line "V E", then E lines "u v w" (vertices 0..V-1,
     '#' starts a comment).
  2. Kruskal (union-find with path compression and union by rank) and
     Prim (binary heap)
  3. Both MST algorithms give the same total weight on random connected graphs
  4. Timing for V = 1,000: sparse (E ~ 3V) and dense (E ~ V^2/4)
  5. A small graph with one negative edge where Dijkstra is wrong
     (../data/negative.txt), compared with Bellman-Ford

Dijkstra is checked against Bellman-Ford on random graphs, and the MSTs
against each other. sorted() is used only for Kruskal's edge-sorting step.

Method: time.perf_counter(), graphs generated outside the timed region
(fixed seed 42), median of 3 runs.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q3_graphs.py                         (everything, uses ../data/graph.txt, source 0)
      python q3_graphs.py dijkstra FILE SOURCE    (just Dijkstra on your own file)
"""
import heapq
import random
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from timing_utils import markdown_table, time_call

INF = float("inf")


# ---------------------------------------------------------------------------
# Graph input
# ---------------------------------------------------------------------------
def read_graph(path):
    """Return (V, edges, adj) with adj[u] = list of (v, w)."""
    with open(path) as f:
        lines = [ln.split("#")[0].strip() for ln in f]
    lines = [ln for ln in lines if ln]
    V, E = map(int, lines[0].split())
    edges = []
    for ln in lines[1:1 + E]:
        u, v, w = ln.split()
        edges.append((int(u), int(v), float(w) if "." in w else int(w)))
    if len(edges) != E:
        raise ValueError(f"header says {E} edges but {len(edges)} were found")
    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
    return V, edges, adj


# ---------------------------------------------------------------------------
# 1. Dijkstra (binary heap)
# ---------------------------------------------------------------------------
def dijkstra(adj, source):
    """Return (dist, parent). Heap holds (distance, vertex); stale entries
    are skipped. A vertex is FINAL when first popped (the set S of CLRS), and
    edges into final vertices are not relaxed. That matches the textbook
    algorithm, which assumes no negative edges.
    Theta((V + E) log V)."""
    V = len(adj)
    dist = [INF] * V
    parent = [None] * V
    done = [False] * V
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if done[u]:
            continue
        done[u] = True
        for v, w in adj[u]:
            if not done[v] and d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(heap, (dist[v], v))
    return dist, parent


def path_to(parent, source, v):
    if v != source and parent[v] is None:
        return None
    out = []
    while v is not None:
        out.append(v)
        v = parent[v]
    return out[::-1]


def bellman_ford(V, edges, source):
    """Checker / correct algorithm with negative edges. Theta(VE)."""
    dist = [INF] * V
    dist[source] = 0
    for _ in range(V - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            raise ValueError("negative cycle reachable from source")
    return dist


def print_shortest_paths(adj, source, names=None):
    dist, parent = dijkstra(adj, source)
    name = (lambda x: names[x]) if names else str
    print(f"Source {name(source)}")
    print(f"{'vertex':>8} {'distance':>9}  path")
    for v in range(len(adj)):
        p = path_to(parent, source, v)
        d = "inf" if dist[v] == INF else f"{dist[v]:g}"
        ps = " -> ".join(name(x) for x in p) if p else "unreachable"
        print(f"{name(v):>8} {d:>9}  {ps}")
    return dist


# ---------------------------------------------------------------------------
# 2. Minimum spanning trees (undirected graphs, edges (u, v, w))
# ---------------------------------------------------------------------------
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        root = x
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[x] != root:                # path compression
            self.parent[x], x = root, self.parent[x]
        return root

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:            # union by rank
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal(V, edges):
    """Sort edges by weight; keep an edge if it joins two different
    components. Theta(E log E) for the sort + ~Theta(E alpha(V)) union-find.
    Returns (total weight, tree edges)."""
    uf = UnionFind(V)
    total, tree = 0, []
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if uf.union(u, v):
            total += w
            tree.append((u, v, w))
            if len(tree) == V - 1:
                break
    if len(tree) != V - 1:
        raise ValueError("graph is not connected")
    return total, tree


def undirected_adj(V, edges):
    adj = [[] for _ in range(V)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    return adj


def prim(V, adj, start=0):
    """Grow one tree from `start`; the heap holds candidate edges (w, v, u)
    leaving the tree; stale ones are skipped. Theta(E log V)."""
    in_tree = [False] * V
    total, tree = 0, []
    heap = [(0, start, None)]
    while heap and len(tree) < V - 1 + 1:
        w, v, u = heapq.heappop(heap)
        if in_tree[v]:
            continue
        in_tree[v] = True
        if u is not None:
            total += w
            tree.append((u, v, w))
        for x, wx in adj[v]:
            if not in_tree[x]:
                heapq.heappush(heap, (wx, x, v))
    if len(tree) != V - 1:
        raise ValueError("graph is not connected")
    return total, tree


def prim_array(V, adj, start=0):
    """Extra for the explanation: Prim with a plain array instead of a heap
    (CLRS's O(V^2) version). The best choice for dense graphs in theory."""
    key = [INF] * V
    in_tree = [False] * V
    key[start] = 0
    total = 0
    for _ in range(V):
        u, best = -1, INF
        for x in range(V):
            if not in_tree[x] and key[x] < best:
                u, best = x, key[x]
        if u == -1:
            raise ValueError("graph is not connected")
        in_tree[u] = True
        total += best
        for x, w in adj[u]:
            if not in_tree[x] and w < key[x]:
                key[x] = w
    return total, None


def random_connected_graph(V, E, rng, max_w=1000):
    """Random spanning tree (guarantees connectivity) + extra random edges,
    no self-loops or duplicate pairs."""
    E = min(E, V * (V - 1) // 2)
    order = list(range(V))
    rng.shuffle(order)
    seen = set()
    edges = []
    for i in range(1, V):
        u, v = order[i], order[rng.randrange(i)]
        seen.add((min(u, v), max(u, v)))
        edges.append((u, v, rng.randint(1, max_w)))
    while len(edges) < E:
        u, v = rng.randrange(V), rng.randrange(V)
        if u != v and (min(u, v), max(u, v)) not in seen:
            seen.add((min(u, v), max(u, v)))
            edges.append((u, v, rng.randint(1, max_w)))
    return edges


# ---------------------------------------------------------------------------
# Parts
# ---------------------------------------------------------------------------
def part1(path="../data/graph.txt", source=0):
    V, edges, adj = read_graph(path)
    print(f"Graph {path}: V = {V}, E = {len(edges)}")
    dist = print_shortest_paths(adj, source)
    assert dist == bellman_ford(V, edges, source)
    rng = random.Random(42)
    for _ in range(300):
        n = rng.randint(1, 30)
        es = [(rng.randrange(n), rng.randrange(n), rng.randint(0, 50))
              for _ in range(rng.randint(0, 4 * n))]
        a = [[] for _ in range(n)]
        for u, v, w in es:
            a[u].append((v, w))
        s = rng.randrange(n)
        assert dijkstra(a, s)[0] == bellman_ford(n, es, s)
    print("Dijkstra == Bellman-Ford on this graph and 300 random graphs (non-negative weights).")


def part3(trials=200):
    rng = random.Random(42)
    for _ in range(trials):
        V = rng.randint(2, 60)
        E = rng.randint(V - 1, V * (V - 1) // 2)
        edges = random_connected_graph(V, E, rng, max_w=rng.choice([5, 1000]))  # include ties
        k, kt = kruskal(V, edges)
        p, pt = prim(V, undirected_adj(V, edges))
        assert k == p == prim_array(V, undirected_adj(V, edges))[0]
        assert len(kt) == len(pt) == V - 1
    print(f"Kruskal and Prim give the same MST weight on {trials} random connected graphs "
          f"(V = 2..60, with and without tied weights).")
    V = 6
    edges = random_connected_graph(V, 9, random.Random(1), max_w=20)
    k, kt = kruskal(V, edges)
    p, pt = prim(V, undirected_adj(V, edges))
    print(f"Example, V = {V}, edges {edges}")
    print(f"  Kruskal: weight {k}, edges {kt}")
    print(f"  Prim   : weight {p}, edges {pt}")


def part4():
    V = 1000
    rng = random.Random(42)
    cases = [("sparse", 3 * V), ("dense", V * V // 4)]
    rows = []
    for label, E in cases:
        edges = random_connected_graph(V, E, rng)               # untimed
        adj = undirected_adj(V, edges)                          # untimed
        tk, (wk, _) = time_call(kruskal, V, edges)
        tp, (wp, _) = time_call(prim, V, adj)
        ta, (wa, _) = time_call(prim_array, V, adj)
        assert wk == wp == wa
        rows.append((label, V, len(edges), wk, tk, tp, ta))
        print(f"{label:<6} V={V} E={len(edges):>7,}  MST={wk:,}  Kruskal={tk:.4f}s  "
              f"Prim(heap)={tp:.4f}s  Prim(array, extra)={ta:.4f}s", flush=True)
    table = markdown_table(["graph", "V", "E", "MST weight", "Kruskal (s)", "Prim heap (s)",
                            "Prim array O(V²) (s, extra)"],
                           [(l, v, f"{e:,}", f"{w:,}", f"{a:.4f}", f"{b:.4f}", f"{c:.4f}")
                            for l, v, e, w, a, b, c in rows])
    with open("../results/q3_mst_timing.md", "w") as f:
        f.write("# Q3.4 - MST timing, V = 1,000 (median of 3, seed 42)\n\n" + table + "\n")

    fig, ax = plt.subplots(figsize=(7, 4.3))
    x = range(len(rows))
    width = 0.27
    ax.bar([i - width for i in x], [r[4] for r in rows], width, label="Kruskal (union-find)")
    ax.bar(list(x), [r[5] for r in rows], width, label="Prim (binary heap)")
    ax.bar([i + width for i in x], [r[6] for r in rows], width, label="Prim (array, extra)")
    ax.set_xticks(list(x), [f"{r[0]}\nE = {r[2]:,}" for r in rows])
    ax.set_yscale("log")
    ax.set_ylabel("time (s, log scale)")
    ax.set_title("MST algorithms, V = 1,000")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig("../results/q3_mst_timing.png", dpi=140)
    print("Saved ../results/q3_mst_timing.{md,png}")


def part5(path="../data/negative.txt"):
    names = ["s", "a", "b", "c"]
    V, edges, adj = read_graph(path)
    print(f"Graph {path}: edges " + ", ".join(f"{names[u]}->{names[v]} ({w})" for u, v, w in edges))
    print("Dijkstra:")
    dist = print_shortest_paths(adj, 0, names)
    bf = bellman_ford(V, edges, 0)
    print("Bellman-Ford (correct):  " + ", ".join(f"{names[v]} = {bf[v]}" for v in range(V)))
    wrong = [names[v] for v in range(V) if dist[v] != bf[v]]
    print(f"Dijkstra is WRONG for: {wrong}")
    return wrong


def main():
    print("=== Q3.1 Dijkstra on ../data/graph.txt from vertex 0 ===")
    part1()
    print("\n=== Q3.2-3.3 Kruskal vs Prim ===")
    part3()
    print("\n=== Q3.4 Timing, V = 1,000 ===")
    part4()
    print("\n=== Q3.5 Negative edge ===")
    part5()


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "dijkstra":
        V, edges, adj = read_graph(sys.argv[2])
        print_shortest_paths(adj, int(sys.argv[3]))
    else:
        main()

# ---------------------------------------------------------------------------
# Analysis / conclusion  (times from one run on my machine; exact times will differ, but the trends should match)
#
# Q3.1: on ../data/graph.txt (the CLRS Fig. 24.6 graph, s=0 t=1 x=2 y=3 z=4)
# Dijkstra gives distances 0, 8, 9, 5, 7, with paths such as 0->3->1->2.
# Vertex 5 has no incoming edge and is reported unreachable. The results
# matched Bellman-Ford on this graph and on 300 random non-negative graphs.
#
# Q3.2-3.3: Kruskal and Prim gave the same total weight on 200 random
# connected graphs, including graphs with many tied weights. With ties the
# tree EDGES may differ, but the total weight of every MST is the same.
#
# Q3.4 timing, V = 1,000 (median of 3):
# | graph  | E       | Kruskal  | Prim (heap) | Prim (array, extra) |
# |--------|---------|----------|-------------|---------------------|
# | sparse | 3,000   | 0.0014 s | 0.0018 s    | 0.0310 s            |
# | dense  | 250,000 | 0.0850 s | 0.8496 s    | 0.0979 s            |
#
# Theory: Kruskal is Theta(E log E) and binary-heap Prim is Theta(E log V).
# Since log E <= 2 log V these are the same order, so neither wins in
# theory on either graph. The array version of Prim is Theta(V^2), which is
# better than E log V only when E is close to V^2.
# - Sparse: both are fast and close (Kruskal 1.4 ms vs Prim 1.8 ms). Kruskal
#   wins slightly: sorting 3,000 edges is cheap, and Prim pays a heap push
#   for each of the 2E = 6,000 adjacency entries.
# - Dense: Kruskal wins clearly (~10x over heap Prim). Prim's lazy heap
#   receives up to 2E = 500,000 pushes, each a Python-level O(log) operation,
#   while Kruskal's main cost is a single sort, done by Python's C-coded
#   sorted(). Kruskal also stops as soon as it has V - 1 edges, after
#   scanning only the cheapest part of the sorted list.
# - Array Prim (extra) is the slowest on the sparse graph (V^2 = 10^6 scans
#   vs E = 3,000) but ~9x faster than heap Prim on the dense graph, nearly tying Kruskal. It shows
#   the textbook advice that for dense graphs the O(V^2) Prim beats the heap
#   version. In a compiled language that version would usually also beat
#   Kruskal on dense graphs. In Python, the C-coded sort gives Kruskal the
#   edge here.
#
# Q3.5 negative edge (s->a 2, s->b 3, b->a -2, a->c 1): Dijkstra makes a
# final when it pops it with distance 2, then relaxes a->c, giving c = 3.
# Only later does it pop b (3) and find the cheaper route s->b->a = 1, but a
# is already final, so neither a nor c is corrected. Dijkstra reports a = 2,
# c = 3, while Bellman-Ford gives the true a = 1, c = 2. Dijkstra's proof
# needs "a popped vertex can never get cheaper", which only holds when no
# edge weight is negative.
# ---------------------------------------------------------------------------
