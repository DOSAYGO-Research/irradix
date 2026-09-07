"""A discriminant-5 Lucas/Williams-style stage-one factoring experiment.

Not a new factoring family or a general-purpose factoring package. Arithmetic
is in (Z/NZ)[phi], phi^2=phi+1, with the norm-one unit phi^2=(1,1).
Success depends on the order of that fixed unit modulo a factor; failure
returns None and is not a primality result. See FAST_ARITHMETIC.md.
"""
from math import gcd, isqrt
from operator import index


def ring_multiply(left, right, modulus):
    """Three scalar products for (u+v*phi)(r+s*phi), reduced modulo N."""
    modulus = index(modulus)
    if modulus < 2:
        raise ValueError('expected modulus>=2')
    u, v = left
    r, s = right
    p, q, t = u*r, v*s, (u+v)*(r+s)
    return (p+q) % modulus, (t-p) % modulus


def ring_power(value, exponent, modulus):
    exponent, modulus = index(exponent), index(modulus)
    if exponent < 0 or modulus < 2:
        raise ValueError('expected exponent>=0 and modulus>=2')
    result = (1, 0)
    while exponent:
        if exponent & 1:
            result = ring_multiply(result, value, modulus)
        value = ring_multiply(value, value, modulus)
        exponent >>= 1
    return result


def _prime_powers(bound):
    sieve = bytearray(b'\x01')*(bound+1)
    sieve[:2] = b'\x00\x00'
    for p in range(2,isqrt(bound)+1):
        if sieve[p]:
            sieve[p*p::p] = b'\x00'*((bound-p*p)//p+1)
    for p in range(2,bound+1):
        if sieve[p]:
            power = p
            while power <= bound//p:
                power *= p
            yield power


def phi_factor_stage1(n, bound=100):
    """Return a proper factor via the fixed phi^2 unit, or None.

    If p!=2,5 divides N, the unit order divides p-(5|p), where (5|p) is
    the Legendre symbol. Its order must divide lcm(1,...,bound), and the
    gcd must distinguish a factor from the whole input.
    """
    n, bound = index(n), index(bound)
    if n < 2 or bound < 2:
        raise ValueError('expected n>=2 and bound>=2')
    for small in (2,5):
        if n % small == 0:
            return small if n != small else None
    value = (1,1)
    for power in _prime_powers(bound):
        value = ring_power(value, power, n)
        factor = gcd(n, value[0]-1, value[1])
        if 1 < factor < n:
            return factor
        if factor == n:
            return None
    return None


def pollard_pm1_stage1(n, bound=100):
    """Fixed-base-2 stage-one comparator with the same prime-power schedule."""
    n, bound = index(n), index(bound)
    if n < 2 or bound < 2:
        raise ValueError('expected n>=2 and bound>=2')
    factor = gcd(n,2)
    if 1 < factor < n:
        return factor
    value = 2 % n
    for power in _prime_powers(bound):
        value = pow(value,power,n)
        factor = gcd(n,value-1)
        if 1 < factor < n:
            return factor
        if factor == n:
            return None
    return None


def lucas_v_mod(parameter, exponent, modulus):
    """V_exponent(parameter,1) modulo N, by scalar binary powering."""
    parameter, exponent, modulus = index(parameter), index(exponent), index(modulus)
    if exponent < 0 or modulus < 2:
        raise ValueError('expected exponent>=0 and modulus>=2')
    parameter %= modulus
    a, b = 2 % modulus, parameter
    for bit in bin(exponent)[2:]:
        cross = (a*b-parameter) % modulus
        if bit == '0':
            a, b = (a*a-2) % modulus, cross
        else:
            a, b = cross, (b*b-2) % modulus
    return a


def lucas_factor_stage1(n, bound=100):
    """Classical scalar Lucas comparator with parameter 3, discriminant 5."""
    n, bound = index(n), index(bound)
    if n < 2 or bound < 2:
        raise ValueError('expected n>=2 and bound>=2')
    for small in (2,5):
        if n % small == 0:
            return small if n != small else None
    value = 3 % n
    for power in _prime_powers(bound):
        value = lucas_v_mod(value,power,n)
        factor = gcd(n,value-2)
        if 1 < factor < n:
            return factor
        if factor == n:
            return None
    return None
