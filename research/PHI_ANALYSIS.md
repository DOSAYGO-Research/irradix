# Exact characterization and practical consequences

Read the [mathematical paper](../output/pdf/phi-proof.pdf) or its [TeX source](../output/pdf/phi-proof.tex). The formal companion is [PhiPacking.lean](lean/PhiPacking.lean).

The exact quotient algorithm produces precisely the positive binary words with an initial `1` and an even number of zeros between successive ones. Trailing zeros are unrestricted. This is the **even shift**, a known language in symbolic dynamics; the proof establishes the connection to this repository's particular integer algorithm. It is not the usual positional base-phi expansion.

Let `t = frac(phi*q)`, `a = phi - 1`, and `c = 2 - phi = a²`. A `1` is admissible after a positive prefix exactly when `t > c`. Appending zero changes the phase to `a*(1-t)`, so

```
new_phase - c = -a * (old_phase - c).
```

After a `1` the phase is above `c`; each zero flips sides. Consequently a following `1` is allowed exactly after an even number of zeros. This proves `101` is impossible and also excludes `10001`, `1000001`, etc. Mere `101` avoidance is necessary but insufficient for validity.

## Exact algorithms

[phi_exact.py](phi_exact.py) provides two independent implementations without modifying the production API:

- `irradix` / `derradix`: exact integer-square-root quotient and ceiling operations.
- `fibonacci_irradix` / `fibonacci_derradix`: the same mapping using Fibonacci ranks and weights; no irrational arithmetic or square roots.
- `guarded_encode_bits` / `guarded_decode_bits`: an explicitly different experimental framing format, `E(n+1) + 00 + 101`, with strict validation.

For a valid length-`k` word `1 d_(k-2) ... d_0`, its integer is

```
F_(k+2) - 1 + sum(d_j * F_(j+1), j = 0 .. k-2).
```

There are exactly `F_(k+1)` words of length `k`, covering the consecutive integers `F_(k+2)-1` through `F_(k+3)-2`. This gives the approximately 44% bit expansion. For 100 random 256-bit integers, the recorded best-of-three encoder timings were approximately 0.493 s for the existing implementation, 0.044 s for exact square roots, and 0.0077 s for Fibonacci ranking. These are local Python measurements, not portable throughput guarantees.

## Packing recommendations

1. Replace approximate arithmetic with the Fibonacci algorithm after choosing API compatibility and malformed-input behavior. The reference preserves the mathematical codewords, not numerical mistakes made by finite precision.
2. For large integers, keep the payload in ordinary binary and encode its length. Compare against Elias delta and other length codes; compress repeated lengths or use a shared block width when the data supports it. Direct Irradix's 44% expansion cannot beat VByte's asymptotic 14.3% expansion on raw payload size.
3. If avoiding `101` is the only required constraint, an enumerative code over **all** `101`-free words can approach 1.232 output bits per input bit before framing. That changes the code; it cannot be achieved merely by accelerating this mapping.
4. Use byte accumulators or streaming bit readers to avoid materializing multiple copies of whole bit strings. The existing `olencode` and `oldecode` are wrappers around batch functions, not incremental implementations.
5. Specify malformed-input rejection, termination, and byte padding. Delimiter exclusion within payloads does not alone establish boundary safety. The reference guard scheme is simple to prove but is not a byte-level streaming implementation or error-correcting code.

The sampled length-first advantage over VByte is reproducible, but not unique to phi: on the seeded 50–100 digit sample, L1 used 264,240 bits, Elias delta 263,072 bits, and VByte 286,984 bits. The original “perfect encoding” benchmark is not a general entropy bound; concatenating variable-size lengths without framing does not by itself define a decodable code.

The [extended analysis](NEGATIVE_PHI_CONNECTION.md) derives the exact correspondence with greedy negative-phi expansions and stronger arithmetic consequences: prime images above 3 have odd bit length and are 1 modulo 6; every even-length block above length 2 is composite. The proportion of images coprime to 6 oscillates with length, while residues are equidistributed at each fixed modulus coprime to 6. Written proofs and exact checks accompany these results; they are outside the current Lean formalization.

For the first 1,000 inputs, the 94 mapped primes compare with a modulo-6 logarithmic heuristic of 94.46. At 100,000 inputs, the exact sieve gives 4,319 versus the heuristic's 4,342.72. This supersedes the earlier parity-only estimate of about 107 for the small sample. It does not prove a prime asymptotic or infinitely many prime images. See [residue_measurements.json](residue_measurements.json) for all tested prefixes.

## Reproduction

```sh
python3 research/analyze_phi.py
python3 research/check_negative_phi.py
python3 research/analyze_residues.py
# To compare with the original implementation, first install requirements.txt:
python3 research/analyze_phi.py --legacy
```

[phi_measurements.json](phi_measurements.json) records the seeded run. Checks cover 100,001 encodings against the independent Fibonacci method, 10,001 signed round-trip magnitudes, 500 Fibonacci length thresholds, 4,369 short sequences per experimental codec, and large random sequences. With `--legacy`, the original packing is also round-tripped using exact arithmetic, isolating framing from numerical error. Fixed 100-decimal-digit precision fails on examples near `10**100`; the theorem applies to exact arithmetic.

The PDF cites the primary literature for the even shift and related universal integer codes. The new derivation is supplied in full; no novelty priority claim is made for the encoding.

## Direct digit arithmetic

[phi_arithmetic.py](phi_arithmetic.py) now implements signed increment,
decrement, addition, and multiplication. The adder follows a 19-state carry
relation, with at most five active product states, without whole-value
decoding. The multiplier composes carry additions using scaled Fibonacci
Horner steps. [ARITHMETIC.md](ARITHMETIC.md) supplies the correctness and
finite-bound proofs, a bounded-delay streaming obstruction, API examples,
measurements, and the exact scope of the new Lean invariants.

The direct incrementer beats decode/increment/re-encode on the recorded
samples. The generic adder and multiplier do not beat their conversion-based
baselines on those samples. These arithmetic results do not change the
packing format or the representation's asymptotic expansion.
