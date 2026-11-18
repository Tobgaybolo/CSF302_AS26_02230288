# CSF302 Lab 4: Modular and Matrix Exponentiation

Python 3.11+ is required. There is one source file per question. Each file starts with an AI disclosure and ends with an analysis/conclusion comment.

## Setup

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

Run the scripts from inside `src/`, because they write to `../results/`:

```bash
cd src
python a1_naive_modexp.py
...
python b9_benchmark_matpow.py          # about 1 minute (add --quick for 1 repeat)
cd ..
pytest -q                              # 19 tests
```

## Files

| Question | File | What it does |
|---|---|---|
| A1 | `src/a1_naive_modexp.py` | Naive a^b mod m, O(b) |
| A2 | `src/a2_binary_modexp.py` | Square-and-multiply, O(log b), with a step trace |
| A3 | `src/a3_compare_modexp.py` | 25 cases, naive vs binary → `results/a3_comparison.md` |
| A4 | `src/a4_bitwise_modexp.py` | Uses `b & 1` and `b >>= 1` |
| A5 | `src/a5_validated_modexp.py` | b=0 → 1 mod m, b<0 → error, a<0 → reduce, m<1 → error |
| A6 | `src/a6_timing_modexp.py` | Timing for b = 10 … 10^6 → `results/a6_timing.{csv,md,png}` |
| B1 | `src/b1_matmul_mod.py` | d×d matrix multiply mod m |
| B2 | `src/b2_identity.py` | Identity matrix |
| B3 | `src/b3_naive_matpow.py` | Naive A^n mod m, O(n d³) |
| B4 | `src/b4_binary_matpow.py` | Repeated squaring, O(d³ log n) |
| B5 | `src/b5_compare_matpow.py` | 20 cases, naive vs binary → `results/b5_comparison.md` |
| B6 | `src/b6_fibonacci_mod.py` | F(n) mod m via [[1,1],[1,0]]^n, checked against the iterative version |
| B7 | `src/b7_fib_huge.py` | F(10^18) mod (10^9+7) = **209783453**, checked by fast doubling |
| B8 | `src/b8_graph_walks.py` | Walks of length k via (A^k)[u][v], checked by brute-force DFS |
| B9 | `src/b9_benchmark_matpow.py` | d = 2…32, n = 2^4…2^12 → `results/b9_benchmark.{csv,md,png}` |
| — | `src/timing_utils.py` | Shared `perf_counter` timing helper (median of 3) |
| — | `tests/test_lab4.py` | pytest suite |

## Timing method

All timings use `time.perf_counter()`. Inputs are generated outside the timed region, each measurement is the median of 3 runs, and the random seed is fixed at 42. Every fast algorithm is checked against its naive or brute-force version before it is timed. Python's `pow()` is used only as an answer checker.

## Key results

- **A6:** Naive time grows about 10× per 10× increase in b (slope 1 on the log-log plot, Θ(b)). Binary time stays almost flat (Θ(log b)). The speed-up is about 20,000× at b = 10^6.
- **B9:** Naive time doubles with n (Θ(n)) and approaches 8× per doubling of d (Θ(d³)). Binary time grows only with log n. The speed-up at n = 4096 is about 250–470×, close to the theoretical 4096/13 ≈ 315×.

The numbers in the analysis comments come from my run. Your machine will give different times, but the trends should be the same.

> **Before submitting:** edit the AI disclosure at the top of each file so it says how you actually used AI. Make sure you can explain every line.
