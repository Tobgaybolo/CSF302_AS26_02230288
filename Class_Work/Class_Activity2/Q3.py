"""Square matrix multiplication with a basic operation count."""

import random as random_288


def is_power_of_two_288(number_288):
	"""Return True when the number is a power of two."""
	return number_288 > 0 and (number_288 & (number_288 - 1)) == 0


def read_matrix_288(size_288, matrix_name_288):
	"""Read a matrix from the user one row at a time."""
	matrix_288 = []
	print(f"\nEnter values for {matrix_name_288}:")

	for row_288 in range(size_288):
		while True:
			try:
				values_288 = [int(value_288) for value_288 in input(
					f"Row {row_288 + 1} ({size_288} integers): "
				).split()]
			except ValueError:
				print("Please enter integers only.")
				continue

			if len(values_288) == size_288:
				matrix_288.append(values_288)
				break
			print(f"Please enter exactly {size_288} integers.")

	return matrix_288


def generate_matrix_288(size_288):
	"""Create a matrix containing random integers from 1 to 10."""
	return [
		[random_288.randint(1, 10) for column_288 in range(size_288)]
		for row_288 in range(size_288)
	]


def multiply_matrices_288(first_matrix_288, second_matrix_288, size_288):
	"""Multiply two square matrices and count basic operations."""
	result_matrix_288 = [
		[0 for column_288 in range(size_288)]
		for row_288 in range(size_288)
	]
	operation_count_288 = 0

	for row_288 in range(size_288):
		for column_288 in range(size_288):
			for position_288 in range(size_288):
				result_matrix_288[row_288][column_288] += (
					first_matrix_288[row_288][position_288]
					* second_matrix_288[position_288][column_288]
				)
				operation_count_288 += 2

	return result_matrix_288, operation_count_288


def display_matrix_288(matrix_288):
	"""Display a matrix row by row."""
	for row_288 in matrix_288:
		print(row_288)


def main_288():
	print("Square Matrix Multiplication")

	while True:
		try:
			size_288 = int(input("Enter matrix size (2, 4, 8, ...): "))
		except ValueError:
			print("Please enter a whole number.")
			continue

		if is_power_of_two_288(size_288):
			break
		print("Matrix size must be a positive power of 2, such as 2, 4, or 8.")

	print("\n1. Enter matrices manually")
	print("2. Generate matrices randomly")
	choice_288 = input("Enter your choice: ")

	if choice_288 == "1":
		first_matrix_288 = read_matrix_288(size_288, "Matrix A")
		second_matrix_288 = read_matrix_288(size_288, "Matrix B")
	elif choice_288 == "2":
		first_matrix_288 = generate_matrix_288(size_288)
		second_matrix_288 = generate_matrix_288(size_288)
		print("\nRandom matrices generated.")
	else:
		print("Invalid choice.")
		return

	print("\nMatrix A:")
	display_matrix_288(first_matrix_288)
	print("\nMatrix B:")
	display_matrix_288(second_matrix_288)

	result_matrix_288, operation_count_288 = multiply_matrices_288(
		first_matrix_288, second_matrix_288, size_288
	)
	print("\nResultant matrix (A x B):")
	display_matrix_288(result_matrix_288)
	print(f"\nStep/Frequency count: {operation_count_288}")
	print(f"Basic operations: {size_288} x {size_288} x {size_288} x 2")
	print("\nStep/Frequency Count Table")
	print("Operation\tCount")
	print(f"Multiplications and additions\t{operation_count_288}")


if __name__ == "__main__":
	main_288()
