# Irradix, negative-phi expansions, and modular arithmetic

Derived September 7, 2026. These results extend the earlier even-gap proof.
They are included in the updated PDF but are not part of the Lean
formalization. This note does not claim novelty priority.

## A more specific piece of prior work

Christiane Frougny and Anna Chiara Lai's **On Negative Bases** (2009),
Examples 2–3 and Figure 2, explicitly identifies the negative-golden-ratio
shift with the even shift. Their paper also proves finite-transducer
normalization results for negative Pisot bases.

- [Author-hosted paper, especially page 9](https://www.irif.fr/~cf/publications/dlt-final.pdf#page=9)
- [Publication record and date](https://iris.uniroma1.it/handle/11573/850258)

Thus the general connection between phi-based numeration and the even shift
predates Irradix's reported 2018 origin. The exact quotient construction
and the explicit correspondence below require their own prior-art check.

## Exact correspondence with a negative-base expansion

Write `phi = (1+sqrt(5))/2`, `a = phi-1`, `c = 2-phi`, and let

```
x(n) = c - frac(phi*n),  n >= 1.
```

These points lie in the standard negative-base interval `[-a, c)`.
Let `E(n)` be the exact Irradix word, and `reverse` reverse its bits.

**Identity.** The greedy base-`-phi` fractional expansion of `x(n)` is

```
. reverse(E(n)) 1 000000...   in base -phi.
```

The extra `1` is essential. This is a positional expansion of `x(n)`,
not of the original integer `n`.

For example, `E(2) = 10`, while

```
x(2) = 5 - 3*phi = (.011)_{-phi}.
```

### Proof, including the terminating boundary case

Recall the phase calculation from the even-gap proof. For a positive
prefix `q`, an admissible bit `d`, and `n = ceil(phi*q)+d`, it gives

```
t(n) = a*(1+d-t(q)),   where t(q)=frac(phi*q).
```

Since `a*(1-c)=c`, subtracting from `c` yields

```
x(n) = -(x(q)+d)/phi.
```

The standard greedy negative-base map is

```
D(x) = floor(-phi*x + a)
T(x) = -phi*x - D(x).
```

For `q>=1`, the previous identity and `0 < x(q)+a < 1` imply

```
D(x(n)) = d
T(x(n)) = x(q).
```

Thus this map removes the least significant Irradix bit, exactly as the
quotient operation does. Iterating reaches `n=1`. At that point,

```
x(1)=3-2*phi  --digit 1-->  -a  --digit 1-->  0  --digit 0-->  0 ...
```

The first of those two ones is the leading bit of `E(n)` read in reverse;
the second is the extra terminal one. This proves the identity. Do not
extend the conjugacy naively to `n=0`: the interval boundary requires the
terminal behavior just described.

## Why the Fibonacci decoder emerges from the same construction

Let `psi=1-phi=-1/phi`, the other root of `z^2-z-1`. If
`E(n)=d_(k-1)...d_0`, the identity reads

```
x(n) = sum(d_j * psi^(j+1), j=0..k-1) + psi^(k+1).
```

But `psi^r = F_(r+1) - F_r*phi`, and independently

```
x(n) = (floor(phi*n)+2) - (n+1)*phi.
```

Equating coefficients of `phi` gives

```
n = F_(k+1) - 1 + sum(d_j*F_(j+1), j=0..k-1).
```

Since the leading digit is one, this is precisely the earlier decoder

```
n = F_(k+2) - 1 + sum(d_j*F_(j+1), j=0..k-2).
```

The graph's adjacency matrix `[[1,1],[1,0]]` has eigenvalues `phi` and
`psi`. Its dominant eigenvalue controls word growth; its other eigenvalue
is exactly the contraction-and-reflection coefficient in the phase proof.
These are two roles of the same quadratic algebra.

## An exact restriction on the binary images

Let `B(n)` be `E(n)` interpreted in ordinary binary, let `r` be its number
of ones, and let `t` be its number of trailing zeros. Then

```
B(n) mod 3 = 0          if r is even;
             (-1)^t    if r is odd.
```

Proof: successive one-bit exponents differ by an odd number because the
intervening zero runs have even length. Their exponent parities therefore
alternate. Modulo 3, `2^j = (-1)^j`, so the contributions cancel in pairs.
With an odd number of ones the remaining contribution is that of the
lowest one, at exponent `t`.

Consequences:

- `3` divides `B(n)` exactly when the word has an even number of ones.
- Every odd `B(n)` is `0` or `1` modulo 3, never `2`.
- **Every prime binary image greater than 3 is `1 mod 6`.**

This is a necessary condition, not a primality test. It is a stronger
arithmetic constraint than the parity bias discussed in the earlier PDF.
It must be included in any revised prime-density baseline.

The same cancellation works when the word is evaluated in any integer
base `b>=2`, using modulus `b+1` instead of 3.

## Concrete questions worth pursuing

1. **Finite-state arithmetic on the existing representation.** Does the
   explicit negative-base correspondence give a small adder or incrementer
   for Irradix? The cited normalization theorems suggest a route; they do
   not supply a finished implementation for this format. In the fractional
   coordinates, addition satisfies

   ```
   x(n+m) = x(n)+x(m)-c + floor(frac(phi*n)+frac(phi*m)).
   ```

   There is only a zero-or-one integer correction, but bit orientation,
   endpoint conventions, normalization, and output length still need work.

2. **Exact residue statistics (resolved for fixed moduli below).** Combine the parity-state graph with a
   residue tracker `r -> 2*r+d mod m`. Analyze the resulting finite matrix
   for moduli 3, 5, 7, etc. This can prove counts and limiting distributions
   for fixed-length codewords and identify systematic arithmetic biases.
   Extending those results to prefixes `n<=N` requires accounting for
   incomplete length blocks. None of this alone proves a prime asymptotic.

3. **Classification beyond phi.** For which bases does repeated floor
   division give a language recognizable by a finite automaton, and when
   does it enumerate a prescribed graph language exactly? Try other Pisot
   bases, but distinguish this quotient algorithm from positional beta
   expansions: a theorem for one does not automatically apply to the other.

## Reproduction

Run `python3 research/check_negative_phi.py`. It checks 10,000 negative-base
expansions using integer pairs representing elements of `Q(phi)` and checks
the modular identity on 100,000 exact encodings. No floating-point arithmetic
is used. These checks supplement the derivations above; they are not Lean
verification.

## Length parity and prime-free intervals

If a word has length `k`, its highest one is at exponent `k-1` and its
lowest at exponent `t`. Alternating exponent parities imply

```
r - 1 = k - 1 - t (mod 2), hence r = k - t (mod 2).
```

So the residue formula depends only on `k` and `t`. An odd binary image
has `t=0`; at even length it is divisible by 3. An even image above 2 is
already composite. Therefore **all images of even length k>=4 are
composite**. Equivalently, every input in

```
[F_(k+2)-1, F_(k+3)-2],  k even and k>=4,
```

maps to a composite number. Examples are `7..11`, `20..32`, `54..87`,
`143..231`, `376..608`, and `986..1595`.

At length `k>=2`, the number of words ending in one is `F_(k-1)`:
these are exactly the paths whose penultimate state is even. Thus the
number of images coprime to 6 is zero for even `k`, and `F_(k-1)` for
odd `k>=3`. The exceptional length-one word represents 1, also coprime
to 6 but not prime. Summing the even-index Fibonacci numbers gives,
for `N_k=F_(k+3)-2`,

```
#{n<=N_k : gcd(B(n),6)=1} = F_k      if k is odd;
                           F_(k-1) if k is even.
```

Dividing by `N_k` gives two different subsequential limits:
`phi^-3 = 0.236067977...` for odd `k`, and
`phi^-4 = 0.145898034...` for even `k`. **The candidate density over
input prefixes has no limit.** This is an exact assertion about
coprimality to 6, not an asymptotic theorem about primes.

## Equidistribution at each fixed modulus coprime to 6

**Theorem.** Fix `m` with `gcd(m,6)=1`. Among all canonical words of length
`k`, every binary residue modulo `m` has proportion tending to `1/m`
as `k` tends to infinity, with exponential convergence for each fixed `m`.

**Proof.** Track the even/odd zero state and the binary residue. The
transitions, with arithmetic modulo `m`, are

```
(E,r) --1--> (E,2r+1)
(E,r) --0--> (O,2r)
(O,r) --0--> (E,2r).
```

For `m=1` the result is immediate. Otherwise let `L` be the multiplicative
order of 4 modulo `m`. An E-to-E block `00` maps `r` to `4r`; a block
`11` maps it to `4r+3`. Use `m*L` such blocks. The initial coefficient
is 1 modulo `m`. At the `m` positions whose remaining block count is
`0,L,...,(m-1)*L`, choose either block; choose `00` elsewhere. Choosing
`11` at `j` of these positions gives `r+3j`. Values `j=0,...,m-1` cover
all residues. Thus all E states communicate. Since 2 is invertible,
the O states are connected to them as well. The loop labeled `1` at
`(E,-1)` makes this strongly connected graph aperiodic.

Its adjacency matrix is consequently primitive. Its positive left and
right eigenvectors can both be chosen constant across residues, with
state weights `(phi,1)`, because the maps `r->2r` and `r->2r+1` are
permutations. Direct multiplication gives eigenvalue `phi`.
Perron--Frobenius convergence, starting at `(E,1)` after the leading bit,
therefore gives equal asymptotic total weight to every residue.
All remaining eigenvalues have strictly smaller modulus, giving the
claimed exponential convergence (with constants depending on `m`).

The same argument gives uniform residues conditional on a final one:
count the previous E states and apply `r->2r+1`. Thus fixed primes
5, 7, 11, etc. have no persistent individual residue bias in these
length blocks. The modulus 3 obstruction above survives through length
parity. The theorem does **not** give estimates uniform in growing `m`;
that missing control matters for sieving and for any prime asymptotic.

## A revised, testable prime heuristic

For `N>=3`, the local restrictions suggest

```
H(N) = 2 + sum(3/log(B(n)), n<=N, B(n)>3, B(n)=1 mod 6).
```

The two exceptions are primes 2 and 3. The factor 3 is the ordinary
prime-density factor for the residue class 1 modulo 6; it was not fitted
to the measurements. Transferring that density to this thin set remains
a heuristic, even after the fixed-modulus theorem.

| Input prefix N | Exact mapped primes | H(N) |
| ---: | ---: | ---: |
| 100 | 12 | 14.32 |
| 1,000 | 94 | 94.46 |
| 10,000 | 466 | 464.53 |
| 100,000 | 4,319 | 4,342.72 |

These nested samples are descriptive, not independent trials. The full
measurement file includes length-block endpoints and their predicted
plateaus, so the near match at 1,000 is not the only reported result.
In particular, 985 through 1,595 all have the same prime count, 94.

Run `python3 research/analyze_residues.py --output research/residue_measurements.json`.
This checks the counting identities through length 100, compares the
residue automaton with direct enumeration through length 13 for eight
moduli, and uses a sieve through 6,692,032 for the first 100,000 inputs.

## What does and does not generalize

Matching a graph's growth eigenvalue is insufficient to reproduce its
language by repeated division. For zero gaps divisible by 3, the graph
has one-step and three-step return paths, so its growth rate `beta`
satisfies `beta^3=beta^2+1`. Its root lies strictly between `4/3` and
`3/2`. Repeated floor division in this base encodes 4 as `101`:
the quotients are `4 -> 2 -> 1 -> 0`, and the corresponding digits are
`1,0,1` from least to most significant. This violates the proposed
multiple-of-three gap condition.

There is a precise limited uniqueness statement: **phi is the only
quadratic Pisot number in (1,2)**. To see this, let `beta` be such a
number and `gamma` its conjugate in `(-1,1)`. The integer trace is 1 or
2. Trace 2 gives an integer norm `beta*(2-beta)` strictly between 0 and
1, impossible. Trace 1 gives integer norm `beta*(1-beta)` strictly
between -2 and 0, hence -1. Therefore `beta^2-beta-1=0`.
This singles out the quadratic contraction mechanism in the binary
range; it does not classify every irrational quotient language.

The most concrete next projects are a finite-state arithmetic prototype
with exact endpoint handling, and quantitative spectral bounds as the
modulus grows. Neither is completed here. Infinitely many prime binary
images and a prime-counting asymptotic are not established by these proofs.
