"""
CSF302 Lab 7 - shared timing helpers.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.
"""
import statistics
import time


def time_sort(sort_fn, data, repeats=3):
    """Median time (s) of sort_fn on a fresh copy of `data` for each repeat.

    The copy is made OUTSIDE the timed region. Returns (median_time, result)
    where result is whatever sort_fn returned on the last run.
    """
    samples, result = [], None
    for _ in range(repeats):
        arr = list(data)                      # untimed copy
        start = time.perf_counter()
        result = sort_fn(arr)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples), result


def markdown_table(headers, rows):
    """Format rows as a Markdown table string."""
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def time_call(fn, *args, repeats=3):
    """Median time (s) of fn(*args) over `repeats` runs; returns (time, result)."""
    samples, result = [], None
    for _ in range(repeats):
        start = time.perf_counter()
        result = fn(*args)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples), result
