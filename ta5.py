#!/usr/bin/env python

import random
from vbyte import vbyte_encode, vbyte_decode
from irradix import encode, decode, l1encode, l1decode, set_precision
import statistics


set_precision(100)  # enough to cover the 32 digits below

# Generate a random integer with 50 to 100 digits
def generate_random_integer_50_to_100_digits():
    num_digits = random.randint(50, 100)
    lower_bound = 10**(num_digits - 1)
    upper_bound = 10**num_digits - 1
    return random.randint(lower_bound, upper_bound)

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
# Which is just a length-value pattern that should approach distribution entropy
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

# Test function to encode and decode a list of random integers and compare with benchmark, including l1 variants
def new_test_random_integers_and_compare_with_l1(generator_function, test_name):
    num_tests = 100  # Number of tests to run
    results = []

    for i in range(num_tests):
        # Generate a random list of integers with a length between 100 and 1000
        sequence_length = random.randint(100, 1000)
        original_numbers = [generator_function() for _ in range(sequence_length)]

        # Encode the list of integers using irradix
        encoded_chunks = encode(original_numbers)
        irradix_length = len(encoded_chunks) * 8  # Convert to bits

        # Encode the list using l1encode
        l1_encoded_chunks = l1encode(original_numbers)
        l1_irradix_length = len(l1_encoded_chunks) * 8  # Convert to bits

        # Encode the list using VByte
        vbyte_encoded_chunks = vbyte_encode(original_numbers)
        vbyte_length = len(vbyte_encoded_chunks) * 8  # Convert to bits

        # Calculate the length using the theoretical benchmark method
        theoretical_length = calculate_theoretical_length(original_numbers)

        # Calculate the percentage expansion
        expansion_percentage = ((irradix_length - theoretical_length) / theoretical_length) * 100
        l1_expansion_percentage = ((l1_irradix_length - theoretical_length) / theoretical_length) * 100
        vbyte_expansion_percentage = ((vbyte_length - theoretical_length) / theoretical_length) * 100

        # Append results
        results.append((sequence_length, irradix_length, l1_irradix_length, vbyte_length, theoretical_length,
                        expansion_percentage, l1_expansion_percentage, vbyte_expansion_percentage, original_numbers))

        # Incremental display of results
        print(f"{test_name} Test {i+1}: Seq Len: {sequence_length}, "
              f"Irradix Bits: {irradix_length}, L1 Bits: {l1_irradix_length}, VByte Bits: {vbyte_length}, "
              f"Benchmark Bits: {theoretical_length}, % Expansion: {expansion_percentage:.2f}%, "
              f"L1 % Expansion: {l1_expansion_percentage:.2f}%, VByte % Expansion: {vbyte_expansion_percentage:.2f}%")

    # Calculate average, median, min, and max for original, l1, and vbyte
    expansion_percentages = [result[5] for result in results]
    l1_expansion_percentages = [result[6] for result in results]
    vbyte_expansion_percentages = [result[7] for result in results]

    average_expansion = statistics.mean(expansion_percentages)
    median_expansion = statistics.median(expansion_percentages)
    min_expansion = min(expansion_percentages)
    max_expansion = max(expansion_percentages)

    l1_average_expansion = statistics.mean(l1_expansion_percentages)
    l1_median_expansion = statistics.median(l1_expansion_percentages)
    l1_min_expansion = min(l1_expansion_percentages)
    l1_max_expansion = max(l1_expansion_percentages)

    vbyte_average_expansion = statistics.mean(vbyte_expansion_percentages)
    vbyte_median_expansion = statistics.median(vbyte_expansion_percentages)
    vbyte_min_expansion = min(vbyte_expansion_percentages)
    vbyte_max_expansion = max(vbyte_expansion_percentages)

    # Display summary statistics for original, l1, and vbyte
    print(f"\n{test_name} Summary Statistics (Original):")
    print(f"Average % Expansion: {average_expansion:.2f}%")
    print(f"Median % Expansion: {median_expansion:.2f}%")
    print(f"Min % Expansion: {min_expansion:.2f}%")
    print(f"Max % Expansion: {max_expansion:.2f}%")

    print(f"\n{test_name} Summary Statistics (L1):")
    print(f"Average % Expansion: {l1_average_expansion:.2f}%")
    print(f"Median % Expansion: {l1_median_expansion:.2f}%")
    print(f"Min % Expansion: {l1_min_expansion:.2f}%")
    print(f"Max % Expansion: {l1_max_expansion:.2f}%")

    print(f"\n{test_name} Summary Statistics (VByte):")
    print(f"Average % Expansion: {vbyte_average_expansion:.2f}%")
    print(f"Median % Expansion: {vbyte_median_expansion:.2f}%")
    print(f"Min % Expansion: {vbyte_min_expansion:.2f}%")
    print(f"Max % Expansion: {vbyte_max_expansion:.2f}%")

# Run the tests and comparison for each scenario
if __name__ == "__main__":
    print("Running 50 to 100 Digit Test (L1 Variants and VByte)...")
    new_test_random_integers_and_compare_with_l1(generate_random_integer_50_to_100_digits, "50 to 100 Digit")

    print("Running Original Test (L1 Variants)...")
    new_test_random_integers_and_compare_with_l1(generate_random_integer_original, "Original")

    print("\nRunning 16-bit Test (L1 Variants)...")
    new_test_random_integers_and_compare_with_l1(generate_random_integer_16bit, "16-bit")

    print("\nRunning 1 Million Test (L1 Variants)...")
    new_test_random_integers_and_compare_with_l1(generate_random_integer_1m, "1 Million")

