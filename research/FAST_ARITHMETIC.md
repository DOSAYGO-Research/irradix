# Balanced conversion, multiplication, and the Pell-conic connection

This exploration produces an exact balanced encoder/decoder and a faster
conversion-based multiplier for long Irradix words. It also identifies a genuine
Pell-conic group in the two-coordinate algebra. Factoring through that group
recovers a discriminant-5 Lucas/Williams method; it does not improve on the
classical scalar Lucas implementation tested here.

Code: [phi_fast.py](phi_fast.py), [phi_factor.py](phi_factor.py).
Checks and measurements: [check_fast.py](check_fast.py),
[fast_measurements.json](fast_measurements.json).
The main [paper](../output/pdf/phi-proof.pdf) includes these results.

## 1. Two coordinates make block decoding possible

Write F₀=0, F₁=1 and φ²=φ+1. For any binary block w=dₖ₋₁…d₀,
including blocks that are not canonical, define

$$X(w)=\sum_j d_j F_{j+1},\qquad Y(w)=\sum_j d_j F_j.$$

Appending digit d sends (X,Y) to (X+Y+d,X). If w=hℓ, where ℓ has
r digits, then the Fibonacci addition identities give

$$\begin{aligned}
X(h\ell)&=F_{r+1}X(h)+F_rY(h)+X(\ell),\\
Y(h\ell)&=F_rX(h)+F_{r-1}Y(h)+Y(\ell)\quad(r\ge1).
\end{aligned}$$

Equivalently, raise the matrix [[1,1],[1,0]] to r and apply it to the
high block, then add the low block. This proves the concatenation rule
without assuming anything about the digits' language.

