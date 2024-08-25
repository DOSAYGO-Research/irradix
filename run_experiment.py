#!/usr/bin/env python

import random
from vbyte import vbyte_encode, vbyte_decode
from irradix import encode, decode, l1encode, l1decode, set_precision
import statistics

set_precision(100)  # Adjust precision as needed

# Functions to generate random integers as in previous tests
def generate_random_integer_50_to_100_digits():
    num_digits = random.randint(50, 100)
    lower_bound = 10**(num_digits - 1)
    upper_bound = 10**num_digits - 1
    return random.randint(lower_bound, upper_bound)

def calculate_theoretical_length(numbers):
    length = 0
    for number in numbers:
        bit_length = number.bit_length()
        length += bit_length
        length += bit_length.bit_length()
    return length

def run_test_and_generate_markdown(generator_function, test_name, num_tests=10):
    results = []
    markdown = []

    markdown.append(f"# {test_name} Results\n")
    markdown.append("| Test | Sequence Length | Irradix Bits | L1 Bits | VByte Bits | Benchmark Bits | Irradix % Expansion | L1 % Expansion | VByte % Expansion |")
    markdown.append("|------|-----------------|--------------|---------|------------|----------------|--------------------|----------------|-------------------|")

    for i in range(num_tests):
        sequence_length = random.randint(100, 1000)
        original_numbers = [generator_function() for _ in range(sequence_length)]

        # Encode using the different methods
        irradix_bits = len(encode(original_numbers)) * 8
        l1_bits = len(l1encode(original_numbers)) * 8
        vbyte_bits = len(vbyte_encode(original_numbers)) * 8

        # Calculate the theoretical minimum length
        benchmark_bits = calculate_theoretical_length(original_numbers)

        # Calculate the percentage expansion
        irradix_expansion = ((irradix_bits - benchmark_bits) / benchmark_bits) * 100
        l1_expansion = ((l1_bits - benchmark_bits) / benchmark_bits) * 100
        vbyte_expansion = ((vbyte_bits - benchmark_bits) / benchmark_bits) * 100

        results.append((sequence_length, irradix_bits, l1_bits, vbyte_bits, benchmark_bits,
                        irradix_expansion, l1_expansion, vbyte_expansion))

        markdown.append(f"| {i+1} | {sequence_length} | {irradix_bits} | {l1_bits} | {vbyte_bits} | {benchmark_bits} | "
                        f"{irradix_expansion:.2f}% | {l1_expansion:.2f}% | {vbyte_expansion:.2f}% |")

    # Calculate summary statistics
    irradix_expansions = [result[5] for result in results]
    l1_expansions = [result[6] for result in results]
    vbyte_expansions = [result[7] for result in results]

    markdown.append(f"\n## Summary Statistics\n")
    markdown.append(f"- **Average Irradix Expansion:** {statistics.mean(irradix_expansions):.2f}%")
    markdown.append(f"- **Average L1 Expansion:** {statistics.mean(l1_expansions):.2f}%")
    markdown.append(f"- **Average VByte Expansion:** {statistics.mean(vbyte_expansions):.2f}%\n")

    return "\n".join(markdown)

if __name__ == "__main__":
    markdown_content = run_test_and_generate_markdown(generate_random_integer_50_to_100_digits, "50 to 100 Digit Test")
    with open("results.md", "w") as f:
        f.write(markdown_content)
    print("Markdown results generated in results.md")

