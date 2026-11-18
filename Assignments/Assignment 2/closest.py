"""
Assignment 2: Closest Camera Traps

Find the two camera traps that are closest together on the map grid.

    closest_pair_brute(points) -> (d, i, j)   Theta(n^2), checks every pair
    closest_pair(points)       -> (d, i, j)   Theta(n log n), divide and conquer

`points` is a list of n >= 2 (x, y) pairs. `d` is the smallest Euclidean
distance and i < j are the indices of the two points in the ORIGINAL list.
If several pairs share the smallest distance, either function may return any
one of them; `d` is always the same.

Internally both functions compare SQUARED distances (dx*dx + dy*dy) and only
take one square root at the end. This avoids thousands of sqrt calls and,
for integer coordinates, keeps every comparison exact.
"""

import math


def _check_input(points):
    if len(points) < 2:
        raise ValueError("need at least 2 points, got %d" % len(points))


def _sq_dist(p, q):
    dx = p[0] - q[0]
    dy = p[1] - q[1]
    return dx * dx + dy * dy


# --------------------------------------------------------------------------
# Part A (1): brute force
# --------------------------------------------------------------------------
def closest_pair_brute(points):
    """Compare every pair of points. n(n-1)/2 comparisons -> Theta(n^2)."""
    _check_input(points)
    n = len(points)
    best, bi, bj = math.inf, 0, 1
    for i in range(n - 1):
        xi, yi = points[i]
        for j in range(i + 1, n):
            dx = xi - points[j][0]
            dy = yi - points[j][1]
            d2 = dx * dx + dy * dy
            if d2 < best:
                best, bi, bj = d2, i, j
    return math.sqrt(best), bi, bj


# --------------------------------------------------------------------------
# Part A (2): divide and conquer
# --------------------------------------------------------------------------
def closest_pair(points):
    """
    Divide and conquer closest pair.

    1. Sort the indices by x once:                     O(n log n)
    2. Recursively, on a range of the x-sorted list:
         - split at the middle point (vertical line x = mid_x)
         - solve the left and right halves              2 T(n/2)
         - merge the two halves' y-sorted lists         O(n)
         - delta = best distance from the two halves
         - check the strip |x - mid_x| < delta, in y order;
           each point is compared only with the next points whose
           y differs by less than delta (at most 7 of them)  O(n)
    Recurrence: T(n) = 2 T(n/2) + Theta(n)  ->  Theta(n log n).
    """
    _check_input(points)
    pts = points
    order = sorted(range(len(pts)), key=lambda k: (pts[k][0], pts[k][1]))

    # best = [squared distance, i, j]; shared by every recursive call so the
    # strip can use the best answer found anywhere so far.
    best = [math.inf, 0, 1]

    def consider(a, b):
        d2 = _sq_dist(pts[a], pts[b])
        if d2 < best[0]:
            best[0], best[1], best[2] = d2, a, b

    def solve(lo, hi):
        """Solve order[lo:hi]; return those indices sorted by y."""
        n = hi - lo
        if n <= 3:                                   # base case: brute force
            for s in range(lo, hi - 1):
                for t in range(s + 1, hi):
                    consider(order[s], order[t])
            return sorted(order[lo:hi], key=lambda k: pts[k][1])

        mid = (lo + hi) // 2
        mid_x = pts[order[mid]][0]                   # dividing line
        left = solve(lo, mid)
        right = solve(mid, hi)

        # merge the two y-sorted halves (merge step of merge sort)
        by_y = []
        a = b = 0
        while a < len(left) and b < len(right):
            if pts[left[a]][1] <= pts[right[b]][1]:
                by_y.append(left[a]); a += 1
            else:
                by_y.append(right[b]); b += 1
        by_y.extend(left[a:])
        by_y.extend(right[b:])

        # strip of width 2*delta around x = mid_x (compare squared values)
        strip = [k for k in by_y if (pts[k][0] - mid_x) ** 2 < best[0]]
        for s in range(len(strip)):
            ys = pts[strip[s]][1]
            t = s + 1
            while t < len(strip) and (pts[strip[t]][1] - ys) ** 2 < best[0]:
                consider(strip[s], strip[t])
                t += 1
        return by_y

    solve(0, len(pts))
    d2, i, j = best
    if i > j:
        i, j = j, i
    return math.sqrt(d2), i, j


if __name__ == "__main__":
    traps = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]
    print("brute force      :", closest_pair_brute(traps))
    print("divide & conquer :", closest_pair(traps))
