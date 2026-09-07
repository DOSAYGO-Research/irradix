"""Exact digit arithmetic for canonical Irradix strings; standard library only.

No conversion to whole integer values, Fibonacci tables, or floating point.
Multiplication composes digit additions using Fibonacci Horner steps.
The addition/subtraction solver follows a 19-state carry relation and a
five-state output-language automaton, retaining paths until the final digit.
It is a finite-state relation implemented offline, not a streaming adder.
See ARITHMETIC.md for the invariant, carry bound, and completeness proof.
"""

from collections import deque


def _magnitude(word):
    """Validate a canonical signed word; return (negative, magnitude)."""
    if not isinstance(word, str):
        raise TypeError('expected an Irradix string')
    negative = word.startswith('-')
    digits = word[1:] if negative else word
    if digits == '0' and not negative:
        return False, digits
    if not digits or digits[0] != '1':
        raise ValueError('noncanonical Irradix word')
    odd = False
    for bit in digits[1:]:
        if bit == '0':
            odd = not odd
        elif bit == '1' and not odd:
            pass
        else:
            raise ValueError('noncanonical Irradix word')
    return negative, digits


def _increment_unsigned(word):
    if word == '0':
        return '1'
    odd, pivot = False, None
    for i in range(1, len(word)):
        if word[i] == '0':
            if not odd:
                pivot = i
            odd = not odd
    if pivot is None:
        return '1' + '0' * len(word)
    return word[:pivot] + '1' + '0' * (len(word)-pivot-1)


def _decrement_unsigned(word):
    if word == '1':
        return '0'
    pivot = word.rfind('1', 1)
    if pivot == -1:
        return '1' * (len(word)-1)
    remaining = len(word)-pivot-1
    suffix = '' if remaining == 0 else '0' + '1' * (remaining-1)
    return word[:pivot] + '0' + suffix


def increment(word):
    """Return E(n+1) from E(n), including signed n; linear digit work."""
    negative, magnitude = _magnitude(word)
    if not negative:
        return _increment_unsigned(magnitude)
    result = _decrement_unsigned(magnitude)
    return '0' if result == '0' else '-' + result


def decrement(word):
    """Return E(n-1) from E(n), including signed n; linear digit work."""
    negative, magnitude = _magnitude(word)
    if negative:
        return '-' + _increment_unsigned(magnitude)
    if magnitude == '0':
        return '-1'
    return _decrement_unsigned(magnitude)


def _carry_machine():
    """Generate, then trim, the proven finite carry rectangle."""
    rectangle = {(u, v) for u in range(-5, 6) for v in range(-4, 5)}
    reachable, queue = {(0, 0)}, deque([(0, 0)])
    while queue:
        u, v = queue.popleft()
        for digit in (-1, 0, 1, 2):
            target = (v + digit, u + v)
            if target in rectangle and target not in reachable:
                reachable.add(target)
                queue.append(target)
    live = {carry for carry in reachable if sum(carry) == 1}
    while True:
        expanded = live | {(u, v) for u, v in reachable
                           if any((v+d, u+v) in live for d in (-1, 0, 1, 2))}
        if expanded == live:
            break
        live = expanded
    states = tuple(sorted(live))
    indices = {state: i for i, state in enumerate(states)}
    transitions = tuple(tuple(indices.get((v+d, u+v), -1)
                              for d in (-1, 0, 1, 2)) for u, v in states)
    accepting = frozenset(i for i, state in enumerate(states) if sum(state) == 1)
    return states, transitions, indices[(0, 0)], accepting


CARRY_STATES, _CARRY_NEXT, _CARRY_START, _CARRY_FINAL = _carry_machine()

# Padded augmented output language: 0*(10 | 11(1|00)*(epsilon|0)).
# States: padding, initial augmentation bit, zero, even, odd.
_OUTPUT_NEXT = ((0, 1), (2, 3), (-1, -1), (4, 3), (3, -1))
_OUTPUT_FINAL = frozenset((2, 3, 4))


def _transition_tables(subtract):
    """Combine carry and output-language states; a table for each input pair."""
    tables = []
    for left in (0, 1):
        for right in (0, 1):
            rows = []
            for carry in range(len(CARRY_STATES)):
                for language in range(5):
                    edges = []
                    for output in (0, 1):
                        target_language = _OUTPUT_NEXT[language][output]
                        if target_language == -1:
                            continue
                        digit = right + output - left if subtract else left + right - output
                        target_carry = _CARRY_NEXT[carry][digit+1]
                        if target_carry != -1:
                            edges.append((5*target_carry+target_language, output))
                    rows.append(tuple(edges))
            tables.append(tuple(rows))
    return tuple(tables)


