"""Exact reference implementation of the quotient-based phi representation.

This research module does not change the existing API or wire format.
Python integers and isqrt avoid any floating-point precision setting.
"""

from math import isqrt
from operator import index


def ceil_phi(n):
    """Return ceil(phi*n) exactly for nonnegative integer n."""
    n = index(n)
    if n < 0:
        raise ValueError("expected a nonnegative integer")
    return (n + isqrt(5 * n * n)) // 2 + (n != 0)


def irradix(n):
    n = index(n)
    sign = "-" if n < 0 else ""
    n = abs(n)
    if not n:
        return "0"
    digits = []
    root = isqrt(5 * n * n)
    while n:
        q = (root - n) // 2
        next_root = isqrt(5 * q * q)
        a = (q + next_root) // 2 + (q != 0)
        digits.append(str(n - a))
        n, root = q, next_root
    return sign + "".join(reversed(digits))


def derradix(rep, *, strict=True):
    """Decode; by default reject strings outside the encoder's image."""
    negative = rep.startswith("-")
    digits = rep[1:] if negative else rep
    if not digits or any(d not in "01" for d in digits):
        raise ValueError("expected a binary representation")
    n = 0
    for digit in digits:
        n = ceil_phi(n) + int(digit)
    n = -n if negative else n
    if strict and irradix(n) != rep:
        raise ValueError("noncanonical representation")
    return n


def fibonacci_irradix(n):
    """Same representation, using Fibonacci unranking and no square roots."""
    n = index(n)
    sign = "-" if n < 0 else ""
    n = abs(n)
    if n == 0:
        return "0"
    fibs = [0, 1, 1]
    while fibs[-1] <= n + 1:
        fibs.append(fibs[-1] + fibs[-2])
    k = len(fibs) - 4
    rank = n - (fibs[k + 2] - 1)
    digits, odd = ["1"], False
    for remaining in range(k - 1, 0, -1):
        if odd:
            digits.append("0")
            odd = False
        elif rank < fibs[remaining]:
            digits.append("0")
            odd = True
        else:
            digits.append("1")
            rank -= fibs[remaining]
    assert rank == 0
    return sign + "".join(digits)


def fibonacci_derradix(rep):
    """Exact inverse via Fibonacci weights, with even-gap validation."""
    negative = rep.startswith("-")
    digits = rep[1:] if negative else rep
    if rep == "0":
        return 0
    if not digits or digits[0] != "1" or any(d not in "01" for d in digits):
        raise ValueError("noncanonical representation")
    fibs = [0, 1]
    for _ in range(len(digits) + 1):
        fibs.append(fibs[-1] + fibs[-2])
    n, odd = fibs[len(digits) + 2] - 1, False
    for remaining, digit in zip(range(len(digits) - 1, 0, -1), digits[1:]):
        if digit == "1":
            if odd:
                raise ValueError("odd zero gap")
            n += fibs[remaining]
        else:
            odd = not odd
    return -n if negative else n


def guarded_encode_bits(numbers):
    """Experimental NEW format: E(n+1) + '00' + '101' per value.

    Includes a terminal delimiter and needs no doubling or suffix repair.
    The two guard bits prevent a delimiter starting in the payload.
    """
    words = []
    for n in numbers:
        n = index(n)
        if n < 0:
            raise ValueError("expected nonnegative integers")
        words.append(irradix(n + 1) + "00101")
    return "".join(words)


def guarded_decode_bits(bits):
    """Decode complete, unpadded frames; reject incomplete/noncanonical data."""
    if any(b not in "01" for b in bits):
        raise ValueError("expected bits")
    if not bits:
        return []
    parts = bits.split("101")
    if parts[-1]:
        raise ValueError("missing terminal delimiter")
    result = []
    for part in parts[:-1]:
        if not part.endswith("00"):
            raise ValueError("missing guard")
        n = derradix(part[:-2])
        if n < 1:
            raise ValueError("invalid payload")
        result.append(n - 1)
    return result
