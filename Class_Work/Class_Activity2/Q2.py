"""Menu-driven Merge Sort program with step and frequency counts."""

import random as random_288
import time as time_288


def merge_288(array_288, left_288, middle_288, right_288, steps_288):
	"""Merge two sorted parts of an array."""
	left_array_288 = array_288[left_288:middle_288 + 1]
	right_array_288 = array_288[middle_288 + 1:right_288 + 1]
	left_index_288 = 0
	right_index_288 = 0
	array_index_288 = left_288

	while left_index_288 < len(left_array_288) and right_index_288 < len(right_array_288):
		steps_288[0] += 1
		if left_array_288[left_index_288] <= right_array_288[right_index_288]:
			array_288[array_index_288] = left_array_288[left_index_288]
			left_index_288 += 1
		else:
			array_288[array_index_288] = right_array_288[right_index_288]
			right_index_288 += 1
		array_index_288 += 1

	while left_index_288 < len(left_array_288):
		steps_288[0] += 1
		array_288[array_index_288] = left_array_288[left_index_288]
		left_index_288 += 1
		array_index_288 += 1

	while right_index_288 < len(right_array_288):
		steps_288[0] += 1
		array_288[array_index_288] = right_array_288[right_index_288]
		right_index_288 += 1
		array_index_288 += 1


def merge_sort_288(array_288, left_288, right_288, steps_288):
	"""Sort an array using Merge Sort."""
	if left_288 < right_288:
		steps_288[0] += 1
		middle_288 = (left_288 + right_288) // 2
		merge_sort_288(array_288, left_288, middle_288, steps_288)
		merge_sort_288(array_288, middle_288 + 1, right_288, steps_288)
		merge_288(array_288, left_288, middle_288, right_288, steps_288)


def descending_sort_288(array_288):
	"""Sort an array in descending order using Bubble Sort."""
	steps_288 = 0
	for pass_288 in range(len(array_288) - 1):
		for index_288 in range(len(array_288) - 1 - pass_288):
			steps_288 += 1
			if array_288[index_288] < array_288[index_288 + 1]:
				array_288[index_288], array_288[index_288 + 1] = (
					array_288[index_288 + 1], array_288[index_288]
				)
	return steps_288


def timed_merge_sort_288(input_array_288):
	"""Return the sorted copy, step count, and running time."""
	array_288 = input_array_288[:]
	steps_288 = [0]
	start_time_288 = time_288.perf_counter()
	if array_288:
		merge_sort_288(array_288, 0, len(array_288) - 1, steps_288)
	time_taken_288 = time_288.perf_counter() - start_time_288
	return array_288, steps_288[0], time_taken_288


def show_analysis_288(input_array_288, data_type_288):
	"""Sort data and display its result, frequency count, and time."""
	sorted_array_288, steps_288, time_taken_288 = timed_merge_sort_288(input_array_288)
	print(f"\n{data_type_288} data")
	print(f"Sorted array: {sorted_array_288}")
	print(f"Step/Frequency count: {steps_288}")
	print(f"Time taken: {time_taken_288:.8f} seconds")
	return steps_288, time_taken_288


def run_experiments_288(input_array_288):
	"""Display a comparison table and graph for the three input types."""
	data_sets_288 = [
		("Random", input_array_288),
		("Already sorted", sorted(input_array_288)),
		("Descending sorted", sorted(input_array_288, reverse=True)),
	]
	steps_list_288 = []
	times_list_288 = []

	print("\nStep/Frequency Count and Time Table")
	print("Input type\tSteps\tTime (seconds)")
	for data_type_288, data_set_288 in data_sets_288:
		_, steps_288, time_taken_288 = timed_merge_sort_288(data_set_288)
		steps_list_288.append(steps_288)
		times_list_288.append(time_taken_288)
		print(f"{data_type_288}\t{steps_288}\t{time_taken_288:.8f}")

	try:
		import matplotlib.pyplot as pyplot_288
	except ImportError:
		print("Matplotlib is not installed; skipping the graph.")
		return

	pyplot_288.bar(
		["Random", "Sorted", "Descending"],
		times_list_288,
		color=["steelblue", "seagreen", "darkorange"],
	)
	pyplot_288.title("Merge Sort Time Complexity Comparison")
	pyplot_288.ylabel("Time (seconds)")
	pyplot_288.tight_layout()
	pyplot_288.savefig("Q2_time_comparison.png")
	pyplot_288.show()


# Conclusion: Merge Sort has O(n log n) time complexity for random, sorted,
# and descending-sorted input, so its step count remains nearly consistent.


def main_288():
	array_288 = []
	random_array_288 = []
	n_288 = 0

	while True:
		print("\n1. Generate n random numbers")
		print("2. Display Array")
		print("3. Sort in Ascending Order using Merge Sort")
		print("4. Sort in Descending Order")
		print("5. Time Complexity for ascending random data")
		print("6. Time Complexity for ascending already sorted data")
		print("7. Time Complexity for ascending descending-sorted data")
		print("8. Exit")

		choice_288 = input("Enter your choice: ")

		if choice_288 == "1":
			n_288 = int(input("Enter the value of n: "))
			array_288 = [random_288.randint(1, 100) for value_288 in range(n_288)]
			random_array_288 = array_288[:]
			print("Random array generated.")
		elif choice_288 == "2":
			print("Array:", array_288)
		elif choice_288 == "3":
			show_analysis_288(array_288, "Ascending")
		elif choice_288 == "4":
			steps_288 = descending_sort_288(array_288)
			print("Descending array:", array_288)
			print(f"Step/Frequency count: {steps_288}")
		elif choice_288 == "5":
			if n_288 == 0:
				print("Generate an array first.")
			else:
				run_experiments_288(random_array_288)
		elif choice_288 == "6":
			if n_288 == 0:
				print("Generate an array first.")
			else:
				show_analysis_288(sorted(random_array_288), "Ascending already sorted")
		elif choice_288 == "7":
			if n_288 == 0:
				print("Generate an array first.")
			else:
				show_analysis_288(sorted(random_array_288, reverse=True), "Ascending descending-sorted")
		elif choice_288 == "8":
			print("Program ended.")
			break
		else:
			print("Invalid choice.")


if __name__ == "__main__":
	main_288()
