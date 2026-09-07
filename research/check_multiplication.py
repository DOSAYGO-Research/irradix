"""Check digit multiplication independently; --output records a seeded run."""
import argparse
import json
import platform
import random
from pathlib import Path
from time import perf_counter

from check_arithmetic import canonical_word, weighted_decode
from phi_arithmetic import add, multiply
from phi_exact import fibonacci_irradix as encode, irradix as sqrt_encode


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    rng=random.Random(20260909)
    inputs=[encode(n) for n in range(128)]
    products={n:encode(n) for n in range(127*127+1)}
    for a in range(128):
        for b in range(128):
            assert multiply(inputs[a],inputs[b]) == products[a*b],(a,b)
    for a in range(-32,33):
        for b in range(-32,33):
            assert multiply(encode(a),encode(b)) == encode(a*b),(a,b)
    print('16,384 unsigned and 4,225 signed products passed.',flush=True)
    for _ in range(100):
        a=rng.getrandbits(rng.randrange(1,257))*rng.choice((-1,1))
        b=rng.getrandbits(rng.randrange(1,257))*rng.choice((-1,1))
        wa,wb=encode(a),encode(b)
        result=multiply(wa,wb)
        assert weighted_decode(result)==a*b
        assert multiply(wb,wa)==result
    for _ in range(20):
        a,b,c=(rng.randrange(-2**24,2**24) for _ in range(3))
        wa,wb,wc=map(encode,(a,b,c))
        assert multiply(wa,add(wb,wc)) == add(multiply(wa,wb),multiply(wa,wc))
    f0,f1=0,1
    for _ in range(64):
        for n in (max(0,f1-1),f1,f1+1):
            a,b=sqrt_encode(n),sqrt_encode(n+1)
            assert multiply(a,b)==sqrt_encode(n*(n+1))
        f0,f1=f1,f0+f1
    for bad in ('','-','-0','00','01','101','10001','2','+1','1 '):
        for a,b in ((bad,'1'),('1',bad),(bad,'0'),('0',bad)):
            try:
                multiply(a,b)
            except ValueError:
                pass
            else:
                raise AssertionError(('accepted malformed operand',a,b))
    for bad in (None,1,b'1'):
        for a,b in ((bad,'1'),('1',bad)):
            try:
                multiply(a,b)
            except TypeError:
                pass
            else:
                raise AssertionError(('accepted non-string',a,b))
    print('Random products, distributivity, and boundary checks passed.',flush=True)
    cases=[]
    for a_length,b_length in ((1000,1000),(20000,3)):
        a,b=canonical_word(a_length,rng),canonical_word(b_length,rng)
        if b_length==3:
            b='111' # E(6), ensures a nontrivial unbalanced multiplication.
        start=perf_counter()
        result=multiply(a,b)
        elapsed=perf_counter()-start
        assert weighted_decode(result)==weighted_decode(a)*weighted_decode(b)
        assert multiply(a,'0')=='0'
        assert multiply('-'+a,'1')=='-'+a
        assert multiply('-'+a,'-1')==a
        cases.append(dict(left_digits=a_length,right_digits=b_length,
                          result_digits=len(result),seconds=elapsed))
    timings=[]
    for bits in (32,128,512):
        a,b=encode(rng.getrandbits(bits)),encode(rng.getrandbits(bits))
        row=dict(input_bits=bits,pairs=1)
        for name,operation in (
                ('digit_multiplier',multiply),
                ('decode_multiply_encode',lambda a,b:encode(weighted_decode(a)*weighted_decode(b)))):
            samples=[]
            for _ in range(3):
                start=perf_counter()
                result=operation(a,b)
                samples.append(perf_counter()-start)
            assert weighted_decode(result)==weighted_decode(a)*weighted_decode(b)
            row[name+'_seconds']=min(samples)
        timings.append(row)
    result=dict(seed=20260909,python=platform.python_version(),platform=platform.platform(),
        checks=dict(unsigned_pairs=16384,signed_pairs=4225,random_signed_pairs=100,
                    max_random_input_bits=256,distributivity_cases=20,
                    fibonacci_boundaries=64,malformed_words=10),
        long_products=cases,timings=timings)
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    print(rendered)


if __name__=='__main__':
    main()
