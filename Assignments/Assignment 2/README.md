# Assignment 2: Closest Camera Traps

| File | Part |
|---|---|
| `closest.py` | A: `closest_pair_brute` and `closest_pair` (divide and conquer) |
| `test_closest.py` | B: 717 pytest cases, all passing |
| `benchmark.py` | C: timings, crossover search, graph |
| `timings.csv`, `crossover.csv`, `bench_log.txt`, `timing_loglog.png` | C: raw results and graph |
| `report.docx` / `report.pdf` | Report: recurrence, table, graph, crossover, reflection |

## Run

    python closest.py                    # example from the brief
    python -m pytest -v test_closest.py  # all tests
    python benchmark.py                  # full timings (about 2 minutes)
    python benchmark.py --plot-only      # redraw graph from the CSV files

Requires Python 3.8+, `pytest`, and `matplotlib` (for the graph only).
