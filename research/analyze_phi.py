"""Reproduce the proof checks and measurements in PHI_ANALYSIS.md.

Run: python research/analyze_phi.py [--legacy]
The default run uses only the standard library. --legacy needs requirements.txt.
All reported storage counts include final byte rounding, but no outer file header.
"""

import argparse
import itertools
import json
import math
import random
import sys
import time
from pathlib import Path

from phi_exact import (
    ceil_phi, derradix, guarded_decode_bits, guarded_encode_bits, irradix,
    fibonacci_irradix, fibonacci_derradix,
)


def legacy_bits(numbers):
    words = []
    for n in numbers:
        word = irradix(2 * (n + 1))
        words.append(word + ("0101" if word.endswith("10") else ""))
    return "101".join(words)


def delta_bits(numbers):
    words = []
    for n in numbers:
        value = bin(n + 1)[2:]
        width = bin(len(value))[2:]
        words.append("0" * (len(width) - 1) + width + value[1:])
    return "".join(words)


def delta_decode(bits):
    result, pos = [], 0
    while pos < len(bits):
        zeros = 0
        while bits[pos] == "0":
            zeros += 1
            pos += 1
        width = int(bits[pos:pos + zeros + 1], 2)
        pos += zeros + 1
        result.append(int("1" + bits[pos:pos + width - 1], 2) - 1)
        pos += width - 1
    return result


def fibonacci_bits(numbers):
    words = []
    for n in numbers:
        n += 1
        fibs = [1, 2]
        while fibs[-1] <= n:
            fibs.append(fibs[-1] + fibs[-2])
        fibs.pop()
        digits = ["0"] * len(fibs)
        for i in range(len(fibs) - 1, -1, -1):
            if fibs[i] <= n:
                n -= fibs[i]
                digits[i] = "1"
        words.append("".join(digits) + "1")
    return "".join(words)


def fibonacci_decode(bits):
    result, value, a, b, previous = [], 0, 1, 2, "0"
    for digit in bits:
        if previous == digit == "1":
            result.append(value - 1)
            value, a, b, previous = 0, 1, 2, "0"
        else:
            value += a * int(digit)
            a, b, previous = b, a + b, digit
    assert previous == "0" and value == 0
    return result


