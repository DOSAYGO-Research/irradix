import random
from math import log10, ceil
from irradix import encode, decode, set_precision

set_precision(100) # enough to cover the 32 digits below

# Generate a random integer with logarithmic bias
def generate_random_integer():
    if random.random() < 0.25:
        return 0
    # Generate a random number of digits
    num_digits = random.randint(1, 32)
    lower_bound = 10**(num_digits - 1)
    upper_bound = 10**num_digits - 1
    return random.randint(lower_bound, upper_bound)

# Test function to encode and decode a list of random integers
def test_random_integers():
    num_tests = 1000  # Number of tests to run

    for i in range(num_tests):
        # Generate a random list of integers
        original_numbers = [generate_random_integer() for _ in range(random.randint(1, 10))]
        print(f"\nTest {i+1}:\nOriginal Numbers: {original_numbers}")

        # Encode the list of integers
        encoded_chunks = encode(original_numbers)
        #print(f" Encoded Chunks: {encoded_chunks}")

        # Decode the packed sequence
        decoded_numbers = decode(encoded_chunks)
        print(f"\n Decoded Numbers: {decoded_numbers}")

        # Verify that the decoded numbers match the original numbers
        assert decoded_numbers == original_numbers, f"Test {i+1} failed! Decoded numbers do not match the original."

    print(f"All {num_tests} tests passed successfully!")

# Run the test
if __name__ == "__main__":
    test_random_integers()