The augmented canonical word U(n)=1E(n) has X(U(n))=n+1, also for
public E(0)=0. Consequently decoding is X(1w)−1. A balanced recursion
with 64-digit Horner leaves computes both coordinates, reusing Fibonacci
pairs obtained by fast doubling. Fast doubling is established arithmetic;
see the [GMP Fibonacci algorithm](https://gmplib.org/manual/Fibonacci-Numbers-Algorithm).

## 2. A balanced encoder with at most two prefix corrections

The decoder alone is insufficient: multiplication must also return an Irradix
word. Ordinary Fibonacci unranking processes one digit at a time and stores
an entire table of growing Fibonacci integers. The following construction
splits unranking into two roughly equal subproblems.

Let T(n)=⌊n/φ⌋. If E(n) has length k and r=⌊k/2⌋, its prefix after
removing r digits represents q=Tʳ(n). Write T(x)=x/φ−ε(x), where
0≤ε(x)<1. Iteration yields

$$0\le n/\varphi^r-q
 =\sum_{i=0}^{r-1}\frac{\varepsilon(T^i(n))}{\varphi^{r-1-i}}
 <\frac1{1-\varphi^{-1}}=\varphi^2<3.$$

Thus, with q₀=⌊n/φʳ⌋,

$$q\in\{q_0,q_0-1,q_0-2\}.$$

This bound is independent of the word length. No approximation to φ is
needed. Put f=Fᵣ, g=Fᵣ₊₁, and t=⌊φnf⌋. Since
φ⁻ʳ=(−1)ʳ(g−fφ) and nf>0,

$$q_0=\begin{cases}t-ng&r\text{ odd},\\ng-t-1&r\text{ even}.
\end{cases}$$

For any nonnegative integer s,
⌊φs⌋=(s+isqrt(5s²))//2, using exact integer square root.

### Finding the correct prefix

For q≥1, let Zᵣ(q) be the integer represented by E(q) followed by r
zeros. Its exact boundary is

$$Z_r(q)=F_r(\lfloor\varphi q\rfloor+2)+F_{r-1}(q+1)-1. \tag{1}$$

To prove (1), use the previously established phase coordinate
x(q)=(⌊φq⌋+2)−(q+1)φ. Appending a zero multiplies x by
ψ=1−φ, so x(Zᵣ(q))=ψʳx(q). Substitute
ψʳ=Fᵣ₊₁−Fᵣφ and compare coefficients of φ. Linear independence
of 1 and φ over the rationals gives (1).

All words of fixed length are in integer lexicographic order. The descendants
of a fixed prefix therefore form a consecutive interval whose first element
is Zᵣ(q). Equivalently, iterating the monotone quotient T groups integers
into consecutive fibers, and choosing the zero digit at every inverse step
selects the smallest element. Hence Zᵣ is strictly increasing, and the desired
q is the greatest prefix with Zᵣ(q)≤n. Start at q₀ and decrement while
Zᵣ(q)>n. The preceding bound proves termination after at most two corrections.
The implementation observes cases requiring both corrections.

### Encoding the suffix by its rank

Recursively encode q as a prefix of length k−r, and set j=n−Zᵣ(q).
The prefix's trailing-zero parity determines which suffixes are allowed.

* **Even parity:** the r-digit suffix language is exactly the language following
  a leading 1. Encode Fᵣ₊₃−1+j as an ordinary word of length r+1 and
  remove its first digit.
* **Odd parity:** the next digit must be 0; this returns the automaton to the
  even state. Encode Fᵣ₊₂−1+j as a word of length r, remove its first
  digit, and prepend the forced 0.

These statements follow from the two-state language and the length-k
starting value Fₖ₊₂−1. The interval property guarantees that j is in the
appropriate range. Induction on k proves the full encoder: the prefix is
correct, the suffix has precisely its required rank, and both recursive
lengths are smaller for k>2. The implementation uses the established
Fibonacci encoder for k≤64. Zero and signs are handled separately.

### Costs and limits

The block arithmetic uses integers with O(k) bits, since Irradix length and
binary bit length differ by a constant factor. If M(k) and S(k) denote the
backend costs of multiplication and integer square root, the recursive
encoding work has the form

$$C(k)\le C(\lceil k/2\rceil)+C(\lfloor k/2\rfloor+1)
       +O(M(k)+S(k)+k),$$

with a constant number of prefix corrections. Fibonacci preparation and the
initial length search also use fast doubling; the implementation caches
pairs within each operation. Under usual regularity assumptions, a
conservative bound including that preparation is
O((M(k)+S(k)+k) log k). This is a backend-dependent cost statement, not
a proof that this Python encoder has Karatsuba's exponent. In particular,
integer square root is not a unit-cost operation.

The algorithm avoids the original encoder's Θ(k²) bits of stored Fibonacci
values. It still creates Python strings and cached big integers; measured
allocation is reported below rather than claiming constant space.

## 3. What improves multiplication, and what does not

`multiply_hybrid(a,b)` performs balanced decoding, Python integer
multiplication, and balanced encoding. It deliberately converts whole
values. The separate `phi_arithmetic.multiply` remains the direct digit
Horner algorithm backed by the carry adder.

```python
from research.phi_fast import encode_balanced, decode_balanced, multiply_hybrid

assert decode_balanced(multiply_hybrid(encode_balanced(-123),
                                      encode_balanced(456))) == -56088
```

Recorded on Python 3.14.4, macOS arm64. Multiplication timings are best of
three on seeded canonical words, with fresh per-operation Fibonacci caches.
All columns use the same operands; “native only” excludes conversion.
The previous route is rolling `weighted_decode` followed by native multiplication
and `fibonacci_irradix`, as recorded in the benchmark source.

| Digits per input | Balanced hybrid | Previous conversion pipeline | Native product only |
| ---: | ---: | ---: | ---: |
| 128 | 0.135 ms | 0.0859 ms | 0.000291 ms |
| 1,024 | 1.18 ms | 0.956 ms | 0.00154 ms |
| 8,192 | 34.9 ms | 45.4 ms | 0.0610 ms |
| 16,384 | 46.9 ms | 111 ms | 0.194 ms |

The gain at 16,384 digits is 2.37× against the previous conversion route.
Short words favor the simpler converter. At 1,024 digits the direct digit
Horner implementation took 3.31 seconds. A separate 100,000-by-100,000-digit
hybrid product produced 200,001 digits in 1.40 seconds and was checked with
an independent rolling Fibonacci-weight decoder.

For encoding a **16,384-digit output**, `tracemalloc` measured 143,193 bytes
of peak Python allocation for balanced encoding versus 13,204,993 bytes
for the previous encoder: about 92× less. This is not whole-process RSS.
The timing table instead has 16,384-digit *inputs*, whose product has
32,768 digits. Component timings in the JSON are separate measurements;
they should not be added to reconstruct a hybrid timing.

### Why quadratic-ring multiplication is not an integer shortcut

For a ring coordinate C=u+vφ define W(C)=u+v. The polynomial sum
Σdⱼφʲ has W equal to its Fibonacci weight. Ring multiplication is

$$(u,v)(a,b)=(ua+vb,\;ub+va+vb).$$

Three scalar products suffice: P=ua, Q=vb, R=(u+v)(a+b), returning
(P+Q,R−P). This resembles the familiar three-product principle in
[Karatsuba multiplication](https://gmplib.org/manual/Karatsuba-Multiplication).
But

$$W(CD)=W(C)W(D)+vb.$$

For example W(φ)=1 while W(φ²)=2. The weight map is not multiplicative,
and augmented words introduce a further +1 offset. Multiplying positional
polynomials and then decoding therefore does not compute the desired
integer product. The correction is itself a large integer product, so
this identity supplies no reduction below the ordinary multiplication core.
It is an obstruction to that proposed shortcut, not an impossibility theorem
for every future Irradix multiplication algorithm.

## 4. A real point group: the Pell conic

Conjugation sends φ to 1−φ, giving the multiplicative norm

$$N(u,v)=u^2+uv-v^2.$$

The norm-one pairs form a group. Their inverse is (u+v,−v).
Changing coordinates to x=2u+v and y=v gives

$$x^2-5y^2=4.$$

Thus the group is the discriminant-5 Pell conic, with identity (2,0).
For odd moduli, its point operation is

$$(x,y)\star(z,t)=\left(\frac{xz+5yt}{2},\frac{xt+yz}{2}\right).$$

Over integers these quotients are integral for the points arising from the
ring. The natural unit α=φ²=1+φ corresponds to (3,1), and its m-th
power corresponds to (L₂ₘ,F₂ₘ), where L denotes Lucas numbers.
This does realize the earlier idea of operations on points, but it is a
classical conic, not an elliptic curve. Lemmermeyer's
[2003 paper](https://arxiv.org/abs/math/0311306) develops the connection;
Šleževičienė's [2004 paper](https://doi.org/10.15388/LMR.2004.31881)
already treats factoring with Pell conics.

### Why a factor's p−1 or p+1 enters

Let p be prime, p≠2,5, and χ=(5|p). In
Rₚ=Fₚ[t]/(t²−t−1):

* If χ=1, the polynomial splits into distinct roots. Then Rₚ is
  Fₚ×Fₚ; norm is the product, and norm-one pairs (a,a⁻¹) form a
  group of order p−1.
* If χ=−1, Rₚ is Fₚ². Conjugation is Frobenius, so norm is
  z↦zᵖ⁺¹. The cyclic multiplicative group has order p²−1, and its
  norm-one kernel has order p+1.

Therefore the order of α modulo p divides p−χ. This is the standard
finite-field structure of the Pell conic, applied here to the φ unit.

Let M=lcm(1,…,B). If the unit order modulo an unknown factor p divides M,
then αᴹ=(1,0) modulo p. Writing αᴹ=(u,v) modulo the input N,

$$g=\gcd(N,u-1,v)$$

is divisible by p. It is useful only if 1<g<N. The implementation builds
M via maximal prime powers ≤B and checks gcd after each step. A proper
factor can appear before the final exponent; saturation at N fails for this
attempt. Merely having small prime divisors is insufficient: their required
powers must also divide M. Returning `None` does not assert primality.

### Reduction to scalar Lucas factoring

The trace of αᵐ is Vₘ(3,1), with V₀=2, V₁=3 and
Vₘ₊₁=3Vₘ−Vₘ₋₁. For a norm-one element z in either finite-field
case above,

$$\operatorname{Tr}(z)-2=z+z^{-1}-2=(z-1)^2/z.$$

The algebra is reduced, so this vanishes precisely when z=1. Hence for
squarefree N coprime to 10 the same factor primes are detected by
`gcd(N,V_M(3,1)−2)`. Prime powers need separate care: the square can
change valuations, so the two gcds need not coincide on arbitrary N.

Our scalar implementation uses V₂ₘ=Vₘ²−2 and
V₂ₘ₊₁=VₘVₘ₊₁−P for general parameter P. Composing Lucas operations
builds the same exponent schedule. This is the discriminant-5 specialization
of established Lucas/Williams factoring, with its p+1 behavior when 5 is a
nonresidue. See Williams, [*A p+1 Method of Factoring* (1982)](https://doi.org/10.1090/S0025-5718-1982-0658227-7),
and the [GMP-ECM implementation documentation](https://github.com/sethtroisi/gmp-ecm/blob/main/README).

## 5. Factoring experiments and practical conclusion

```python
from research.phi_factor import phi_factor_stage1, pollard_pm1_stage1

assert phi_factor_stage1(107*1019, 27) == 107
assert pollard_pm1_stage1(107*1019, 27) is None
assert phi_factor_stage1(113*1019, 16) is None
assert pollard_pm1_stage1(113*1019, 16) == 113
```

Here 107+1=108 fits the first bound's prime powers whereas 107−1 has
factor 53; 113−1=112 fits the second bound whereas 113+1 has factor 19.
The exact checks establish the claimed outcomes for the other cofactor too.
These examples show complementary behavior to fixed-base p−1, not dominance.

On 200 seeded semiprimes, each made from two distinct primes in [1000,9999]:

| Bound B | φ pairs / scalar Lucas successes | Base-2 p−1 successes | Either succeeds |
| ---: | ---: | ---: | ---: |
| 16 | 16 / 16 | 14 | 22 |
| 64 | 105 / 105 | 102 | 129 |
| 256 | 172 / 172 | 171 | 191 |

At B=256 the pair implementation took 31.6 ms for the sample; scalar Lucas
took 10.0 ms and p−1 took 4.43 ms. The classical scalar method detects
the same factors faster. These are toy stage-one experiments, not a comparison
with full factoring packages, ECM, or algorithms on cryptographic-size inputs.
There are no stage-two steps, seed searches, or complete factoring driver.

The useful engineering result is balanced conversion when Irradix words
must be retained. For arithmetic-heavy applications, binary integers and an
established big-integer backend remain the sensible core. For factoring,
the φ route reveals an existing method rather than a new speedup.
The point group embeds into a finite field multiplicative group, so it also
offers no new post-quantum hardness assumption.

## Verification scope and reproduction

```sh
python3 research/check_fast.py --output research/fast_measurements.json
```

The recorded run forces recursive encoding with two-digit leaves on 20,001
inputs; checks 2,001 signed and 300 large random round trips; tests 500
Fibonacci thresholds; verifies 4,225 small signed and 100 large random
products; checks 1,000 ring identities and the order bound at 166 primes;
and independently validates the large product and returned proper factors.

[PhiArithmetic.lean](lean/PhiArithmetic.lean) additionally proves the high-block
weight formula, the three-product ring identity, norm multiplicativity, the
weight-product correction, and the Pell-coordinate identity. These are compiled
algebraic theorems. The balanced encoder's two-correction bound and correctness,
finite-field group structure, and factoring analysis have written proofs here;
they are not included in the Lean formalization. The Python programs themselves
are not formally verified. See the [compiler record](lean/arithmetic-verification.txt).
