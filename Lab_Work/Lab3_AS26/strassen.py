"""
strassen.py
------------
Strassen's Algorithm for Matrix Multiplication (Divide and Conquer)

Strassen's algorithm multiplies two n x n matrices using only 7
matrix multiplications per split (instead of the 8 you'd need with
the obvious divide-and-conquer approach). This lowers the time
complexity from O(n^3) to about O(n^2.807).

Matrix size (n) must be a power of 2 (2, 4, 8, 16, 32, ...).
"""


def add(A, B):
    """Add two matrices of the same size."""
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def subtract(A, B):
    """Subtract matrix B from matrix A (same size)."""
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def split_matrix(M):
    """Split a matrix into 4 equal quadrants: top-left, top-right, bottom-left, bottom-right."""
    n = len(M)
    mid = n // 2
    top_left = [row[:mid] for row in M[:mid]]
    top_right = [row[mid:] for row in M[:mid]]
    bottom_left = [row[:mid] for row in M[mid:]]
    bottom_right = [row[mid:] for row in M[mid:]]
    return top_left, top_right, bottom_left, bottom_right


def combine_quadrants(C11, C12, C21, C22):
    """Combine 4 quadrants back into a single matrix."""
    top = [C11[i] + C12[i] for i in range(len(C11))]
    bottom = [C21[i] + C22[i] for i in range(len(C21))]
    return top + bottom


def strassen_multiply(A, B):
    """
    Multiply two n x n matrices using Strassen's Algorithm.
    n must be a power of 2.
    """
    n = len(A)

    # Base case: 1x1 matrix -> just multiply the two numbers
    if n == 1:
        return [[A[0][0] * B[0][0]]]

    # Step 1: split A and B into 4 quadrants each
    a11, a12, a21, a22 = split_matrix(A)
    b11, b12, b21, b22 = split_matrix(B)

    # Step 2: compute the 7 products (recursively) instead of 8
    M1 = strassen_multiply(add(a11, a22), add(b11, b22))
    M2 = strassen_multiply(add(a21, a22), b11)
    M3 = strassen_multiply(a11, subtract(b12, b22))
    M4 = strassen_multiply(a22, subtract(b21, b11))
    M5 = strassen_multiply(add(a11, a12), b22)
    M6 = strassen_multiply(subtract(a21, a11), add(b11, b12))
    M7 = strassen_multiply(subtract(a12, a22), add(b21, b22))

    # Step 3: combine the 7 products into the 4 result quadrants
    C11 = add(subtract(add(M1, M4), M5), M7)
    C12 = add(M3, M5)
    C21 = add(M2, M4)
    C22 = add(subtract(add(M1, M3), M2), M6)

    # Step 4: combine quadrants into the final n x n matrix
    return combine_quadrants(C11, C12, C21, C22)


if __name__ == "__main__":
    # Quick self-test with a small 4x4 example
    A = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    B = [[16, 15, 14, 13], [12, 11, 10, 9], [8, 7, 6, 5], [4, 3, 2, 1]]
    result = strassen_multiply(A, B)
    print("Strassen result:")
    for row in result:
        print(row)
