#!/usr/bin/env python

from irradix import irradix, set_precision
import random

def test_no_101_sequence():
    set_precision(1000)
    val = 10  # Start with a small number
    for i in range(1000):  # Test over a range of values
        encoded = irradix(val)
        
        if '101' in encoded:
            print(f"Test failed at {i+2}-digit value: Encoded value contains '101'.")
            print(f"Value: {val}")
            print(f"Encoded: {encoded}")
            return False
        else:
            print(f"{i+2}-digit values pass: No '101' in {encoded}")

        # Generate the next number
        digit = random.randint(0, 9)
        val *= 10
        val += digit

    print("All tests passed: No '101' sequence found in encoded values.")
    return True

# Run the test
test_no_101_sequence()

