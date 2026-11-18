"""
CSF302 Lab 4 - shared timing helper.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.
"""
import statistics
import time


def time_call(fn, *args, repeats=3):
    """Return the median wall-clock time (seconds) of fn(*args) over `repeats` runs.

    Arguments are built by the caller, outside the timed region.
    """
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        fn(*args)
        samples.append(time.perf_counter() - start)
    return statistics.median(samples)


def markdown_table(headers, rows):
    """Format rows as a Markdown table string."""
    line = "| " + " | ".join(headers) + " |"
    sep = "| " + " | ".join("---" for _ in headers) + " |"
    body = ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join([line, sep, *body])
