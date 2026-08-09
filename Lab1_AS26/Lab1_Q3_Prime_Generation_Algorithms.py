"""
Question 3: Prime Generation Algorithms
Naive Trial Division vs Optimized Trial Division (sqrt n) vs Sieve of Eratosthenes.
"""

import time


# ---------- Algorithms ----------

def is_prime_naive_288(n_288):
    """Trial division checking ALL numbers from 2 to n-1."""
    if n_288 < 2:
        return False
    for i_288 in range(2, n_288):
        if n_288 % i_288 == 0:
            return False
    return True


def is_prime_optimized_288(n_288):
    """Trial division checking only up to sqrt(n)."""
    if n_288 < 2:
        return False
    if n_288 in (2, 3):
        return True
    if n_288 % 2 == 0:
        return False
    i_288 = 3
    while i_288 * i_288 <= n_288:
        if n_288 % i_288 == 0:
            return False
        i_288 += 2
    return True


def primes_naive_288(limit_288):
    return [n_288 for n_288 in range(2, limit_288 + 1) if is_prime_naive_288(n_288)]


def primes_optimized_288(limit_288):
    return [n_288 for n_288 in range(2, limit_288 + 1) if is_prime_optimized_288(n_288)]


def primes_sieve_288(limit_288):
    """Sieve of Eratosthenes."""
    if limit_288 < 2:
        return []
    is_p_288 = [True] * (limit_288 + 1)
    is_p_288[0] = is_p_288[1] = False
    for i_288 in range(2, int(limit_288 ** 0.5) + 1):
        if is_p_288[i_288]:
            for multiple_288 in range(i_288 * i_288, limit_288 + 1, i_288):
                is_p_288[multiple_288] = False
    return [i_288 for i_288, prime_288 in enumerate(is_p_288) if prime_288]


# ---------- Benchmarking ----------

def time_it_288(func_288, limit_288):
    start_288 = time.perf_counter()
    result_288 = func_288(limit_288)
    end_288 = time.perf_counter()
    return end_288 - start_288, len(result_288)


def benchmark_288(sizes_288, run_naive_up_to_288=100_000):
    """
    run_naive_up_to_288 caps where we still bother running the naive O(n^2)-ish
    algorithm -- at N=1,000,000 naive trial division for every number is
    extremely slow (can take many minutes), so by default we skip it above
    100,000 and just record it as None. Raise the cap if you have time/patience.
    """
    results_288 = []
    for n_288 in sizes_288:
        row_288 = {"n_288": n_288}

        if n_288 <= run_naive_up_to_288:
            t_naive_288, count_naive_288 = time_it_288(primes_naive_288, n_288)
            row_288["naive_trial_division_sec_288"] = t_naive_288
        else:
            row_288["naive_trial_division_sec_288"] = None
            count_naive_288 = None

        t_opt_288, count_opt_288 = time_it_288(primes_optimized_288, n_288)
        row_288["optimized_trial_division_sec_288"] = t_opt_288

        t_sieve_288, count_sieve_288 = time_it_288(primes_sieve_288, n_288)
        row_288["sieve_of_eratosthenes_sec_288"] = t_sieve_288

        row_288["prime_count_288"] = count_opt_288  # sanity check value
        results_288.append(row_288)

        naive_str_288 = f"{row_288['naive_trial_division_sec_288']:.6f}s" if row_288["naive_trial_division_sec_288"] is not None else "SKIPPED"
        print(f"n_288={n_288:>9} | primes_288={count_opt_288:>6} | naive_288={naive_str_288} | "
              f"optimized_288={t_opt_288:.6f}s | sieve_288={t_sieve_288:.6f}s")

    return results_288


if __name__ == "__main__":
    SIZES_288 = [10_000, 50_000, 100_000, 500_000, 1_000_000]
    results_288 = benchmark_288(SIZES_288, run_naive_up_to_288=100_000)
    print("\nBenchmarking complete.")
