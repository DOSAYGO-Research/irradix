"""Exact even-shift residue counts and a reproducible prime experiment.

Run from the repository root; --output writes the measurements as JSON.
Only the heuristic sums and displayed ratios use floating-point arithmetic.
"""
import argparse
import json
from math import gcd, isqrt, log
from pathlib import Path

from phi_exact import fibonacci_irradix


def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def residue_counts(length, modulus):
    """Counts of canonical words by binary residue, without enumeration."""
    even, odd = [0] * modulus, [0] * modulus
    even[1 % modulus] = 1
    for _ in range(length - 1):
        new_even, new_odd = [0] * modulus, [0] * modulus
        for r in range(modulus):
            new_even[(2*r+1) % modulus] += even[r]
            new_odd[2*r % modulus] += even[r]
            new_even[2*r % modulus] += odd[r]
        even, odd = new_even, new_odd
    return [a+b for a, b in zip(even, odd)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    blocks = []
    cumulative = 0
    for k in range(1, 101):
        counts = residue_counts(k, 6)
        assert sum(counts) == fibonacci(k+1)
        expected = (1 if k == 1 else fibonacci(k-1)) if k % 2 else 0
        assert counts[1] == expected and counts[5] == 0
        cumulative += counts[1]
        assert cumulative == fibonacci(k if k % 2 else k-1)
        if k in (13, 14, 29, 30, 59, 60):
            total = fibonacci(k+3)-2
            blocks.append(dict(length=k, inputs=total, coprime_to_6=cumulative,
                               candidate_fraction=cumulative/total))

    # Independent enumeration checks the DP, including composite moduli.
    for modulus in (2, 3, 5, 6, 7, 11, 13, 35):
        for k in range(1, 14):
            observed = [0]*modulus
            for n in range(fibonacci(k+2)-1, fibonacci(k+3)-1):
                observed[int(fibonacci_irradix(n), 2) % modulus] += 1
            assert observed == residue_counts(k, modulus)

    uniformity = []
    for modulus in (5, 7, 11, 13, 35):
        for k in (20, 60, 100):
            counts = residue_counts(k, modulus)
            total = sum(counts)
            uniformity.append(dict(modulus=modulus, length=k,
                max_relative_deviation=max(abs(modulus*c-total) for c in counts)/total))

    n_max = 100_000
    values = [int(fibonacci_irradix(n), 2) for n in range(1, n_max+1)]
    limit = max(values)
    sieve = bytearray(b'\x01')*(limit+1)
    sieve[:2] = b'\x00\x00'
    for p in range(2, isqrt(limit)+1):
        if sieve[p]:
            sieve[p*p::p] = b'\x00'*((limit-p*p)//p+1)
    checkpoints = {100, 1000, 10000, n_max}
    checkpoints.update(fibonacci(k+3)-2 for k in range(5, 24)
                       if fibonacci(k+3)-2 <= n_max)
    primes, candidates, heuristic = 0, 0, 0.0
    samples = []
    for n, value in enumerate(values, 1):
        word = bin(value)[2:]
        trailing = len(word)-len(word.rstrip('0'))
        predicted = 0 if (len(word)-trailing) % 2 == 0 else (-1)**trailing % 3
        assert value % 3 == predicted
        if sieve[value] and value > 3:
            assert len(word) % 2 == 1 and value % 6 == 1
        primes += sieve[value]
        candidates += gcd(value, 6) == 1
        if value in (2, 3):
            heuristic += 1
        elif value > 3 and value % 6 == 1:
            heuristic += 3/log(value)
        if n in checkpoints:
            samples.append(dict(inputs=n, max_binary_image=value,
                mapped_primes=primes, coprime_to_6=candidates,
                mod_6_logarithmic_heuristic=heuristic))
    result = dict(checks=dict(length_formulas=100, enumerated_max_length=13,
                  enumerated_moduli=[2, 3, 5, 6, 7, 11, 13, 35],
                  prime_sieve_inputs=n_max, sieve_max=limit),
                  candidate_density_blocks=blocks, fixed_modulus_uniformity=uniformity,
                  prime_samples=samples)
    rendered = json.dumps(result, indent=2)+'\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered)


if __name__ == '__main__':
    main()