def padded_size(size):
    return 8 * ((size + 7) // 8)


def checks():
    previous = -1
    for n in range(100_001):
        word = irradix(n)
        assert fibonacci_irradix(n) == word
        assert fibonacci_derradix(word) == n
        assert "101" not in word
        assert int(word, 2) > previous
        previous = int(word, 2)
        if n <= 10_000:
            assert derradix(word) == n
            assert derradix(irradix(-n)) == -n
    # Exact length thresholds M_k = F_(k+2)-1, including very large integers.
    a, b = 1, 2
    for k in range(1, 501):
        minimum = b - 1
        assert len(irradix(minimum)) == k
        for n in (minimum - 1, minimum, minimum + 1):
            assert fibonacci_irradix(n) == irradix(n)
            assert fibonacci_derradix(irradix(n)) == n
        if k > 1:
            assert len(irradix(minimum - 1)) == k - 1
        assert ceil_phi(minimum) == a + b - 1
        a, b = b, a + b
    count = 0
    for width in range(4):
        for values in itertools.product(range(16), repeat=width):
            values = list(values)
            assert guarded_decode_bits(guarded_encode_bits(values)) == values
            assert delta_decode(delta_bits(values)) == values
            assert fibonacci_decode(fibonacci_bits(values)) == values
            count += 1
    for malformed in ["", "101", "10001", "01", "-0", "2"]:
        try:
            derradix(malformed)
        except ValueError:
            pass
        else:
            raise AssertionError(malformed)
    for malformed in ["1", "101", "000101", "10001", "x"]:
        try:
            guarded_decode_bits(malformed)
        except ValueError:
            pass
        else:
            raise AssertionError(malformed)
    return {"no_101_and_monotonic_values": 100_001,
            "signed_roundtrip_magnitudes": 10_001,
            "fibonacci_length_thresholds": 500,
            "sequences_per_experimental_codec": count}


def benchmarks():
    rng = random.Random(20260907)
    samples = {}
    for width in (8, 32, 256, 512):
        samples[f"uniform_{width}_bit"] = [
            rng.randrange(1 << (width - 1), 1 << width) for _ in range(1000)
        ]
    samples["decimal_50_to_100_digits"] = []
    for _ in range(1000):
        digits = rng.randint(50, 100)
        samples["decimal_50_to_100_digits"].append(
            rng.randrange(10 ** (digits - 1), 10 ** digits))
    rows = []
    for name, values in samples.items():
        widths = [max(1, n.bit_length()) for n in values]
        payload = sum(widths)
        delta = delta_bits(values)
        fib = fibonacci_bits(values)
        guarded = guarded_encode_bits(values)
        assert delta_decode(delta) == values
        assert fibonacci_decode(fib) == values
        assert guarded_decode_bits(guarded) == values
        rows.append({
            "dataset": name, "count": len(values), "raw_payload_bits": payload,
            "irradix_bits": padded_size(len(legacy_bits(values))),
            "l1_bits": padded_size(len(legacy_bits(widths)) + 7 + payload),
            "guarded_phi_bits": padded_size(len(guarded)),
            "fibonacci_bits": padded_size(len(fib)),
            "elias_delta_bits": padded_size(len(delta)),
            "vbyte_bits": sum(8 * ((w + 6) // 7) for w in widths),
        })
    return rows, samples


def prime_measurements():
    values = [int(irradix(n), 2) for n in range(1, 1001)]
    sieve = bytearray(b"\1") * (max(values) + 1)
    sieve[:2] = b"\0\0"
    for p in range(2, math.isqrt(max(values)) + 1):
        if sieve[p]:
            sieve[p*p::p] = b"\0" * ((max(values) - p*p) // p + 1)
    return {"count": len(values), "max_mapped_value": max(values),
            "original_primes": sum(sieve[1:1001]),
            "mapped_primes": sum(sieve[n] for n in values),
            "mapped_odd_count": sum(n % 2 for n in values),
            "naive_log_expected_count": sum(1 / math.log(n) for n in values if n >= 2),
            "parity_adjusted_heuristic_count": sum(
                2 / math.log(n) for n in values if n >= 3 and n % 2) + (2 in values)}


def legacy_checks(samples):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    import irradix as old
    old.set_precision(100)
    for n in range(10_001):
        assert old.irradix(n) == irradix(n)
    # A precision failure is expected; report evidence, not a passing assertion.
    precision_cases = []
    for n in (10**100 - 1, 10**100, 10**100 + 1, 10**101 + 12345):
        word = old.irradix(n)
        precision_cases.append({"input": str(n), "exact_encoding_matches": word == irradix(n),
                                "legacy_roundtrip_matches": old.derradix(word) == n})
    values = samples["uniform_256_bit"][:100]
    timings = {}
    for name, encoder in (("legacy", old.irradix), ("exact", irradix),
                          ("fibonacci", fibonacci_irradix)):
        runs = []
        for _ in range(3):
            start = time.perf_counter()
            words = [encoder(n) for n in values]
            runs.append(time.perf_counter() - start)
        assert words == [irradix(n) for n in values]
        timings[name + "_seconds_best_of_3"] = min(runs)
    # Isolate the existing framing from numerical approximation.
    old_encoder, old_decoder = old.irradix, old.derradix
    old.irradix, old.derradix = irradix, lambda rep: derradix(rep, strict=False)
    try:
        for width in range(4):
            for values in itertools.product(range(16), repeat=width):
                assert old.decode(old.encode(values)) == list(values)
                assert old.l1decode(old.l1encode(values)) == list(values)
        for values in samples.values():
            assert old.decode(old.encode(values)) == values
            assert old.l1decode(old.l1encode(values)) == values
    finally:
        old.irradix, old.derradix = old_encoder, old_decoder
    return {"small_encodings_agree": 10_001, "precision_cases": precision_cases,
            "timing_100_values_256_bits": timings,
            "exact_arithmetic_legacy_framing_roundtrips": "passed"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy", action="store_true")
    args = parser.parse_args()
    result = {"checks": checks()}
    result["benchmarks"], samples = benchmarks()
    result["prime_measurements"] = prime_measurements()
    if args.legacy:
        result["legacy"] = legacy_checks(samples)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
