# CSF302 Lab 6: Dynamic Programming

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
python q1_rod_cutting.py                 # ~30 s (naive n = 25 makes 33.5 million calls)
python q2_matrix_chain.py
python q3_lcs.py                         # table, LCS, timing, then diff of data/old.txt vs data/new.txt
python q3_lcs.py diff FILE1 FILE2        # diff any two text files
python q4_optimal_bst.py                 # optional question
cd ..
pytest -q                                # 8 tests
```

## Files

| Question | File | Contents |
|---|---|---|
| Q1 | `src/q1_rod_cutting.py` | Naive, memoized and bottom-up rod cutting; revenue and pieces for n = 1–10; call counts and timing for n = 5–25 |
| Q2 | `src/q2_matrix_chain.py` | Bottom-up DP, parenthesisation, brute-force check, CLRS and small chains plus 5 random chains, left-to-right cost |
| Q3 | `src/q3_lcs.py` | LCS table with arrows, reconstruction, two-row length version, DP vs brute force for lengths 5–18, line diff |
| Q4 | `src/q4_optimal_bst.py` | Optimal BST: e and root tables, cost 2.75 (checked two ways), tree structure and drawing |
| — | `data/old.txt`, `data/new.txt` | Sample files for the diff |
| — | `src/timing_utils.py`, `tests/test_lab6.py` | Timing helper, pytest suite |
| — | `results/` | Tables (`.md`, `.csv`), LCS timing graph, Q3 log |

## Key results

- **Q1:** revenues for n = 1–10 are 1, 5, 8, 10, 13, 17, 18, 22, 25, 30. Naive recursion makes exactly 2ⁿ calls (33,554,432 at n = 25, about 6 s). Memoized makes n(n+1)/2 + 1 calls (326). Bottom-up makes no calls, only 325 loop iterations, and is 100,000–200,000× faster than naive.
- **Q2:** the CLRS chain costs 15,125 with order ((A1(A2A3))((A4A5)A6)), against 40,500 left-to-right. `<5,4,6,2,7>` costs 158 with ((A1(A2A3))A4). DP matches brute force on all 7 chains. Left-to-right was 1.6–15.9× worse.
- **Q3:** the LCS of ABCBDAB and BDCABA is BCBA (length 4). Brute force grows as 2ᵐ and is about 13,000× slower than DP at length 18.
- **Q4:** the expected search cost is 2.75, with k2 as the root (the CLRS tree).

The times in the analysis comments come from my run. Yours will differ, but the trends and call counts should match.

> **Before submitting:** edit the AI disclosure at the top of each file so it says how you actually used AI.
