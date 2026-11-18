# Assignment 3 – Fixing a Slow Quicksort

| File | Purpose |
|---|---|
| `sorts.py` | Part A: `quicksort_basic`, `quicksort_improved` (+ helpers) |
| `test_sorts.py` | Part B: brute-force and special-case tests (72 tests, all pass) |
| `report.docx` / `report.pdf` | Report: tables, graphs, recurrence, cutoff, comparison, reflection |
| `benchmark.py` | Part C: regenerates every table/graph in `results/` |
| `count_comparisons.py` | Comparison counts used in Section 5 and the reflection |
| `results/` | Raw CSV timings and the three figures |

Run:
```
pip install pytest matplotlib
python -m pytest -v test_sorts.py     # all tests
python benchmark.py                   # ~4 minutes; writes results/
python count_comparisons.py
```
Timings will differ on your machine; re-run `benchmark.py` and update the report's numbers if you want them to be your own.
