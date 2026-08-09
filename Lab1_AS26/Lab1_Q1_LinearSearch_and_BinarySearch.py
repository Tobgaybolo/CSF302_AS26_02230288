"""
Question 1: Linear Search vs Binary Search
Empirical growth-rate measurement.
"""

import random
import time
import statistics


# ---------- Algorithms ----------

def linear_search_288(arr_288, target_288):
    for i_288, val_288 in enumerate(arr_288):
        if val_288 == target_288:
            return i_288
    return -1


def binary_search_288(arr_288, target_288):
    lo_288, hi_288 = 0, len(arr_288) - 1
    while lo_288 <= hi_288:
        mid_288 = (lo_288 + hi_288) // 2
        if arr_288[mid_288] == target_288:
            return mid_288
        elif arr_288[mid_288] < target_288:
            lo_288 = mid_288 + 1
        else:
            hi_288 = mid_288 - 1
    return -1


# ---------- Benchmarking ----------

def make_dataset_288(n_288, seed_288=42):
    rng_288 = random.Random(seed_288)
    # unique values so a search target is guaranteed findable
    return rng_288.sample(range(n_288 * 10), n_288)


def time_it_288(func_288, *args_288, trials_288=5):
    """Run func_288 several times, return average elapsed seconds."""
    times_288 = []
    for _ in range(trials_288):
        start_288 = time.perf_counter()
        func_288(*args_288)
        end_288 = time.perf_counter()
        times_288.append(end_288 - start_288)
    return statistics.mean(times_288)


def benchmark_288(sizes_288, trials_288=5, worst_case_288=True):
    results_288 = []
    for n_288 in sizes_288:
        data_288 = make_dataset_288(n_288)

        # target: worst case = not present (forces full scan / full log2 n comparisons)
        target_288 = -1 if worst_case_288 else data_288[len(data_288) // 2]

        # Linear search on the UNSORTED data (its natural use case)
        lin_time_288 = time_it_288(linear_search_288, data_288, target_288, trials_288=trials_288)

        # Binary search requires sorted data -- sort first, time sort separately
        sort_start_288 = time.perf_counter()
        sorted_data_288 = sorted(data_288)
        sort_time_288 = time.perf_counter() - sort_start_288

        bin_time_288 = time_it_288(binary_search_288, sorted_data_288, target_288, trials_288=trials_288)

        results_288.append({
            "n_288": n_288,
            "linear_search_sec_288": lin_time_288,
            "sort_sec_288": sort_time_288,
            "binary_search_sec_288": bin_time_288,
        })
        print(f"n_288={n_288:>9} | linear_288={lin_time_288:.6f}s | sort_288={sort_time_288:.6f}s | binary_288={bin_time_288:.6f}s")
    return results_288


if __name__ == "__main__":
    SIZES_288 = [1_000, 5_000, 10_000, 50_000, 100_000, 500_000, 1_000_000]
    # NOTE: trials=5 for smaller sizes is fine; drop to 1-2 for the biggest
    # sizes if it's too slow on your machine (linear search on 1,000,000
    # unsorted elements, repeated 5x, is the expensive part).
    results_288 = benchmark_288(SIZES_288, trials_288=3)
    print("\nBenchmarking complete.")
