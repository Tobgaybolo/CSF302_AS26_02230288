"""Prime number testing using a naive method and the Sieve of Eratosthenes."""

import time as time_288
from importlib import import_module as import_module_288



def naive_is_prime_288(number_288):
	"""Return whether number is prime and the number of divisibility checks."""
	if number_288 < 2:
		return False, 0

	steps_288 = 0
	for divisor_288 in range(2, number_288):
		steps_288 += 1
		if number_288 % divisor_288 == 0:
			return False, steps_288

	return True, steps_288


def sieve_primes_288(limit_288):
	"""Return a list showing which numbers are prime and the step count."""
	is_prime_288 = [True] * (limit_288 + 1)
	steps_288 = 0

	if limit_288 >= 0:
		is_prime_288[0] = False
	if limit_288 >= 1:
		is_prime_288[1] = False

	divisor_288 = 2
	while divisor_288 * divisor_288 <= limit_288:
		steps_288 += 1  # Check whether this number is a prime divisor.
		if is_prime_288[divisor_288]:
			multiple_288 = divisor_288 * divisor_288
			while multiple_288 <= limit_288:
				steps_288 += 1  # Mark one multiple as not prime.
				is_prime_288[multiple_288] = False
				multiple_288 += divisor_288
		divisor_288 += 1

	return is_prime_288, steps_288


def get_numbers_288():
	"""Read at least 10 whole numbers from the user."""
	while True:
		try:
			numbers_288 = [int(value_288) for value_288 in input(
				"Enter at least 10 whole numbers, separated by spaces: "
			).split()]
		except ValueError:
			print("Please enter whole numbers only.")
			continue

		if len(numbers_288) >= 10:
			return numbers_288

		print("Please enter at least 10 numbers.")


def main_288():
	numbers_288 = get_numbers_288()

	naive_results_288 = []
	naive_steps_288 = 0
	naive_start_288 = time_288.perf_counter()
	for number_288 in numbers_288:
		result_288, steps_288 = naive_is_prime_288(number_288)
		naive_results_288.append(result_288)
		naive_steps_288 += steps_288
	naive_time_288 = time_288.perf_counter() - naive_start_288

	largest_number_288 = max(numbers_288)
	if largest_number_288 < 0:
		largest_number_288 = 1

	sieve_start_288 = time_288.perf_counter()
	prime_list_288, sieve_steps_288 = sieve_primes_288(largest_number_288)
	sieve_results_288 = [
		number_288 >= 0 and prime_list_288[number_288]
		for number_288 in numbers_288
	]
	sieve_time_288 = time_288.perf_counter() - sieve_start_288

	print("\nResults")
	print("Number\tNaive\tSieve")
	for number_288, naive_result_288, sieve_result_288 in zip(
		numbers_288, naive_results_288, sieve_results_288
	):
		print(f"{number_288}\t{naive_result_288}\t{sieve_result_288}")

	print("\nPerformance comparison")
	print(f"Naive steps: {naive_steps_288}")
	print(f"Sieve steps: {sieve_steps_288}")
	print(f"Naive time: {naive_time_288:.8f} seconds")
	print(f"Sieve time: {sieve_time_288:.8f} seconds")
	print("\nStep/Frequency Count Table")
	print("Method\tSteps\tTime (seconds)")
	print(f"Naive\t{naive_steps_288}\t{naive_time_288:.8f}")
	print(f"Sieve\t{sieve_steps_288}\t{sieve_time_288:.8f}")

	try:
		plt_288 = import_module_288("matplotlib.pyplot")
	except ImportError:
		print("Matplotlib is not installed; skipping the performance chart.")
	else:
		algorithms_288 = ["Naive method", "Sieve method"]
		times_288 = [naive_time_288, sieve_time_288]
		plt_288.bar(algorithms_288, times_288, color=["steelblue", "seagreen"])
		plt_288.title("Prime Testing: Runtime Comparison")
		plt_288.ylabel("Time (seconds)")
		plt_288.tight_layout()
		plt_288.savefig("Q1_time_comparison.png")
		plt_288.show()


if __name__ == "__main__":
	main_288()
