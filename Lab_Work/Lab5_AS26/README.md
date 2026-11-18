# CSF302 Lab 5: Sorting Algorithms

Python 3.11+ is required. There is one source file per question. Each file starts with an AI disclosure and ends with an analysis/conclusion comment that uses the measured numbers.

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
python q1_quicksort.py              # ~5 min (add --quick for 1 repeat; --plot-only to redraw the graph)
python q2_counting_radix.py         # ~1-2 min
python q3_inversions.py             # menu: 1 verify, 2 timing (~3 min), 3 Kendall tau
python q3_inversions.py kendall     # go straight to the keyboard-input Kendall tau part
cd ..
pytest -q                           # 37 tests
```

## Files

| Question | File | Contents |
|---|---|---|
| Q1 | `src/q1_quicksort.py` | Lomuto (last pivot), Hoare (first pivot), randomised, and 3-way quicksort. Recurses on the smaller part and loops on the larger. Counts comparisons and times 4 input types × n = 1k–16k |
| Q2 | `src/q2_counting_radix.py` | Stable counting sort, LSD radix sort (base 10 and 256), the k- and n-experiments, plots, and the stability demo with (key, index) pairs |
| Q2 | `src/merge_sort.py` | Lab 1 merge sort used as the baseline (step counter removed) |
| Q3 | `src/q3_inversions.py` | Brute-force and merge-based inversion counts, verification, timing with a 60 s cutoff, and Kendall tau from keyboard input |
| — | `src/timing_utils.py` | Timing helper (copies input outside the timer, median of 3) |
| — | `tests/test_lab5.py` | pytest suite |
| — | `results/` | Tables (`.md`, `.csv`), graphs (`.png`) and run logs |

## Key results

**Q1:** the variants that degrade to Θ(n²) (about n²/2 comparisons) are:
- Lomuto on sorted and reverse-sorted input.
- Hoare on sorted and reverse-sorted input.
- Lomuto and randomised on many-duplicates input (about n²/20).

Three-way quicksort with a random pivot stays Θ(n log n) on every input type, and it is fastest on duplicates.

**Q2:** counting sort is 5–25× faster than merge sort when k ≤ n, and 4× slower at k = 100n. Radix base 256 (4 passes) beats base 10 (10 passes) by about 2×, and beats merge sort at every n.

**Q3:**
- **Brute force:** reached 54 s at n = 50,000 and passed 60 s at n = 100,000, so it was stopped there.
- **Merge-based:** counts all inversions for n = 10⁶ (about 2.5 × 10¹¹) in about 3 s.

The times in the analysis comments come from my run. Yours will differ, but the trends and the deterministic comparison counts should match.

> **Before submitting:** edit the AI disclosure at the top of each file so it says how you actually used AI. If your own Lab 1 merge sort differs, paste it into `src/merge_sort.py`; it only needs to provide `merge_sort(list) -> sorted list`.
