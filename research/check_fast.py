"""Balanced conversion/multiplication and discriminant-5 factoring checks."""
import argparse
import json
import platform
import random
from math import gcd, isqrt
from pathlib import Path
from time import perf_counter
import tracemalloc

from check_arithmetic import canonical_word, weighted_decode
from phi_arithmetic import multiply
from phi_exact import fibonacci_irradix as encode, irradix as sqrt_encode
from phi_fast import _Blocks, encode_balanced, decode_balanced, multiply_hybrid
from phi_factor import (ring_multiply, ring_power, phi_factor_stage1,
                        pollard_pm1_stage1, lucas_factor_stage1, lucas_v_mod)


def primes_below(limit):
    return [n for n in range(2,limit) if all(n%d for d in range(2,isqrt(n)+1))]


def best_time(operation, repetitions=3):
    samples=[]
    for _ in range(repetitions):
        start=perf_counter(); operation(); samples.append(perf_counter()-start)
    return min(samples)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    rng=random.Random(20260910)
    max_corrections=0
    for n in range(20001):
        blocks=_Blocks(leaf_digits=2) # Force recursive branches on small examples.
        word=blocks.encode(n)
        assert word==encode(n),n
        assert blocks.coordinates('1'+word)[0]-1==n,n
        max_corrections=max(max_corrections,blocks.max_prefix_corrections)
    assert max_corrections==2
    for n in range(-1000,1001):
        assert encode_balanced(n)==encode(n)
        assert decode_balanced(encode(n))==n
    for _ in range(300):
        n=rng.getrandbits(rng.randrange(1,8193))*rng.choice((-1,1))
        word=encode_balanced(n)
        assert word==encode(n)
        assert decode_balanced(word)==n
    f0,f1=0,1
    for _ in range(500):
        for n in (max(0,f1-2),max(0,f1-1),f1,f1+1):
            assert encode_balanced(n)==sqrt_encode(n),n
        f0,f1=f1,f0+f1
    for a in range(-32,33):
        for b in range(-32,33):
            assert multiply_hybrid(encode(a),encode(b))==encode(a*b),(a,b)
    for _ in range(100):
        a=rng.getrandbits(rng.randrange(1,4097))*rng.choice((-1,1))
        b=rng.getrandbits(rng.randrange(1,4097))*rng.choice((-1,1))
        result=multiply_hybrid(encode(a),encode(b))
        assert weighted_decode(result)==a*b
    for bad in ('','-','-0','01','00','101','10001','1 ','2'):
        for fn in (decode_balanced,lambda w:multiply_hybrid(w,'0'),
                   lambda w:multiply_hybrid('0',w)):
            try: fn(bad)
            except ValueError: pass
            else: raise AssertionError(('invalid word accepted',bad))
    for bad in (None,1,b'1'):
        try: decode_balanced(bad)
        except TypeError: pass
        else: raise AssertionError('non-string accepted')
    for bad in (None,1.5,'1'):
        try: encode_balanced(bad)
        except TypeError: pass
        else: raise AssertionError('non-integer accepted')
    print('Balanced conversion and signed hybrid multiplication checks passed.',flush=True)

    prime_list=primes_below(1000)
    for p in prime_list:
        if p in (2,5): continue
        legendre=pow(5,(p-1)//2,p)
        chi=1 if legendre==1 else -1
        assert ring_power((1,1),p-chi,p)==(1,0),p
    for _ in range(1000):
        n=rng.randrange(2,100000)
        u,v,r,s=(rng.randrange(n) for _ in range(4))
        result=ring_multiply((u,v),(r,s),n)
        assert result==((u*r+v*s)%n,(u*s+v*r+v*s)%n)
        norm=lambda a,b:a*a+a*b-b*b
        assert norm(*result)%n==norm(u,v)*norm(r,s)%n
        e=rng.randrange(1000)
        a,b=ring_power((1,1),e,n)
        assert (2*a+b)%n==lucas_v_mod(3,e,n)
    invalid=[(1,10),(10,1),(-1,10)]
    for operation in (phi_factor_stage1,pollard_pm1_stage1,lucas_factor_stage1):
        for n,bound in invalid:
            try: operation(n,bound)
            except ValueError: pass
            else: raise AssertionError('invalid factoring arguments accepted')
        for p in prime_list:
            assert operation(p,27) is None,p
        for n in range(4,1000):
            factor=operation(n,27)
            assert factor is None or 1<factor<n and n%factor==0,(n,factor)
    for operation in (ring_power,lambda a,e,n:lucas_v_mod(3,e,n)):
        for exponent,modulus in ((-1,10),(1,1)):
            try: operation((1,1),exponent,modulus)
            except ValueError: pass
            else: raise AssertionError('invalid power arguments accepted')
    demos=[]
    for p,q,bound in ((107,1019,27),(113,1019,16)):
        n=p*q
        demos.append(dict(n=n,p=p,q=q,bound=bound,phi=phi_factor_stage1(n,bound),
            lucas=lucas_factor_stage1(n,bound),pollard_pm1=pollard_pm1_stage1(n,bound)))
    assert demos[0]['phi']==107 and demos[0]['pollard_pm1'] is None
    assert demos[1]['phi'] is None and demos[1]['pollard_pm1']==113
    pool=primes_below(10000)
    pool=[p for p in pool if p>=1000]
    semiprimes=[tuple(rng.sample(pool,2)) for _ in range(200)]
    factoring=[]
    for bound in (16,64,256):
        row=dict(bound=bound,semiprimes=len(semiprimes))
        outputs={}
        for name,operation in [('phi',phi_factor_stage1),('lucas',lucas_factor_stage1),('pollard_pm1',pollard_pm1_stage1)]:
            start=perf_counter()
            results=[operation(p*q,bound) for p,q in semiprimes]
            row[name+'_seconds']=perf_counter()-start
            row[name+'_successes']=sum(f is not None for f in results)
            for (p,q),factor in zip(semiprimes,results):
                assert factor is None or factor in (p,q)
            outputs[name]=results
        assert outputs['phi']==outputs['lucas']
        row['either_phi_or_pm1']=sum(a is not None or b is not None
                                    for a,b in zip(outputs['phi'],outputs['pollard_pm1']))
        factoring.append(row)
    print('Ring identities, prime-order bound, and factoring checks passed.',flush=True)

    timings=[]
    for length in (128,1024,8192,16384):
        a,b=canonical_word(length,rng),canonical_word(length,rng)
        ai,bi=weighted_decode(a),weighted_decode(b)
        expected=ai*bi
        result=multiply_hybrid(a,b)
        assert weighted_decode(result)==expected
        row=dict(input_digits=length,output_digits=len(result))
        row['hybrid_seconds']=best_time(lambda:multiply_hybrid(a,b))
        row['previous_conversion_seconds']=best_time(lambda:encode(weighted_decode(a)*weighted_decode(b)))
        row['native_product_only_seconds']=best_time(lambda:ai*bi)
        if length<=1024:
            assert multiply(a,b)==result
            row['digit_horner_seconds']=best_time(lambda:multiply(a,b),1)
        row['balanced_decode_seconds']=best_time(lambda:decode_balanced(a))
        row['rolling_decode_seconds']=best_time(lambda:weighted_decode(a))
        row['balanced_encode_seconds']=best_time(lambda:encode_balanced(expected))
        row['previous_encode_seconds']=best_time(lambda:encode(expected))
        timings.append(row)
    memories=[]
    for length in (4096,16384):
        word=canonical_word(length,rng)
        value=weighted_decode(word)
        row=dict(output_digits=length)
        for name,operation in [('balanced',encode_balanced),('previous',encode)]:
            tracemalloc.start()
            assert operation(value)==word
            _,peak=tracemalloc.get_traced_memory();tracemalloc.stop()
            row[name+'_peak_python_bytes']=peak
        memories.append(row)
    a,b=canonical_word(100000,rng),canonical_word(100000,rng)
    start=perf_counter();result=multiply_hybrid(a,b);elapsed=perf_counter()-start
    assert weighted_decode(result)==weighted_decode(a)*weighted_decode(b)
    large=dict(input_digits=100000,output_digits=len(result),hybrid_seconds=elapsed)
    print('100,000-digit by 100,000-digit hybrid product passed.',flush=True)
    result=dict(seed=20260910,python=platform.python_version(),platform=platform.platform(),
        checks=dict(forced_recursive_encodings=20001,signed_roundtrips=2001,
            random_roundtrips=300,max_random_conversion_bits=8192,fibonacci_boundaries=500,
            signed_product_pairs=4225,random_signed_products=100,max_random_product_bits=4096,
            observed_max_prefix_corrections=max_corrections,ring_identities=1000,
            prime_order_checks=len(prime_list)-2),
        multiplication_timings=timings,encoding_memory=memories,large_product=large,
        factoring_examples=demos,factoring_experiment=factoring)
    rendered=json.dumps(result,indent=2)+'\n'
    if args.output:args.output.write_text(rendered)
    print(rendered)


if __name__=='__main__':main()
