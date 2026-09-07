"""Independent arithmetic checks and reproducible local benchmarks.

Run from the repository root. --output records counts, bounds, and timings.
"""
import argparse
from collections import deque
import json
import platform
import random
from pathlib import Path
from time import perf_counter

from phi_arithmetic import (CARRY_STATES, _CARRY_NEXT, _CARRY_FINAL,
                            _CARRY_START, _ADD_TABLE, _SUBTRACT_TABLE, _START,
                            _solve, add, decrement, increment, is_sum)
from phi_exact import fibonacci_irradix as encode, irradix as sqrt_encode


def weighted_decode(word):
    """Independent, unbounded Fibonacci-weight oracle; no carry automaton."""
    negative = word.startswith('-')
    if negative:
        word = word[1:]
    a, b, value = 1, 1, 0
    for bit in reversed('1'+word):
        if bit == '1':
            value += a
        a, b = b, a+b
    value -= 1
    return -value if negative else value


def canonical_word(length, rng):
    bits, odd = ['1'], False
    for _ in range(length-1):
        bit = '0' if odd else rng.choice('01')
        bits.append(bit)
        odd = not odd if bit == '0' else False
    return ''.join(bits)


def frontier_bound(tables):
    """Exhaust the finite subset graph over all four input bit pairs."""
    initial = frozenset((_START,))
    seen, queue = {initial}, deque((initial,))
    while queue:
        states = queue.popleft()
        for table in tables:
            target = frozenset(t for s in states for t, _ in table[s])
            if target not in seen:
                seen.add(target)
                queue.append(target)
    return dict(reachable_subsets=len(seen), max_active_states=max(map(len,seen)))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rng = random.Random(20260907)
    assert len(CARRY_STATES) == 19
    frontier_certificate = dict(add=frontier_bound(_ADD_TABLE),
                                subtract=frontier_bound(_SUBTRACT_TABLE))
    assert frontier_certificate == dict(
        add=dict(reachable_subsets=41,max_active_states=5),
        subtract=dict(reachable_subsets=39,max_active_states=5))
    assert {CARRY_STATES[i] for i in _CARRY_FINAL} == {(-1,2),(0,1),(1,0),(2,-1)}
    for index, (u, v) in enumerate(CARRY_STATES):
        assert -5 <= u <= 5 and -4 <= v <= 4
        for digit, target in zip((-1,0,1,2), _CARRY_NEXT[index]):
            if target != -1:
                assert CARRY_STATES[target] == (v+digit, u+v)
    words = [encode(n) for n in range(100_002)]
    for n in range(100_001):
        assert increment(words[n]) == words[n+1], n
        assert decrement(words[n+1]) == words[n], n
    print('100,001 successor/predecessor pairs passed.', flush=True)
    for a in range(256):
        for b in range(256):
            result = add(words[a], words[b])
            assert result == words[a+b], (a,b)
            assert is_sum(words[a], words[b], result)
            assert not is_sum(words[a], words[b], words[a+b+1])
    signed = {n: encode(n) for n in range(-129,130)}
    for a in range(-64,65):
        assert increment(signed[a]) == signed[a+1]
        assert decrement(signed[a]) == signed[a-1]
        for b in range(-64,65):
            assert add(signed[a],signed[b]) == signed[a+b], (a,b)
    # Exercise the core solver at zero as well as public zero shortcuts.
    for a in range(256):
        assert _solve(words[a], '0') == words[a]
        assert _solve(words[a], words[a], subtract=True) == '0'
    for a in range(16):
        for b in range(16):
            for c in range(32):
                assert is_sum(words[a],words[b],words[c]) == (a+b==c)
    print('65,536 unsigned and 16,641 signed addition pairs passed.', flush=True)

    malformed = ('', '-', '-0', '00', '01', '101', '10001', '12', '+1', ' 1', '1\n')
    for bad in malformed:
        for operation in (increment, decrement, lambda w: add(w,'1'),
                          lambda w: add('1',w), lambda w: is_sum(w,'1','10'),
                          lambda w: is_sum('1',w,'10'), lambda w: is_sum('1','1',w)):
            try:
                operation(bad)
            except ValueError:
                pass
            else:
                raise AssertionError(('accepted malformed word',bad))
    for bad in (None, 1, b'1'):
        try:
            increment(bad)
        except TypeError:
            pass
        else:
            raise AssertionError(('accepted wrong type',bad))
    try:
        is_sum('-1','1','0')
    except ValueError:
        pass
    else:
        raise AssertionError('is_sum accepted a signed word')

    for _ in range(1000):
        a = rng.getrandbits(rng.randrange(1,4097)) * rng.choice((-1,1))
        b = rng.getrandbits(rng.randrange(1,4097)) * rng.choice((-1,1))
        wa, wb = encode(a), encode(b)
        result = add(wa,wb)
        assert weighted_decode(result) == a+b
        assert add(wb,wa) == result
        assert add(result, encode(-b)) == wa
    # Independent square-root encoder across length boundaries.
    f0, f1 = 0, 1
    for _ in range(300):
        for n in (max(0,f1-2),max(0,f1-1),f1,f1+1):
            w = sqrt_encode(n)
            assert increment(w) == sqrt_encode(n+1)
            assert add(w,w) == sqrt_encode(2*n)
        f0, f1 = f1, f0+f1
    print('Random signed arithmetic and 300 Fibonacci boundaries passed.', flush=True)

    long_runs=[]
    for length in (1000,10000,100000):
        a, b = canonical_word(length,rng), canonical_word(length,rng)
        stats={}
        start=perf_counter()
        result=_solve(a,b,stats=stats)
        elapsed=perf_counter()-start
        assert weighted_decode(result) == weighted_decode(a)+weighted_decode(b)
        assert is_sum(a,b,result)
        # Long propagation and parity-dependent low digits.
        assert increment('1'*length) == '1'+'0'*length
        assert increment('1'*(length-1)+'0') == '1'*length
        assert increment('1'+'0'*(length-1))[-1] == str((length-1)%2)
        assert increment('11'+'0'*(length-2))[-1] == str((length-2)%2)
        long_runs.append(dict(input_digits=length,output_digits=len(result),
                              seconds=elapsed,**stats))
    print('100,000-digit addition passed an independent weight oracle.', flush=True)

    timings=[]
    for bits in (64,256,1024,4096):
        pairs=[(encode(rng.getrandbits(bits)),encode(rng.getrandbits(bits)))
               for _ in range(10)]
        def converted(a,b):
            return encode(weighted_decode(a)+weighted_decode(b))
        methods={'carry_adder':add,'decode_add_encode':converted}
        entry={'input_bits':bits,'pairs':len(pairs)}
        for name,method in methods.items():
            samples=[]
            for _ in range(3):
                start=perf_counter()
                for a,b in pairs:
                    method(a,b)
                samples.append(perf_counter()-start)
            entry[name+'_seconds']=min(samples)
        timings.append(entry)
    increment_rng = random.Random(20260908)
    increment_timings = []
    for bits in (64,256,1024,4096):
        inputs = [encode(increment_rng.getrandbits(bits)) for _ in range(10)]
        row = dict(input_bits=bits, words=len(inputs))
        for name, method in (
                ('incrementer', increment),
                ('decode_increment_encode', lambda w: encode(weighted_decode(w)+1))):
            samples = []
            for _ in range(3):
                start = perf_counter()
                for word in inputs:
                    method(word)
                samples.append(perf_counter()-start)
            row[name+'_seconds'] = min(samples)
        increment_timings.append(row)
    result=dict(seed=20260907,python=platform.python_version(),
                platform=platform.platform(),carry_states=len(CARRY_STATES),
                output_language_states=5,combined_state_bound=95,frontier_certificate=frontier_certificate,
                terminal_carries=[list(CARRY_STATES[i]) for i in sorted(_CARRY_FINAL)],
                checks=dict(successor_predecessor_pairs=100001,unsigned_addition_pairs=65536,
                    signed_addition_pairs=16641,exhaustive_relation_triples=8192,
                    random_signed_pairs=1000,max_random_input_bits=4096,
                    fibonacci_boundaries=300,malformed_strings=len(malformed)),
                long_additions=long_runs,timings=timings,
                increment_timings=dict(seed=20260908,runs=increment_timings))
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.write_text(rendered)
    print(rendered)


if __name__=='__main__':
    main()
