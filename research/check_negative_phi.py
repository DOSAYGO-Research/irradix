"""Exact checks for NEGATIVE_PHI_CONNECTION.md; standard library only."""

from math import isqrt

from phi_exact import fibonacci_irradix


def floor_phi(n):
    if n >= 0:
        return (n + isqrt(5 * n * n)) // 2
    return -floor_phi(-n) - 1


def negative_phi_step(point):
    """Greedy -phi step on an integer pair representing u+v*phi."""
    u, v = point
    z = (-v, -u - v)  # -phi * point
    digit = z[0] - 1 + floor_phi(z[1] + 1)
    return digit, (z[0] - digit, z[1])


def main():
    for n in range(1, 10_001):
        word = fibonacci_irradix(n)
        point = (floor_phi(n) + 2, -n - 1)
        for expected in word[::-1] + "1":
            digit, point = negative_phi_step(point)
            assert digit == int(expected), (n, word, digit, expected)
        assert point == (0, 0), (n, word, point)
    print("10,000 exact negative-phi expansion identities passed.")

    residues = dict.fromkeys(range(6), 0)
    for n in range(1, 100_001):
        word = fibonacci_irradix(n)
        value = int(word, 2)
        ones = word.count("1")
        trailing = len(word) - len(word.rstrip("0"))
        predicted = 0 if ones % 2 == 0 else (1 if trailing % 2 == 0 else 2)
        assert value % 3 == predicted, (n, word, value)
        assert value % 6 != 5, (n, word, value)
        residues[value % 6] += 1
    print("100,000 exact residue identities passed.")
    print("Residues modulo 6:", residues)


if __name__ == "__main__":
    main()
