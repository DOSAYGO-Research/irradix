#!/usr/bin/env python

import random
from irradix import encode, decode, set_precision
import statistics

set_precision(100)  # enough to cover the 32 digits below

# Generate a random integer with logarithmic bias for the original setup
def generate_random_integer_original():
    if random.random() < 0.25:
        return 0
    # Generate a random number of digits
    num_digits = random.randint(1, 32)
    lower_bound = 10**(num_digits - 1)
    upper_bound = 10**num_digits - 1
    return random.randint(lower_bound, upper_bound)

# Generate a random integer constrained to 16-bit values with reduced 0 probability
def generate_random_integer_16bit():
    if random.random() < 0.01:  # 1/100th probability of 0
        return 0
    return random.randint(1, 65535)  # 16-bit constraint (1 to 65535)

# Generate a random integer between 1 and 1 million with equal probability of all digit lengths
def generate_random_integer_1m():
    return random.randint(1, 1000000)  # Equal probability between 1 and 1 million

# Calculate the length of the encoded sequence using the theoretical benchmark method
def calculate_theoretical_length(numbers):
    length = 0
    for number in numbers:
        bit_length = number.bit_length()
        if bit_length <= 6:
            length += 2 + 6 + bit_length
        elif bit_length <= 14:
            length += 2 + 14 + bit_length
        elif bit_length <= 22:
            length += 2 + 22 + bit_length
        else:
            length += 2 + 30 + bit_length
    return length

# Test function to encode and decode a list of random integers and compare with benchmark
def test_random_integers_and_compare(generator_function, test_name):
    num_tests = 250  # Number of tests to run
    results = []

    for i in range(num_tests):
        # Generate a random list of integers with a length between 100 and 1000
        sequence_length = random.randint(100, 1000)
        original_numbers = [generator_function() for _ in range(sequence_length)]
        
        # Encode the list of integers using irradix
        encoded_chunks = encode(original_numbers)
        irradix_length = len(encoded_chunks) * 8  # Convert to bits

        # Calculate the length using the theoretical benchmark method
        theoretical_length = calculate_theoretical_length(original_numbers)

        # Calculate the percentage expansion
        expansion_percentage = ((irradix_length - theoretical_length) / theoretical_length) * 100

        # Append results
        results.append((sequence_length, irradix_length, theoretical_length, expansion_percentage, original_numbers))

        # Incremental display of results
        print(f"{test_name} Test {i+1}: Seq Len: {sequence_length}, Irradix Bits: {irradix_length}, "
              f"Benchmark Bits: {theoretical_length}, % Expansion: {expansion_percentage:.2f}%")

    # Calculate average, median, min, and max
    expansion_percentages = [result[3] for result in results]
    average_expansion = statistics.mean(expansion_percentages)
    median_expansion = statistics.median(expansion_percentages)
    min_expansion = min(expansion_percentages)
    max_expansion = max(expansion_percentages)

    # Find the sequences that produced min and max expansions
    min_expansion_result = next(result for result in results if result[3] == min_expansion)
    max_expansion_result = next(result for result in results if result[3] == max_expansion)

    # Display summary statistics
    print(f"\n{test_name} Summary Statistics:")
    print(f"Average % Expansion: {average_expansion:.2f}%")
    print(f"Median % Expansion: {median_expansion:.2f}%")
    print(f"Min % Expansion: {min_expansion:.2f}%")
    print(f"Max % Expansion: {max_expansion:.2f}%")
    print(f"\nMin Expansion Sequence:")
    print(f"Seq Len: {min_expansion_result[0]}, Irradix Bits: {min_expansion_result[1]}, "
          f"Benchmark Bits: {min_expansion_result[2]}, % Expansion: {min_expansion_result[3]:.2f}%")
    print(f"Sequence: {min_expansion_result[4]}")
    print(f"\nMax Expansion Sequence:")
    print(f"Seq Len: {max_expansion_result[0]}, Irradix Bits: {max_expansion_result[1]}, "
          f"Benchmark Bits: {max_expansion_result[2]}, % Expansion: {max_expansion_result[3]:.2f}%")
    print(f"Sequence: {max_expansion_result[4]}")

# Run the tests and comparison for each scenario
if __name__ == "__main__":
    print("Running Original Test...")
    test_random_integers_and_compare(generate_random_integer_original, "Original")

    print("\nRunning 16-bit Test...")
    test_random_integers_and_compare(generate_random_integer_16bit, "16-bit")

    print("\nRunning 1 Million Test...")
    test_random_integers_and_compare(generate_random_integer_1m, "1 Million")

