"""
CSF302 Lab 7 - Q1: Activity Selection and Knapsack

  1. Greedy activity selection (earliest finish time). Activities are read as
     (start, finish) pairs from a file (default ../data/activities.txt) or
     typed at the keyboard.
  2. Two other greedy rules (earliest start, shortest duration). Random
     testing finds an input where each selects fewer activities than
     earliest finish.
  3. Fractional knapsack (highest value/weight first)
  4. The same ratio rule on 0/1 knapsack vs an exact DP on random inputs,
     with the worst greedy/optimal ratio found

Activities are half-open intervals [s, f): two are compatible if one
finishes no later than the other starts (f1 <= s2), as in CLRS.

Note: sorted() is used only to put items in greedy order (by finish time,
start time, duration or ratio). Sorting is not the algorithm being studied
here. Results are checked by brute force.

AI disclosure: I used AI (Claude/Anthropic) as a coding assistant to help draft
and review this file. I checked the implementation, tests, and results myself.

Run:  python q1_greedy.py                      (uses ../data/activities.txt)
      python q1_greedy.py FILE                 (your own file: "start finish" per line)
      python q1_greedy.py --keyboard           (type the pairs)
"""
import itertools
import random
import sys

from timing_utils import markdown_table


# ---------------------------------------------------------------------------
# 1-2. Activity selection
# ---------------------------------------------------------------------------
def read_activities(path):
    acts = []
    with open(path) as f:
        for line in f:
            line = line.split("#")[0].strip()
            if line:
                s, fin = map(int, line.replace(",", " ").split())
                if fin < s:
                    raise ValueError(f"finish before start in line: {line}")
                acts.append((s, fin))
    return acts


def read_activities_keyboard():
    n = int(input("Number of activities: "))
    acts = []
    for i in range(n):
        s, fin = map(int, input(f"  activity {i + 1} (start finish): ").replace(",", " ").split())
        acts.append((s, fin))
    return acts


def greedy_select(acts, key):
    """Generic greedy: consider activities in order of `key`; take each one
    that does not overlap anything already taken."""
    chosen = []
    for a in sorted(acts, key=key):
        if all(a[1] <= b[0] or b[1] <= a[0] for b in chosen):
            chosen.append(a)
    return sorted(chosen, key=lambda x: x[1])


def select_earliest_finish(acts):
    """CLRS GREEDY-ACTIVITY-SELECTOR. After sorting by finish time, only the
    last chosen finish time needs checking: Theta(n log n) total."""
    chosen, last_finish = [], float("-inf")
    for s, f in sorted(acts, key=lambda a: a[1]):
        if s >= last_finish:
            chosen.append((s, f))
            last_finish = f
    return chosen


def select_earliest_start(acts):
    return greedy_select(acts, key=lambda a: (a[0], a[1]))


def select_shortest(acts):
    return greedy_select(acts, key=lambda a: (a[1] - a[0], a[0]))


def max_compatible_brute(acts):
    """Exact answer by trying every subset (small n only)."""
    best = 0
    for r in range(len(acts), 0, -1):
        for sub in itertools.combinations(sorted(acts, key=lambda a: a[1]), r):
            if all(sub[i][1] <= sub[i + 1][0] for i in range(r - 1)):
                return r
    return best


