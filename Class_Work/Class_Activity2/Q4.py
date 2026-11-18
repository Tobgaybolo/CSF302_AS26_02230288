"""Strassen matrix multiplication with experiment tables and graphs."""

import random as random_288
import time as time_288



def is_power_of_two_288(number_288):
	"""Return True when the number is a positive power of two."""
	return number_288 > 0 and (number_288 & (number_288 - 1)) == 0


def generate_matrix_288(size_288):
	"""Generate a square matrix with random values from 1 to 10."""
	return [
		[random_288.randint(1, 10) for column_288 in range(size_288)]
		for row_288 in range(size_288)
	]


def read_matrix_288(size_288, matrix_name_288):
	"""Read a square matrix manually."""
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


def add_matrices_288(first_matrix_288, second_matrix_288, steps_288):
	"""Add two matrices and count each addition."""
	size_288 = len(first_matrix_288)
	result_matrix_288 = []
	for row_288 in range(size_288):
		result_row_288 = []
		for column_288 in range(size_288):
			result_row_288.append(
				first_matrix_288[row_288][column_288]
				+ second_matrix_288[row_288][column_288]
			)
			steps_288[0] += 1
		result_matrix_288.append(result_row_288)
	return result_matrix_288


def subtract_matrices_288(first_matrix_288, second_matrix_288, steps_288):
	"""Subtract two matrices and count each subtraction."""
	size_288 = len(first_matrix_288)
	result_matrix_288 = []
	for row_288 in range(size_288):
		result_row_288 = []
		for column_288 in range(size_288):
			result_row_288.append(
				first_matrix_288[row_288][column_288]
				- second_matrix_288[row_288][column_288]
			)
			steps_288[0] += 1
		result_matrix_288.append(result_row_288)
	return result_matrix_288


def strassen_288(first_matrix_288, second_matrix_288, steps_288):
	"""Multiply two square matrices using Strassen's algorithm."""
	size_288 = len(first_matrix_288)
	if size_288 == 1:
		steps_288[0] += 1
		return [[first_matrix_288[0][0] * second_matrix_288[0][0]]]

	middle_288 = size_288 // 2
	top_left_a_288 = [row_288[:middle_288] for row_288 in first_matrix_288[:middle_288]]
	top_right_a_288 = [row_288[middle_288:] for row_288 in first_matrix_288[:middle_288]]
	bottom_left_a_288 = [row_288[:middle_288] for row_288 in first_matrix_288[middle_288:]]
	bottom_right_a_288 = [row_288[middle_288:] for row_288 in first_matrix_288[middle_288:]]
	top_left_b_288 = [row_288[:middle_288] for row_288 in second_matrix_288[:middle_288]]
	top_right_b_288 = [row_288[middle_288:] for row_288 in second_matrix_288[:middle_288]]
	bottom_left_b_288 = [row_288[:middle_288] for row_288 in second_matrix_288[middle_288:]]
	bottom_right_b_288 = [row_288[middle_288:] for row_288 in second_matrix_288[middle_288:]]

	p1_288 = strassen_288(
		add_matrices_288(top_left_a_288, bottom_right_a_288, steps_288),
		add_matrices_288(top_left_b_288, bottom_right_b_288, steps_288),
		steps_288,
	)
	p2_288 = strassen_288(
		add_matrices_288(bottom_left_a_288, bottom_right_a_288, steps_288),
		top_left_b_288,
		steps_288,
	)
	p3_288 = strassen_288(
		top_left_a_288,
		subtract_matrices_288(top_right_b_288, bottom_right_b_288, steps_288),
		steps_288,
	)
	p4_288 = strassen_288(
		bottom_right_a_288,
		subtract_matrices_288(bottom_left_b_288, top_left_b_288, steps_288),
		steps_288,
	)
	p5_288 = strassen_288(
		add_matrices_288(top_left_a_288, top_right_a_288, steps_288),
		bottom_right_b_288,
		steps_288,
	)
	p6_288 = strassen_288(
		subtract_matrices_288(bottom_left_a_288, top_left_a_288, steps_288),
		add_matrices_288(top_left_b_288, top_right_b_288, steps_288),
		steps_288,
	)
	p7_288 = strassen_288(
		subtract_matrices_288(top_right_a_288, bottom_right_a_288, steps_288),
		add_matrices_288(bottom_left_b_288, bottom_right_b_288, steps_288),
		steps_288,
	)

	left_top_288 = add_matrices_288(
		subtract_matrices_288(add_matrices_288(p1_288, p4_288, steps_288), p5_288, steps_288),
		p7_288,
		steps_288,
	)
	right_top_288 = add_matrices_288(p3_288, p5_288, steps_288)
	left_bottom_288 = add_matrices_288(p2_288, p4_288, steps_288)
	right_bottom_288 = add_matrices_288(
		add_matrices_288(p1_288, p3_288, steps_288),
		subtract_matrices_288(p6_288, p2_288, steps_288),
		steps_288,
	)

	result_matrix_288 = []
	for row_288 in range(middle_288):
		result_matrix_288.append(left_top_288[row_288] + right_top_288[row_288])
	for row_288 in range(middle_288):
		result_matrix_288.append(left_bottom_288[row_288] + right_bottom_288[row_288])
	return result_matrix_288


