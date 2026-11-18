"""count_comparisons.py - counts key comparisons, to separate the effect of
the ALGORITHM (number of comparisons) from the LANGUAGE (cost per step)."""
import random
from sorts import quicksort_improved, max_depth_basic, max_depth_improved

class C:
    __slots__ = ("v",)
    n = 0
    def __init__(self, v): self.v = v
    def __lt__(s, o): C.n += 1; return s.v < o.v
    def __gt__(s, o): C.n += 1; return s.v > o.v
    def __le__(s, o): C.n += 1; return s.v <= o.v
    def __eq__(s, o): C.n += 1; return s.v == o.v

random.seed(7)
n = 64000
for kind, data in [("random", [random.randint(0, 10**6) for _ in range(n)]),
                   ("sorted", list(range(n))),
                   ("dups 0-9", [random.randint(0, 9) for _ in range(n)])]:
    a = [C(x) for x in data]; C.n = 0; quicksort_improved(a, 16); q = C.n
    a = [C(x) for x in data]; C.n = 0; a.sort(); s = C.n   # reference only
    print(f"{kind:9s} improved={q:>9,}  sorted()={s:>9,}  ratio={q/s:.2f}")
m = 4000   # depth simulation of the basic sort is itself Theta(n^2)
print(f"recursion depth, n={m:,} sorted: basic", max_depth_basic(list(range(m))),
      " improved", max_depth_improved(list(range(m))))
print(f"recursion depth, n={n:,} sorted: improved", max_depth_improved(list(range(n))),
      "(basic would need n-1 = {:,})".format(n - 1))
