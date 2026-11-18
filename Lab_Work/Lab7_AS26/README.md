# CSF302 Lab 7: Greedy and Randomized Algorithms

Python 3.11+ is required. There is one source file per question. Each file starts with an AI disclosure and ends with an analysis/conclusion comment that uses the measured numbers.

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

Run the scripts from inside `src/`, because they read `../data/` and write `../results/`:

```bash
cd src
python q1_greedy.py                        # activities from ../data/activities.txt
python q1_greedy.py --keyboard             # ...or type (start, finish) pairs
python q2_huffman.py                       # 4 sample texts; or: python q2_huffman.py FILE ...
python q3_graphs.py                        # all of Q3 (~10 s)
python q3_graphs.py dijkstra FILE SOURCE   # Dijkstra on your own graph file
python q4_randomized.py                    # ~1 min
cd ..
pytest -q                                  # 11 tests
```

**Graph file format:** the first line is `V E`, followed by one `u v w` line per edge. Vertices are numbered `0..V-1`, and `#` starts a comment.

## Files

| Question | File | Contents |
|---|---|---|
| Q1 | `src/q1_greedy.py` | Earliest-finish activity selection, earliest-start and shortest-duration rules with counterexamples from random testing, fractional knapsack, greedy vs DP for 0/1 knapsack |
| Q2 | `src/q2_huffman.py` | Huffman tree built with heapq, code table, encode/decode check, compression ratio on 4 files |
| Q3 | `src/q3_graphs.py` | Dijkstra with a binary heap (checked against Bellman-Ford), Kruskal with union-find, Prim with a heap, MST check, sparse/dense timing, negative-edge counterexample |
| Q4 | `src/q4_randomized.py` | Randomized quickselect vs sort + index, Miller-Rabin vs trial division, the 561 experiment |
| — | `data/` | `activities.txt` (CLRS), `graph.txt` (CLRS Fig. 24.6), `negative.txt`, and `texts/` (English prose, Python source, DNA, random printable characters) |
| — | `results/` | Tables, Huffman code tables, plots, logs |

## Key results

- **Q1:** earliest finish selects 4 activities (optimal). Earliest start fails on `[(5,6),(6,12),(4,8)]` and shortest duration fails on `[(6,10),(4,7),(1,5)]`. Fractional knapsack on the CLRS items gives 240. For 0/1 knapsack, the worst greedy/optimal ratio found was **0.129**, and an adversarial family drives it towards 0.
- **Q2:** compared with 8-bit fixed-length encoding, Huffman saves 46% on English prose, 40% on Python source, 72% on DNA and 17% on random characters. Every file decodes back to the original exactly.
- **Q3:**
  - **Sparse graph:** Kruskal and Prim are about equally fast.
  - **Dense graph:** Kruskal is about 10× faster than heap-based Prim. The extra array-based Prim (O(V²)) is about 9× faster than heap-based Prim and close to Kruskal.
  - **Negative edge:** Dijkstra gets a = 2 and c = 3, while the correct distances are a = 1 and c = 2.
- **Q4:**
  - **Quickselect:** about 7–10× faster than our own merge sort plus indexing.
  - **Primality:** Miller-Rabin and trial division agree on all 20 numbers. On 12-digit primes, Miller-Rabin is 55–156× faster.
  - **561:** one-round Miller-Rabin answered "prime" 13 times in 1,000 runs. The exact rate is 8 strong liars out of 558 bases, or 1.43%.

**Note on library use:** `heapq` is used where the lab allows a priority queue (Huffman, Dijkstra, Prim). `sorted()` is used only for pre-sorting steps that aren't the algorithm being studied (activities by finish time, knapsack items by ratio, Kruskal's edge list), and as one of the baselines in Q4.1. If your instructor requires your own sort there, swap in the Lab 1 merge sort.

The times in the analysis comments come from my run. Yours will differ, but the trends should match.

> **Before submitting:** edit the AI disclosure at the top of each file so it says how you actually used AI.
