"""
Question 2: Bubble Sort vs Merge Sort
Empirical growth-rate measurement.
"""

import random
import time
import statistics


# ---------- Algorithms ----------

def bubble_sort_288(arr_288):
    a_288 = arr_288[:]  # don't mutate caller's list
    n_288 = len(a_288)
    for i_288 in range(n_288 - 1):
        swapped_288 = False
        for j_288 in range(n_288 - 1 - i_288):
            if a_288[j_288] > a_288[j_288 + 1]:
                a_288[j_288], a_288[j_288 + 1] = a_288[j_288 + 1], a_288[j_288]
                swapped_288 = True
        if not swapped_288:
            break
    return a_288


def merge_sort_288(arr_288):
    if len(arr_288) <= 1:
        return arr_288[:]
    mid_288 = len(arr_288) // 2
    left_288 = merge_sort_288(arr_288[:mid_288])
    right_288 = merge_sort_288(arr_288[mid_288:])
    return _merge_288(left_288, right_288)


def _merge_288(left_288, right_288):
    result_288 = []
    i_288 = j_288 = 0
    while i_288 < len(left_288) and j_288 < len(right_288):
        if left_288[i_288] <= right_288[j_288]:
            result_288.append(left_288[i_288])
            i_288 += 1
        else:
            result_288.append(right_288[j_288])
            j_288 += 1
    result_288.extend(left_288[i_288:])
    result_288.extend(right_288[j_288:])
    return result_288


# ---------- Benchmarking ----------

def make_dataset_288(n_288, seed_288=42):
    rng_288 = random.Random(seed_288)
    return [rng_288.randint(0, n_288 * 10) for _ in range(n_288)]


def time_it_288(func_288, arr_288, trials_288=5):
    times_288 = []
    for _ in range(trials_288):
        start_288 = time.perf_counter()
        func_288(arr_288)
        end_288 = time.perf_counter()
        times_288.append(end_288 - start_288)
    return statistics.mean(times_288)


def benchmark_288(sizes_288, trials_288=5):
    results_288 = []
    for n_288 in sizes_288:
        data_288 = make_dataset_288(n_288)

        bubble_time_288 = time_it_288(bubble_sort_288, data_288, trials_288=trials_288)
        merge_time_288 = time_it_288(merge_sort_288, data_288, trials_288=trials_288)

        results_288.append({
            "n_288": n_288,
            "bubble_sort_sec_288": bubble_time_288,
            "merge_sort_sec_288": merge_time_288,
        })
        print(f"n_288={n_288:>6} | bubble_288={bubble_time_288:.6f}s | merge_288={merge_time_288:.6f}s")
    return results_288


if __name__ == "__main__":
    SIZES_288 = [100, 500, 1000, 2000, 4000, 8000]
    # Bubble sort is O(n^2) -- 8000 elements already takes a couple seconds
    # in pure Python. Don't push bubble sort's input size much higher.
    results_288 = benchmark_288(SIZES_288, trials_288=5)
    print("\nBenchmarking complete.")