def find_counterexample(rule, rng, max_n=6, tries=200_000):
    """Random testing: smallest random input where `rule` picks fewer
    activities than earliest finish. Tries small n first so the example is short."""
    for n in range(2, max_n + 1):
        for _ in range(tries // max_n):
            acts = []
            for _ in range(n):
                s = rng.randint(0, 10)
                acts.append((s, s + rng.randint(1, 6)))
            if len(rule(acts)) < len(select_earliest_finish(acts)):
                return acts
    return None


def activity_part(acts):
    print(f"Activities (start, finish): {acts}")
    chosen = select_earliest_finish(acts)
    print(f"Earliest-finish selection ({len(chosen)} activities): {chosen}")
    if len(acts) <= 15:
        print(f"Brute-force maximum = {max_compatible_brute(acts)}")
    print(f"Earliest-start picks {len(select_earliest_start(acts))}, "
          f"shortest-duration picks {len(select_shortest(acts))}")

    # earliest finish is always optimal: random check against brute force
    rng = random.Random(42)
    for _ in range(2000):
        n = rng.randint(1, 8)
        test = [(s, s + rng.randint(1, 8)) for s in (rng.randint(0, 15) for _ in range(n))]
        assert len(select_earliest_finish(test)) == max_compatible_brute(test)
    print("Earliest finish == brute-force optimum on 2,000 random inputs.")

    print("\nCounterexamples found by random testing (seed 42):")
    rng = random.Random(42)
    lines = []
    for name, rule in [("earliest start", select_earliest_start),
                       ("shortest duration", select_shortest)]:
        ex = find_counterexample(rule, rng)
        r_sel, f_sel = rule(ex), select_earliest_finish(ex)
        msg = (f"  {name:<17}: input {ex}\n"
               f"      {name} picks {len(r_sel)}: {r_sel}\n"
               f"      earliest finish picks {len(f_sel)}: {f_sel}")
        print(msg)
        lines.append(msg)
    return lines


# ---------------------------------------------------------------------------
# 3. Fractional knapsack
# ---------------------------------------------------------------------------
def fractional_knapsack(items, capacity):
    """items: list of (value, weight). Take items in decreasing value/weight
    order, splitting the last one. Returns (total value, [(index, fraction)])."""
    order = sorted(range(len(items)), key=lambda i: items[i][0] / items[i][1], reverse=True)
    total, taken, room = 0.0, [], capacity
    for i in order:
        if room <= 0:
            break
        v, w = items[i]
        frac = min(1.0, room / w)
        total += frac * v
        room -= frac * w
        taken.append((i, frac))
    return total, taken


# ---------------------------------------------------------------------------
# 4. 0/1 knapsack: greedy-by-ratio vs DP
# ---------------------------------------------------------------------------
def greedy_01(items, capacity):
    """Same ratio rule, but whole items only: take an item if it still fits."""
    order = sorted(range(len(items)), key=lambda i: items[i][0] / items[i][1], reverse=True)
    total, room, chosen = 0, capacity, []
    for i in order:
        v, w = items[i]
        if w <= room:
            total += v
            room -= w
            chosen.append(i)
    return total, chosen


def dp_01(items, capacity):
    """Exact 0/1 knapsack, one-row table: best[c] = max value with weight <= c.
    Theta(n W) time."""
    best = [0] * (capacity + 1)
    for v, w in items:
        for c in range(capacity, w - 1, -1):        # backwards: each item used once
            if best[c - w] + v > best[c]:
                best[c] = best[c - w] + v
    return best[capacity]


def knapsack_part(trials=20_000):
    items = [(60, 10), (100, 20), (120, 30)]          # CLRS example, W = 50
    W = 50
    val, taken = fractional_knapsack(items, W)
    print(f"Fractional knapsack, items (value, weight) = {items}, W = {W}")
    print(f"  take {[(i + 1, round(f, 3)) for i, f in taken]} (item, fraction)  -> value {val:.1f}")
    g, _ = greedy_01(items, W)
    print(f"  Same items as 0/1: greedy = {g}, DP optimum = {dp_01(items, W)}")

    rng = random.Random(42)
    worst = (1.0, None)
    ratios = []
    for _ in range(trials):
        n = rng.randint(2, 10)
        its = [(rng.randint(1, 100), rng.randint(1, 50)) for _ in range(n)]
        cap = rng.randint(1, sum(w for _, w in its))
        opt = dp_01(its, cap)
        if opt == 0:
            continue
        g, _ = greedy_01(its, cap)
        assert g <= opt and fractional_knapsack(its, cap)[0] >= opt - 1e-9
        ratios.append(g / opt)
        if g / opt < worst[0]:
            worst = (g / opt, (its, cap, g, opt))
    ratio, (its, cap, g, opt) = worst
    below = sum(r < 1 for r in ratios)
    print(f"\n0/1 knapsack, {len(ratios):,} random instances (n = 2..10, seed 42):")
    print(f"  greedy optimal in {len(ratios) - below:,} ({(len(ratios) - below) / len(ratios):.1%}), "
          f"average ratio {sum(ratios) / len(ratios):.4f}")
    print(f"  WORST ratio greedy/optimal = {ratio:.4f}")
    print(f"     items (value, weight) = {its}, W = {cap}: greedy {g}, optimal {opt}")
    # The ratio can be made arbitrarily bad:
    for big in (10, 100, 1000):
        its = [(2, 1), (big, big)]
        print(f"  adversarial {its}, W = {big}: greedy {greedy_01(its, big)[0]}, optimal "
              f"{dp_01(its, big)} -> ratio {greedy_01(its, big)[0] / dp_01(its, big):.4f}")
    return ratio


def main():
    if "--keyboard" in sys.argv:
        acts = read_activities_keyboard()
    else:
        path = next((a for a in sys.argv[1:] if not a.startswith("--")), "../data/activities.txt")
        acts = read_activities(path)
    print("=== Q1.1-1.2 Activity selection ===")
    lines = activity_part(acts)
    print("\n=== Q1.3-1.4 Knapsack ===")
    knapsack_part()
    with open("../results/q1_counterexamples.txt", "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------------------------
# Analysis / conclusion
#
# Activity selection (CLRS 11 activities): earliest finish picks 4 activities
# {(1,4), (5,7), (8,11), (12,16)}, which equals the brute-force maximum. It also
# matched brute force on 2,000 random inputs. Why it is optimal: the activity
# that finishes first leaves the most room for the rest (exchange argument).
# Any optimal solution can swap its first activity for this one and stay
# valid, so the greedy choice is always safe.
#
# Counterexamples found by random testing (seed 42):
#  - Earliest start, input [(5,6), (6,12), (4,8)]: it takes (4,8) first
#    because that starts earliest, and (4,8) overlaps both others -> 1
#    activity, while earliest finish takes (5,6), (6,12) -> 2.
#    An early start says nothing about how long the activity blocks the room.
#  - Shortest duration, input [(6,10), (4,7), (1,5)]: the shortest activity
#    (4,7) overlaps both longer ones -> 1, while earliest finish takes (1,5),
#    (6,10) -> 2. A short activity can sit across two compatible ones.
#    (On the CLRS input shortest duration happens to find 4 as well, which
#    shows why random testing is needed to expose the flaw.)
#
# Fractional knapsack (CLRS items, W = 50): take items 1 and 2 whole and 2/3
# of item 3 -> 240. This is optimal because any unit of capacity is best
# spent on the highest value/weight item still available. Theta(n log n).
#
# 0/1 knapsack with the same rule: on the CLRS items greedy gets 160 but the
# optimum is 220 (items 2+3). Over 18,509 random instances (all-zero optima
# skipped), greedy was optimal 80.7% of the time with an average ratio of
# 0.983. The WORST ratio found was 0.129: items [(55,49), (4,1), (31,23)],
# W = 23. Greedy takes the small high-ratio item (4,1), and then (31,23) no
# longer fits -> 4 instead of 31. The adversarial family [(2,1), (B,B)],
# W = B gives ratio 2/B, so the greedy ratio can be made as close to 0 as we
# like. The greedy-choice property fails for 0/1 items because the leftover
# capacity cannot be filled with a fraction. That is why 0/1 knapsack needs
# DP (Theta(nW)).
# ---------------------------------------------------------------------------
