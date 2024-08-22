#!/usr/bin/env python

from irradix import irradix
from sympy import isprime

def test_irradix_binary_equivalence():
    max_num = 1000
    both_prime_count = 0
    original_prime_count = 0
    binary_prime_count = 0

    print(f"{'Original Integer':<20} {'irradix Representation':<30} {'Interpreted as Binary':<30} {'isPrime':<10} {'Prime Comparison':<20} {'Binary Expansion (%)':<20}")
    print("-" * 150)

    for i in range(1, max_num + 1):
        irradix_rep = irradix(i)
        binary_interpretation = int(irradix_rep, 2)
        original_prime_check = isprime(i)
        binary_prime_check = isprime(binary_interpretation)

        # Prime comparison column
        if original_prime_check and binary_prime_check:
            prime_comparison = 3
            both_prime_count += 1
        elif original_prime_check and not binary_prime_check:
            prime_comparison = 2
            original_prime_count += 1
        elif not original_prime_check and binary_prime_check:
            prime_comparison = 1
            binary_prime_count += 1
        else:
            prime_comparison = 0

        # Binary expansion as percentage
        original_binary_length = len(bin(i)[2:])
        irradix_binary_length = len(irradix_rep)
        binary_expansion = (irradix_binary_length / original_binary_length) * 100

        print(f"{i:<20} {irradix_rep:<30} {binary_interpretation:<30} {str(binary_prime_check):<10} {prime_comparison:<20} {binary_expansion:<20.2f}")

    # Calculate prime density
    original_prime_density = (both_prime_count + original_prime_count) / max_num * 100
    binary_prime_density = (both_prime_count + binary_prime_count) / max_num * 100

    print("\nPrime Density:")
    print(f"Original: {original_prime_density:.2f}%")
    print(f"Binary: {binary_prime_density:.2f}%")

if __name__ == "__main__":
    test_irradix_binary_equivalence()

