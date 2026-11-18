import random

# comparison counter (using student-id-styled variable name)
count288 = 0

def minmax_288(arr288, lo288, hi288):
    global count288

    # base case 1: single element
    if lo288 == hi288:
        return (arr288[lo288], arr288[lo288])

    # base case 2: exactly two elements
    if hi288 == lo288 + 1:
        count288 += 1
        if arr288[lo288] < arr288[hi288]:
            return (arr288[lo288], arr288[hi288])
        else:
            return (arr288[hi288], arr288[lo288])

    # recursive case: split into two halves
    mid288 = (lo288 + hi288) // 2
    min1_288, max1_288 = minmax_288(arr288, lo288, mid288)
    min2_288, max2_288 = minmax_288(arr288, mid288 + 1, hi288)

    # combine: exactly 2 comparisons
    count288 += 1
    finalMin288 = min1_288 if min1_288 < min2_288 else min2_288

    count288 += 1
    finalMax288 = max1_288 if max1_288 > max2_288 else max2_288

    return (finalMin288, finalMax288)


def closed_form_288(n288):
    # predicted comparisons from our derived formula C(n) = 3n/2 - 2
    return (3 * n288) // 2 - 2


def two_scan_288(n288):
    # the "obvious" method for comparison
    return 2 * n288 - 2


if __name__ == "__main__":
    sizes288 = [8, 64, 512, 4096]
    print(f"{'n':<8}{'Measured':<12}{'Predicted (closed form)':<26}{'2n-2 (two-scan)':<18}")
    for n288 in sizes288:
        arr288 = random.sample(range(1, n288 * 10), n288)  # random distinct numbers
        count288 = 0  # reset counter
        found_min288, found_max288 = minmax_288(arr288, 0, n288 - 1)

        predicted288 = closed_form_288(n288)
        twoscan288 = two_scan_288(n288)

        print(f"{n288:<8}{count288:<12}{predicted288:<26}{twoscan288:<18}")

        # sanity check against python's built-in min/max
        assert found_min288 == min(arr288)
        assert found_max288 == max(arr288)

    print("\nAll results verified correct against Python's built-in min()/max().")
