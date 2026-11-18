"""
search.py
----------
Q3: Binary Search vs Ternary Search (Menu-Driven Program)

Binary Search:  T(n) = T(n/2) + O(1)   ->  O(log2 n)
Ternary Search: T(n) = T(n/3) + O(1)   ->  O(log3 n)

Ternary Search splits the array into 3 parts instead of 2, so it needs
fewer *rounds* (log base 3 grows slower than log base 2). But each
round it makes more comparisons than Binary Search (checking 2 middle
points instead of 1). In practice this usually means Ternary Search
ends up doing MORE total comparisons than Binary Search, even though
it has fewer recursive levels. Option 7 in the menu below lets you see
this for yourself.

Run this file directly: python3 search.py
"""

import random


def generate_sorted_array(n, low=1, high=1000):
    """Generate n sorted, unique random integers."""
    count = min(n, high - low + 1)
    numbers = random.sample(range(low, high + 1), count)
    numbers.sort()
    return numbers


def binary_search(arr, key):
    """
    Standard iterative binary search.
    Returns (index_or_minus_1, number_of_comparisons).
    """
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2

        comparisons += 1
        if arr[mid] == key:
            return mid, comparisons

        comparisons += 1
        if arr[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


def ternary_search(arr, key):
    """
    Standard iterative ternary search.
    Returns (index_or_minus_1, number_of_comparisons).
    """
    low, high = 0, len(arr) - 1
    comparisons = 0

    while low <= high:
        third = (high - low) // 3
        mid1 = low + third
        mid2 = high - third

        comparisons += 1
        if arr[mid1] == key:
            return mid1, comparisons

        comparisons += 1
        if arr[mid2] == key:
            return mid2, comparisons

        comparisons += 1
        if key < arr[mid1]:
            high = mid1 - 1
        else:
            comparisons += 1
            if key > arr[mid2]:
                low = mid2 + 1
            else:
                low, high = mid1 + 1, mid2 - 1

    return -1, comparisons


def display_array(arr):
    if not arr:
        print("Array is empty. Please generate one first (menu option 1).")
        return
    print(arr)


def best_case_demo(arr):
    """Best case: the key is found on the very first check."""
    if not arr:
        print("Array is empty. Please generate one first (menu option 1).")
        return
    mid = len(arr) // 2
    key = arr[mid]          # binary search will find this on its first check
    b_idx, b_count = binary_search(arr, key)
    t_idx, t_count = ternary_search(arr, key)
    print(f"Best-case key chosen: {key}")
    print(f"Binary Search  -> found at index {b_idx}, comparisons = {b_count}")
    print(f"Ternary Search -> found at index {t_idx}, comparisons = {t_count}")


def worst_case_demo(arr):
    """Worst case: the key does not exist in the array."""
    if not arr:
        print("Array is empty. Please generate one first (menu option 1).")
        return
    key = arr[-1] + 1        # guaranteed to be absent, since arr is sorted+unique
    b_idx, b_count = binary_search(arr, key)
    t_idx, t_count = ternary_search(arr, key)
    print(f"Worst-case key chosen (not present): {key}")
    print(f"Binary Search  -> found at index {b_idx}, comparisons = {b_count}")
    print(f"Ternary Search -> found at index {t_idx}, comparisons = {t_count}")


def comparison_table():
    """Show a worst-case comparisons table for increasing n."""
    sizes = [10, 100, 1000, 10000, 100000]
    print(f"{'n':>8} | {'Binary comparisons':>19} | {'Ternary comparisons':>20}")
    print("-" * 55)
    for n in sizes:
        arr = generate_sorted_array(n, low=1, high=n * 10)
        key = 0  # guaranteed absent, since generate_sorted_array uses low=1 upward
        _, b_count = binary_search(arr, key)
        _, t_count = ternary_search(arr, key)
        print(f"{n:>8} | {b_count:>19} | {t_count:>20}")

    print()
    print("Analysis: Binary Search does fewer total comparisons than Ternary")
    print("Search here, even though Ternary needs fewer rounds (log3 n < log2 n),")
    print("because each Ternary round costs up to 4 comparisons vs Binary's 2.")


def print_menu():
    print("\n" + "=" * 55)
    print("  BINARY SEARCH vs TERNARY SEARCH - MENU")
    print("=" * 55)
    print("1. Generate n sorted random numbers -> Array")
    print("2. Display Array")
    print("3. Search for a key using Binary Search")
    print("4. Search for a key using Ternary Search")
    print("5. Step/frequency count for BEST case")
    print("6. Step/frequency count for WORST case")
    print("7. Step/frequency count comparison table across increasing n")
    print("8. Exit")


def main():
    arr = []
    while True:
        print_menu()
        choice = input("Enter your choice (1-8): ").strip()

        if choice == '1':
            n = int(input("Enter number of elements (n): "))
            arr = generate_sorted_array(n)
            print(f"Generated {len(arr)} sorted numbers.")

        elif choice == '2':
            display_array(arr)

        elif choice == '3':
            if not arr:
                print("Array is empty. Please generate one first (menu option 1).")
                continue
            key = int(input("Enter key to search: "))
            idx, count = binary_search(arr, key)
            if idx != -1:
                print(f"Found at index {idx}. Comparisons made: {count}")
            else:
                print(f"Key not found. Comparisons made: {count}")

        elif choice == '4':
            if not arr:
                print("Array is empty. Please generate one first (menu option 1).")
                continue
            key = int(input("Enter key to search: "))
            idx, count = ternary_search(arr, key)
            if idx != -1:
                print(f"Found at index {idx}. Comparisons made: {count}")
            else:
                print(f"Key not found. Comparisons made: {count}")

        elif choice == '5':
            best_case_demo(arr)

        elif choice == '6':
            worst_case_demo(arr)

        elif choice == '7':
            comparison_table()

        elif choice == '8':
            print("Goodbye!")
            break

        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()

# ---------------------------------------------------------
# Analysis / Conclusion
# ---------------------------------------------------------
# Binary Search:  T(n) = T(n/2) + O(1)  -> O(log2 n) comparisons
# Ternary Search: T(n) = T(n/3) + O(1)  -> O(log3 n) comparisons
#
# log3(n) is smaller than log2(n) for the same n, so Ternary Search
# needs fewer recursive "rounds" to narrow down the search range.
# However, each round of Ternary Search checks two midpoints and can
# make up to 4 comparisons, while each round of Binary Search checks
# one midpoint and makes at most 2 comparisons. The extra work per
# round outweighs the savings from having fewer rounds, so in
# practice Binary Search usually wins on total comparison count.