def normal_multiply_288(first_matrix_288, second_matrix_288, steps_288):
	"""Multiply matrices normally and count multiplications and additions."""
	size_288 = len(first_matrix_288)
	result_matrix_288 = [[0] * size_288 for row_288 in range(size_288)]
	for row_288 in range(size_288):
		for column_288 in range(size_288):
			for position_288 in range(size_288):
				result_matrix_288[row_288][column_288] += (
					first_matrix_288[row_288][position_288]
					* second_matrix_288[position_288][column_288]
				)
				steps_288[0] += 2
	return result_matrix_288


def display_matrix_288(matrix_288):
	"""Display a matrix."""
	for row_288 in matrix_288:
		print(row_288)


def run_experiments_288():
	"""Print the step/frequency table and create a timing graph."""
	print("\nStep/Frequency and Time Complexity Table")
	print("Size\tNormal steps\tStrassen steps\tNormal time\tStrassen time")
	sizes_288 = [2, 4, 8]
	normal_times_288 = []
	strassen_times_288 = []
	for size_288 in sizes_288:
		first_matrix_288 = generate_matrix_288(size_288)
		second_matrix_288 = generate_matrix_288(size_288)
		normal_steps_288 = [0]
		strassen_steps_288 = [0]
		start_time_288 = time_288.perf_counter()
		normal_multiply_288(first_matrix_288, second_matrix_288, normal_steps_288)
		normal_time_288 = time_288.perf_counter() - start_time_288
		start_time_288 = time_288.perf_counter()
		strassen_288(first_matrix_288, second_matrix_288, strassen_steps_288)
		strassen_time_288 = time_288.perf_counter() - start_time_288
		normal_times_288.append(normal_time_288)
		strassen_times_288.append(strassen_time_288)
		print(
			f"{size_288}\t{normal_steps_288[0]}\t\t{strassen_steps_288[0]}\t\t"
			f"{normal_time_288:.8f}\t{strassen_time_288:.8f}"
		)

	try:
		import matplotlib.pyplot as pyplot_288
	except ImportError:
		print("Matplotlib is not installed; skipping the graph.")
		return

	pyplot_288.plot(sizes_288, normal_times_288, marker="o", label="Normal")
	pyplot_288.plot(sizes_288, strassen_times_288, marker="o", label="Strassen")
	pyplot_288.xlabel("Matrix size n")
	pyplot_288.ylabel("Time (seconds)")
	pyplot_288.title("Normal Multiplication vs Strassen Multiplication")
	pyplot_288.legend()
	pyplot_288.grid(True)
	pyplot_288.tight_layout()
	pyplot_288.savefig("Q4_time_comparison.png")
	pyplot_288.show()


# Conclusion: Normal multiplication uses O(n^3), while Strassen uses O(n^2.807).
# Strassen reduces multiplications, but for small matrices its extra additions can add overhead.


def main_288():
	while True:
		try:
			size_288 = int(input("Enter matrix size (2, 4, 8, ...): "))
		except ValueError:
			print("Please enter a whole number.")
			continue
		if is_power_of_two_288(size_288):
			break
		print("Matrix size must be a positive power of 2.")

	print("1. Enter matrices manually")
	print("2. Generate matrices randomly")
	choice_288 = input("Enter your choice: ")
	if choice_288 == "1":
		first_matrix_288 = read_matrix_288(size_288, "Matrix A")
		second_matrix_288 = read_matrix_288(size_288, "Matrix B")
	elif choice_288 == "2":
		first_matrix_288 = generate_matrix_288(size_288)
		second_matrix_288 = generate_matrix_288(size_288)
	else:
		print("Invalid choice.")
		return

	steps_288 = [0]
	result_matrix_288 = strassen_288(first_matrix_288, second_matrix_288, steps_288)
	print("\nMatrix A:")
	display_matrix_288(first_matrix_288)
	print("\nMatrix B:")
	display_matrix_288(second_matrix_288)
	print("\nResultant matrix using Strassen:")
	display_matrix_288(result_matrix_288)
	print(f"\nStep/Frequency count: {steps_288[0]}")

	if input("Run comparison experiments? (y/n): ").lower() == "y":
		run_experiments_288()


if __name__ == "__main__":
	main_288()
