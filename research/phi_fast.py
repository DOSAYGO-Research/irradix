"""Balanced exact conversion and hybrid multiplication for Irradix.

This module deliberately converts whole values to Python integers. It speeds
up that route; it is separate from phi_arithmetic.multiply's direct digit
algorithm. Per-operation Fibonacci caches have no persistent warm state.
See FAST_ARITHMETIC.md for the block and bounded-correction proofs.
"""
from math import isqrt
from operator import index

try:
    from .phi_arithmetic import _magnitude
    from .phi_exact import fibonacci_irradix
except ImportError:
    from phi_arithmetic import _magnitude
    from phi_exact import fibonacci_irradix


def _floor_phi(n):
    return (n + isqrt(5*n*n)) // 2


class _Blocks:
    def __init__(self, leaf_digits=64):
        if leaf_digits < 2:
            raise ValueError('leaf_digits must be at least two')
        self.leaf_digits = leaf_digits
        self.fibs = {0: (0, 1)}
        self.max_prefix_corrections = 0
        self.split_nodes = 0

    def fib(self, n):
        """Return (F_n,F_(n+1)) by exact fast doubling."""
        if n not in self.fibs:
            a, b = self.fib(n//2)
            c, d = a*(2*b-a), a*a+b*b
            self.fibs[n] = (d, c+d) if n % 2 else (c, d)
        return self.fibs[n]

    def coordinates(self, word):
        """Return Fibonacci block coordinates (X,Y), including leading zeros."""
        if len(word) <= self.leaf_digits:
            x = y = 0
            for bit in word:
                x, y = x+y+(bit == '1'), x
            return x, y
        r = len(word)//2
        x, y = self.coordinates(word[:-r])
        z, t = self.coordinates(word[-r:])
        f, g = self.fib(r)
        return g*x+f*y+z, f*x+(g-f)*y+t

    def length(self, n):
        # F_(2b+2) >= 2^b for b>=1, so this upper bound exceeds the answer.
        low, high = 1, 2*n.bit_length()+2
        while low < high:
            middle = (low+high+1)//2
            if self.fib(middle+2)[0] <= n+1:
                low = middle
            else:
                high = middle-1
        return low

    def encode(self, n, length=None):
        if n == 0:
            return '0'
        if length is None:
            length = self.length(n)
        if length <= self.leaf_digits:
            return fibonacci_irradix(n)
        r = length//2
        f, g = self.fib(r)
        # Exact floor(n/phi^r), using phi^(-r)=(-1)^r(F_(r+1)-F_r*phi).
        product_floor = _floor_phi(n*f)
        q = product_floor-n*g if r % 2 else n*g-product_floor-1

        def first_descendant(prefix):
            # Value of E(prefix) followed by r zeros; prefix >= 1.
            return f*(_floor_phi(prefix)+2)+(g-f)*(prefix+1)-1

        boundary = first_descendant(q)
        corrections = 0
        while boundary > n:
            q -= 1
            corrections += 1
            if q < 1 or corrections > 2:
                raise ArithmeticError('prefix correction bound violated')
            boundary = first_descendant(q)
        self.max_prefix_corrections = max(self.max_prefix_corrections, corrections)
        self.split_nodes += 1
        prefix = self.encode(q, length-r)
        rank = n-boundary
        odd = (len(prefix)-len(prefix.rstrip('0'))) % 2
        if odd:
            # A forced 0 returns to even; encode the remaining r-1 suffix bits.
            suffix = self.encode(self.fib(r+2)[0]-1+rank, r)
            return prefix+'0'+suffix[1:]
        suffix = self.encode(self.fib(r+3)[0]-1+rank, r+1)
        return prefix+suffix[1:]


def decode_balanced(word):
    """Decode a canonical signed Irradix word using a balanced block tree."""
    negative, magnitude = _magnitude(word)
    value = _Blocks().coordinates('1'+magnitude)[0]-1
    return -value if negative else value


def encode_balanced(n):
    """Encode an integer exactly using balanced prefix/suffix subdivision."""
    n = index(n)
    word = _Blocks().encode(abs(n))
    return '-'+word if n < 0 else word


def multiply_hybrid(left, right):
    """Balanced decode, native integer multiplication, balanced encode.

    This is explicitly a conversion-based algorithm, not a direct digit
    multiplier or a claim to outperform native integer multiplication.
    """
    a_negative, a_word = _magnitude(left)
    b_negative, b_word = _magnitude(right)
    blocks = _Blocks()
    a = blocks.coordinates('1'+a_word)[0]-1
    b = blocks.coordinates('1'+b_word)[0]-1
    product = a*b
    word = blocks.encode(product)
    return '-'+word if product and a_negative != b_negative else word
