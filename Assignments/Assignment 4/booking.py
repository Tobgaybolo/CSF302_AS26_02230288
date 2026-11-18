"""
Assignment 4: Booking the Hall

Weighted interval scheduling for a community hall in Paro.

Each request is a tuple (start, finish, fee). Two requests fit together if
one finishes no later than the other starts, so an event ending at 12 and
one starting at 12 can both be accepted.

Every function returns (total_fee, chosen), where `chosen` is the list of
indices (into the ORIGINAL `requests` list) of the accepted requests, in
increasing order.
"""

from bisect import bisect_right
from itertools import combinations


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def _validate(requests):
    """Reject malformed input early so every function sees the same data."""
    for i, req in enumerate(requests):
        if len(req) != 3:
            raise ValueError(f"request {i} must be (start, finish, fee), got {req!r}")
        start, finish, fee = req
        if finish < start:
            raise ValueError(f"request {i} finishes before it starts: {req!r}")
        if fee < 0:
            raise ValueError(f"request {i} has a negative fee: {req!r}")


def fits(a, b):
    """True if bookings a and b can both use the hall (touching ends allowed)."""
    return a[1] <= b[0] or b[1] <= a[0]


def _finish_order(requests):
    """Indices sorted by (finish, start).

    Sorting ties by start puts a zero-length event at time t after any
    longer event that also finishes at t, which keeps p(j) correct.
    """
    return sorted(range(len(requests)), key=lambda i: (requests[i][1], requests[i][0]))


# --------------------------------------------------------------------------
# Greedy rule 1: earliest finish (the manager's current rule)
# --------------------------------------------------------------------------

def greedy_earliest_finish(requests):
    """Sort by finish time and accept every request that fits.

    Because requests are taken in finish order, a request fits if and only
    if it starts no earlier than the finish of the last accepted request.

    Time O(n log n) (sort), extra space O(n).
    """
    _validate(requests)
    chosen = []
    total = 0
    last_finish = float("-inf")
    for i in _finish_order(requests):
        start, finish, fee = requests[i]
        if start >= last_finish:
            chosen.append(i)
            total += fee
            last_finish = finish
    return total, sorted(chosen)


# --------------------------------------------------------------------------
# Greedy rule 2: highest fee first
# --------------------------------------------------------------------------

def greedy_highest_fee(requests):
    """Sort by fee (highest first) and accept every request that fits.

    Accepted requests are not taken in time order, so a new request must be
    checked against every booking already accepted.

    Time O(n log n + n*k) where k is the number accepted; O(n^2) worst case.
    """
    _validate(requests)
    # Ties on fee are broken by earlier finish, then by index (deterministic).
    order = sorted(range(len(requests)),
                   key=lambda i: (-requests[i][2], requests[i][1], i))
    chosen = []
    total = 0
    for i in order:
        if all(fits(requests[i], requests[j]) for j in chosen):
            chosen.append(i)
            total += requests[i][2]
    return total, sorted(chosen)


# --------------------------------------------------------------------------
# Dynamic programming: weighted interval scheduling
# --------------------------------------------------------------------------

def best_schedule(requests):
    """Maximum-revenue schedule by dynamic programming.

    Sort requests by finish time and number them 1..n in that order.
    p(j) = the largest i < j whose request finishes no later than request j
    starts (0 if there is none).

        OPT(0) = 0
        OPT(j) = max(OPT(j-1),  fee_j + OPT(p(j)))

    OPT(n) is the best total. Walking back from j = n recovers the chosen
    requests: if taking j is at least as good as skipping it, take j and
    jump to p(j); otherwise move to j-1.

    Time O(n log n): sorting plus one binary search per request for p(j);
    the table fill and reconstruction are O(n). Space O(n).
    """
    _validate(requests)
    n = len(requests)
    order = _finish_order(requests)              # position -> original index
    starts = [requests[i][0] for i in order]
    finishes = [requests[i][1] for i in order]
    fees = [requests[i][2] for i in order]

    # p[j] for j = 1..n (1-based). bisect_right counts how many of the first
    # j-1 finishes are <= start_j, which is exactly the 1-based index of the
    # last compatible request (0 if none). hi=j-1 keeps p(j) < j.
    p = [0] * (n + 1)
    for j in range(1, n + 1):
        p[j] = bisect_right(finishes, starts[j - 1], 0, j - 1)

    opt = [0] * (n + 1)
    for j in range(1, n + 1):
        opt[j] = max(opt[j - 1], fees[j - 1] + opt[p[j]])

    # Reconstruction
    chosen = []
    j = n
    while j > 0:
        if fees[j - 1] + opt[p[j]] >= opt[j - 1]:
            chosen.append(order[j - 1])
            j = p[j]
        else:
            j -= 1
    return opt[n], sorted(chosen)


# --------------------------------------------------------------------------
# Brute force (checking only)
# --------------------------------------------------------------------------

def _compatible(requests, subset):
    """True if every pair in `subset` fits. Sorting by finish lets us check
    neighbours only: O(k log k)."""
    ordered = sorted(subset, key=lambda i: (requests[i][1], requests[i][0]))
    for a, b in zip(ordered, ordered[1:]):
        if requests[a][1] > requests[b][0]:
            return False
    return True


def brute_force(requests):
    """Try every subset and keep the best feasible one. For n <= 15 only.

    Time O(2^n * n log n), space O(n).
    """
    _validate(requests)
    n = len(requests)
    if n > 15:
        raise ValueError("brute_force is only for checking small inputs (n <= 15)")
    best_total, best_set = 0, []
    for size in range(1, n + 1):
        for subset in combinations(range(n), size):
            total = sum(requests[i][2] for i in subset)
            if total > best_total and _compatible(requests, subset):
                best_total, best_set = total, list(subset)
    return best_total, best_set


def is_valid_schedule(requests, chosen):
    """Helper for tests: indices are distinct, in range and pairwise compatible."""
    if len(set(chosen)) != len(chosen):
        return False
    if any(not 0 <= i < len(requests) for i in chosen):
        return False
    # Deliberately checks every pair directly (independent of _compatible).
    return all(fits(requests[a], requests[b]) for a, b in combinations(chosen, 2))


if __name__ == "__main__":
    requests = [(9, 12, 3000), (10, 16, 8000), (13, 17, 4000),
                (12, 14, 2500), (16, 18, 2000)]
    print("greedy_earliest_finish:", greedy_earliest_finish(requests))
    print("greedy_highest_fee:    ", greedy_highest_fee(requests))
    print("best_schedule:         ", best_schedule(requests))
    print("brute_force:           ", brute_force(requests))