_ADD_TABLE = _transition_tables(False)
_SUBTRACT_TABLE = _transition_tables(True)
_FINAL = frozenset(5*c+q for c in _CARRY_FINAL for q in _OUTPUT_FINAL)
_START = 5 * _CARRY_START


def _solve(left, right, subtract=False, *, stats=None):
    """Solve a+b=c or c+b=a for unsigned canonical words a,b."""
    width = max(len(left), len(right)) + 3
    a, b = ('1'+left).zfill(width), ('1'+right).zfill(width)
    table = _SUBTRACT_TABLE if subtract else _ADD_TABLE
    frontier = {_START}
    history = []
    max_frontier = 1
    for abit, bbit in zip(a, b):
        column = table[2*(abit == '1')+(bbit == '1')]
        predecessors = {}
        for state in frontier:
            for target, bit in column[state]:
                if target not in predecessors:
                    predecessors[target] = (state, bit)
        if not predecessors:
            raise ArithmeticError('no arithmetic path')
        history.append(predecessors)
        frontier = predecessors.keys()
        max_frontier = max(max_frontier, len(predecessors))
    accepting = set(frontier) & _FINAL
    if len(accepting) != 1:
        raise ArithmeticError('expected one canonical result')
    state = accepting.pop()
    output = []
    for predecessors in reversed(history):
        state, bit = predecessors[state]
        output.append('1' if bit else '0')
    augmented = ''.join(reversed(output)).lstrip('0')
    if stats is not None:
        stats.update(columns=width, max_frontier=max_frontier,
                     history_entries=sum(map(len, history)))
    return augmented[1:]


def add(left, right):
    """Return E(a+b) from canonical signed E(a), E(b), without decoding."""
    a_negative, a = _magnitude(left)
    b_negative, b = _magnitude(right)
    if a == '0':
        return right
    if b == '0':
        return left
    if a_negative == b_negative:
        result = _solve(a, b)
        return '-' + result if a_negative else result
    # Binary numeric order equals integer order; shortlex compares magnitudes.
    if (len(a), a) < (len(b), b):
        a, b, a_negative = b, a, b_negative
    if a == b:
        return '0'
    result = _solve(a, b, subtract=True)
    return '-' + result if a_negative else result


def is_sum(left, right, result):
    """Check nonnegative E(a)+E(b)=E(c) using a single bounded-state pass.

    All three supplied words are validated. Signed inputs are rejected;
    use add for signed arithmetic. This checker stores no history.
    """
    words = []
    for word in (left, right, result):
        negative, magnitude = _magnitude(word)
        if negative:
            raise ValueError('is_sum expects nonnegative words')
        words.append('1'+magnitude)
    width = max(map(len, words))
    a, b, c = (word.zfill(width) for word in words)
    carry = _CARRY_START
    for x, y, z in zip(a, b, c):
        digit = (x == '1') + (y == '1') - (z == '1')
        carry = _CARRY_NEXT[carry][digit+1]
        if carry == -1:
            return False
    return carry in _CARRY_FINAL


def multiply(left, right):
    """Return E(a*b) using Fibonacci Horner steps and the carry adder.

    Reads the shorter magnitude as the multiplier. For each augmented digit
    d, (x,y) <- (x+y+d*abs(a), x); subtract abs(a) at the end to account for
    W(1E(b))=abs(b)+1. This is repeated digit addition, not a finite-state
    multiplier. No operands are decoded into whole integer values.
    """
    a_negative, a = _magnitude(left)
    b_negative, b = _magnitude(right)
    negative = a_negative != b_negative
    if a == '0' or b == '0':
        return '0'
    if len(a) < len(b):
        a, b = b, a
    if b == '1':
        return '-' + a if negative else a
    # Start after the augmentation bit 1, whose scaled weight is a.
    x, y = a, '0'
    for bit in b:
        previous = x
        x = add(x, y)
        if bit == '1':
            x = add(x, a)
        y = previous
    result = _solve(x, a, subtract=True)
    return '-' + result if negative else result
