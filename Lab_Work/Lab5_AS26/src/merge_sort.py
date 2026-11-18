"""
CSF302 Lab 5 - Merge sort carried over from Lab 1 (used as the comparison
baseline in Q2).

Same top-down algorithm as the Lab 1 version: split in half, sort each half
recursively, merge with `<=` so equal keys keep their order (stable).
The Lab 1 step-counter global has been removed so it does not affect timing.
If your own Lab 1 code differs, you can paste it here; Q2 only needs
merge_sort(list) -> new sorted list.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.
"""


def merge(left, right):
    """Merge two sorted lists into one sorted list (stable)."""
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort(arr):
    """Return a new sorted list. Theta(n log n) time, Theta(n) extra space."""
    if len(arr) <= 1:
        return list(arr)
    mid = len(arr) // 2
    return merge(merge_sort(arr[:mid]), merge_sort(arr[mid:]))
