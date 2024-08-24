#!/usr/bin/env python

import random
from irradix import encode, decode, set_precision

set_precision(100)  # enough to cover the 32 digits below

# Generate a random integer with logarithmic bias
def generate_random_integer():
    if random.random() < 0.25:
        return 0
    # Generate a random number of digits
    num_digits = random.randint(1, 32)
    lower_bound = 10**(num_digits - 1)
    upper_bound = 10**num_digits - 1
    return random.randint(lower_bound, upper_bound)

# Test function to encode and decode a list of random integers (small sequences)
def test_random_integers_small():
    num_tests = 1000  # Number of tests to run

    for i in range(num_tests):
        # Generate a random list of integers with a length between 1 and 10
        original_numbers = [generate_random_integer() for _ in range(random.randint(1, 10))]
        print(f"\nSmall Test {i+1}:\nOriginal Numbers (length: {len(original_numbers)}): {original_numbers}")

        # Encode the list of integers
        encoded_chunks = encode(original_numbers)
        # print(f" Encoded Chunks: {encoded_chunks}")

        # Decode the packed sequence
        decoded_numbers = decode(encoded_chunks)
        print(f"\nDecoded Numbers (length: {len(decoded_numbers)}): {decoded_numbers}")

        # Verify that the decoded numbers match the original numbers
        assert decoded_numbers == original_numbers, f"Small Test {i+1} failed! Decoded numbers do not match the original."

    print(f"All {num_tests} small tests passed successfully!")

# Test function to encode and decode a list of random integers (large sequences)
def test_random_integers_large():
    num_tests = 100  # Number of tests to run

    for i in range(num_tests):
        # Generate a random list of integers with a length between 1000 and 10000
        sequence_length = random.randint(1000, 10000)
        original_numbers = [generate_random_integer() for _ in range(sequence_length)]
        print(f"\nLarge Test {i+1}:\nOriginal Numbers (length: {len(original_numbers)}): {original_numbers[:5]}...")

        # Encode the list of integers
        encoded_chunks = encode(original_numbers)
        # print(f" Encoded Chunks: {encoded_chunks}")

        # Decode the packed sequence
        decoded_numbers = decode(encoded_chunks)
        print(f"\nDecoded Numbers (length: {len(decoded_numbers)}): {decoded_numbers[:5]}...")

        # Verify that the decoded numbers match the original numbers
        assert decoded_numbers == original_numbers, f"Large Test {i+1} failed! Decoded numbers do not match the original."

    print(f"All {num_tests} large tests passed successfully!")

# Run both tests
if __name__ == "__main__":
    test_random_integers_small()
    test_random_integers_large()

