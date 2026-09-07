# Exact arithmetic on Irradix words

Implemented September 7, 2026. [phi_arithmetic.py](phi_arithmetic.py) adds
signed increment, decrement, addition, and multiplication directly on
canonical digit strings. It also checks unsigned addition relations. No operation decodes
an operand into its whole integer value or builds a Fibonacci table.

```python
from research.phi_arithmetic import add, increment, decrement, multiply, is_sum

assert increment("1001") == "1100"       # 8 + 1 = 9
assert decrement("1000") == "111"        # 7 - 1 = 6
assert add("110", "1001") == "10010"     # 5 + 8 = 13
assert add("-1001", "110") == "-11"      # -8 + 5 = -3
assert add("-1", "1") == "0"
assert multiply("110", "1001") == "1001111"  # 5 * 8 = 40
assert is_sum("110", "1001", "10010")
```

Inputs must be canonical Irradix strings; `-0`, leading zeros, invalid
digits, and odd internal zero gaps are rejected. `is_sum` accepts only
nonnegative words. The original codec API and byte format are unchanged.

## 1. Increment and decrement need only the language

The earlier proof establishes that integer order is shortlex order on
canonical positive words: shorter words come first, then lexicographic
order within a length. This gives a direct successor algorithm.

Scan after the leading one, tracking the parity of zeros since the last
one. Remember the rightmost zero encountered in the even state. Replace
that zero with one and replace all following digits with zeros. If there
is no such position, the word is all ones; return a leading one followed
by `k` zeros, where `k` was the input length. Handle `0 -> 1` separately.

**Proof.** A zero can be changed to one precisely in the even state.
Changing the rightmost such zero gives the next larger lexicographic
branch, and an all-zero suffix is its least accepted continuation.
If none exists, every digit after the leading one must be one: the first
zero, if present, would be in an even state. Thus the input is the largest
word of its length and its successor is the least word of the next length.
Completeness and order preservation of the encoding identify this word
with `E(n+1)`.

The predecessor changes the rightmost nonleading one to zero, then fills
with the largest legal suffix: a forced zero, if space remains, followed
by ones. If the input is `1` followed by zeros, move to all ones of the
previous length. Handle `1 -> 0` separately. The symmetric lexicographic
argument proves correctness. Signed increment and decrement reverse these
magnitude operations as appropriate, with explicit handling of zero.

Both algorithms do `O(k)` digit work. The Python implementation stores a
pivot index and creates the output string. This is a full-word algorithm,
not a claim that a one-way streaming transducer can emit the result.

## 2. Augmenting the word exposes the arithmetic

For `w=E(n)`, prefix one extra `1` and call the resulting word `U(n)=1w`.
With least significant position numbered zero, let

```
W(d_k ... d_0) = sum(d_j F_(j+1)).
```

The Fibonacci decoder gives **`W(U(n)) = n+1`**. This also holds at zero:
`U(0)=10` has weight `F_2=1`. Extra leading zeros do not change the weight.

Consequently, after right-aligning three augmented words,

```
a + b = c  iff  W(U(a) + U(b) - U(c)) = 1,
```

where the signs on words mean digitwise addition/subtraction, without
ordinary binary carries. Each column difference belongs to `{-1,0,1,2}`.
The terminal target is **1, not 0**; the augmentation offset matters.

This is the practical payoff of the negative-phi correspondence. That
identity supplies exactly these Fibonacci weights, including the extra
terminal digit. We can work in the conjugate quadratic algebra rather
than normalizing floating-point fractional coordinates.

## 3. A bounded carry automaton

Represent a partial polynomial value as `C=u+v*phi`, with integer `u,v`.
Reading a difference digit `e` from most to least significant performs

```
C <- phi*C + e
(u,v) <- (v+e, u+v).
```

Start at `(0,0)`. Since `phi^j=F_(j-1)+F_j*phi` for `j>=1`, the sum of
the two coefficients of a completed polynomial is its weight `W`;
the constant term has weight `F_1=1` as well. Therefore the exact
acceptance condition is **`u+v=1`**.

The [Lean companion](lean/PhiArithmetic.lean) proves this invariant for
arbitrary integer digit lists, and proves acceptance equivalent to
`a+b=c` under the three augmented-weight hypotheses. Its recorded build
is [arithmetic-verification.txt](lean/arithmetic-verification.txt).

### Why finitely many carries suffice

Let `psi=1-phi=-1/phi` and `C'=u+v*psi`. Every prefix, whether valid or not,
satisfies

```
|C'| <= 2 sum_(j>=0) |psi|^j = 2/(1-1/phi) < 6.
```

For an accepted full word, `u+v=1`, so `C'=1-phi*v`. The preceding bound
forces integer `v` into `{-3,...,4}`, giving `|C|=|1+v/phi|<4` at the end.
If a prefix has `r` digits remaining, writing out the suffix recurrence
gives

```
|C_prefix| <= 4*phi^(-r) + 2*(1-phi^(-r))/(phi-1) <= 4.
```

The inequality is strict for actual finite words. Thus every prefix of
an accepted word has `|C|<4` and `|C'|<6`. Since

```
v = (C-C')/sqrt(5),
u = (phi*C' - psi*C)/sqrt(5),
```

we have `|v|<5` and `|u|<6`. **All necessary carries are inside the fixed
99-state rectangle `-5<=u<=5`, `-4<=v<=4`.** No input-length bound was used.

Generate all transitions in that rectangle. Of its 99 states, 67 are
reachable from `(0,0)`; trimming those with no path to a terminal state
leaves **19 carry states**, with four terminals:

```
(-1,2), (0,1), (1,0), (2,-1).
```

Trimming preserves every accepting path. These are not 19 states per
input digit: the same machine handles every length. We do not claim that
19 is a minimal possible carry presentation.

## 4. Turning the relation into an adder

Given input bits `a_i,b_i`, try output bit `c_i` in `{0,1}` and follow the
carry transition for `e_i=a_i+b_i-c_i`. Simultaneously validate the padded
augmented output language

```
0*(10 | 11(1|00)*(epsilon|0)).
```

Its five states distinguish padding, the initial augmentation one, the
special zero word, and the even/odd positive-word states. The product has
at most `19*5=95` states. This is a nondeterministic finite transducer whose
successful output is unique; an addition recognizer alone would not
suffice to construct that output.

The implementation actually constructs it: retain reachable product
states at each column, remembering one predecessor and output bit per
state. At the end select an accepting state and trace the path backward.
Merging two paths at the same state is safe because all future constraints
depend only on that state and the remaining input. Each retained path
already has a valid language prefix and the same carry.

**Soundness.** Every completed accepting path has a canonical augmented
output and satisfies the carry equation, so its decoded value is `a+b`.

**Completeness.** The canonical word for `a+b` exists. If the longer input
has `k` digits, its sum has at most `k+2` digits: for positive operands,
`a+b <= 2(F_(k+3)-2) < F_(k+5)-1`, the minimum value at length `k+3`.
Zero causes no difficulty. We allow `k+3` columns, including augmentation.
The correct output therefore fits, and its entire carry path lies in the
proved rectangle and survives trimming. Uniqueness follows from the
bijection between integers and canonical words.

**Subtraction and signs.** To find `c=a-b>=0`, use column differences
`b_i+c_i-a_i` in the same carry machine. This checks `c+b=a` and again has
terminal target 1. Signed addition compares magnitudes by shortlex order,
then selects addition or subtraction and applies the appropriate sign.

**Complexity.** With a fixed 95-state bound and at most two output choices
per state, time and stored path history are `O(k)`; carry arithmetic uses
only bounded small integers. Exhaustive closure of the reachable subset
graph sharpens the implementation bound: addition has 41 reachable
frontier subsets, subtraction has 39, and **at most five active product
states** occur in either case, even over arbitrary input bit pairs. This
finite enumeration is checked by `frontier_bound` in the test script; it
is not a Lean theorem. The test covers the whole subset graph, not merely
sampled operands.

`is_sum` checks supplied unsigned operands and result by one deterministic
carry pass after validation, without keeping path history. Its Python
wrapper materializes padded strings; a caller supplying aligned columns
could run the recognizer with only the fixed carry state.

## 5. Multiplication by Fibonacci Horner steps

`multiply(left, right)` implements signed multiplication using the carry
adder. It is the Fibonacci-weight analogue of shift-and-add, rather than
ordinary binary Russian-peasant multiplication. Choose the shorter word
as the multiplier; let `a` be the other nonnegative operand.

For the augmented multiplier `U(b)`, scan digits from most significant
first, maintaining Irradix representations of two values `x,y`:

```
start: x=0, y=0
for each digit d in U(b):
    (x,y) = (x+y+d*a, x)
return x-a
```

The implementation starts just after the augmentation bit, at `(a,0)`.
It uses the existing carry adder for both additions and the same machine
in subtraction mode for the final offset. Zero, one, and signs are
handled explicitly. No loop count is the numerical value of an operand;
there is one iteration per multiplier digit.

**Proof.** If a processed prefix has digits `d_j` numbered from the right,
maintain

```
x = a * sum(d_j F_(j+1)),
y = a * sum(d_j F_j).
```

Appending a digit shifts the existing weights up one index.
`F_(j+2)=F_(j+1)+F_j` therefore gives the update `x+y+d*a`, and the new
second value is the old `x`. After the entire augmented word,
`x=a*W(U(b))=a*(b+1)`. Subtracting `a` gives exactly `a*b`.
The [Lean file](lean/PhiArithmetic.lean) verifies the scaled Horner
invariant and final offset equation; it does not verify the Python
composition of carry-machine calls.

If operand lengths are `k` and `l`, there are `min(k,l)` iterations.
Intermediate words have `O(k+l)` digits, giving **`O(min(k,l)*(k+l))`
digit work and `O(k+l)` working space** with the current linear-time
adder. For equally sized inputs this is quadratic. The multiplier as a
whole is not claimed to be a finite-state transducer; it composes the
finite-state addition relation over growing intermediate words.

Run `python3 research/check_multiplication.py`, optionally with
`--output research/multiplication_measurements.json`. The checks include
16,384 unsigned and 4,225 signed products, 100 random signed pairs up to
256 bits, 20 distributivity checks, 64 Fibonacci boundaries, and malformed
inputs. Long cases include two 1,000-digit operands and a 20,000-digit
operand multiplied by 6, checked by an independent Fibonacci-weight
oracle. [Recorded multiplication measurements](multiplication_measurements.json)
include comparisons with decode/multiply/re-encode. Native integer
multiplication followed by re-encoding is substantially faster on those
samples; this implementation establishes direct digit arithmetic.

## 6. Why bounded-delay streaming fails in both directions

Here bounded delay means a deterministic one-way algorithm must emit
successive result digits after at most a fixed amount of lookahead,
independent of word length. Both compared inputs may have known equal
length. The result is emitted in the same direction as the input is read.

**Most significant first.** Compare `1^k` with `1^(k-1)0`. They share
`k-1` initial digits, but their increments are `10^k` and `1^k`.
The second output digit is different, requiring arbitrarily long
lookahead. With a common padded output width, even the first digit differs.

**Least significant first.** Compare `10^(k-1)` with `110^(k-2)` for
`k>=3`. Their reversals share `k-2` initial zeros. A word ending in `t>0`
zeros increments to a word ending in one exactly when `t` is odd.
The two inputs have opposite trailing-zero parity, so their first emitted
result digits differ, again after an arbitrarily long shared input prefix.

Thus even incrementing is impossible in this bounded-delay model; a
general adder would inherit the obstruction by fixing one operand to 1.
This does not exclude two-way or multipass machines, redundant output
representations, or the offline finite-state path construction above.
It also does not contradict online results for other Fibonacci normal
forms: the canonical Irradix language is a different representation.

## 7. Evidence and practical limits

Run from the repository root:

```sh
python3 research/check_arithmetic.py
# To record a new run, including local timings:
python3 research/check_arithmetic.py --output research/arithmetic_measurements.json
```

Checks cover 100,001 successor/predecessor pairs, all 65,536 unsigned
operand pairs in `0..255`, all 16,641 signed pairs in `-64..64`, 8,192
exhaustive relation triples, 1,000 random signed pairs up to 4,096 bits,
300 Fibonacci boundaries checked with the independent square-root encoder,
and malformed inputs. A 100,000-digit addition is checked against an
independent unbounded Fibonacci-weight oracle. See the
[recorded measurements](arithmetic_measurements.json).

The prototype demonstrates linear digit arithmetic and finite carries.
It is not a throughput claim against native binary arithmetic. The recorded
local run took about 0.34 seconds for one 100,000-digit sum; at 64--4,096
input bits, decoding, adding with Python integers, and re-encoding remained
faster than the generic carry-path solver. Benchmark results depend on
implementation, machine, and workload.

Formal scope is deliberately narrower than the full implementation:
Lean checks the algebraic carry invariant, conditional acceptance
criterion, and the multiplier’s scaled Horner invariant. The finite bound, canonical-language arguments, successor
proof, and streaming obstruction have written proofs here. Python graph
construction and output recovery are tested, not formally verified.

## 8. Cryptographic interpretation

For signed words, transporting addition gives a group isomorphic to the
ordinary integers: `E(a) (+) E(b)=E(a+b)`. It supplies no hard discrete-log
problem. Repeating a public generator `E(g)` a secret number `s` of times
produces `E(s*g)`; decoding and dividing by `g!=0` recovers `s`. Modulo a
public modulus, the analogous problem is an elementary linear congruence.
Encoding elliptic-curve coordinates with Irradix would preserve the
underlying curve's security assumptions, not add a new one.

Changing representations also does not evade
[Shor's quantum discrete-log algorithm](https://arxiv.org/abs/quant-ph/9508027).
A new noisy, high-dimensional construction over a quadratic ring would
require separate hardness assumptions and cryptanalysis; nothing proved
here provides them. NIST's [ML-KEM](https://csrc.nist.gov/pubs/fips/203/final)
and [SLH-DSA](https://csrc.nist.gov/pubs/fips/205/final) illustrate different
post-quantum foundations, not consequences of this adder.

## Related arithmetic literature

- Christiane Frougny, *On-line finite automata for addition in some
  numeration systems*, RAIRO--Theoretical Informatics and Applications
  33(1), 79--101 (1999).
  [Paper](https://www.numdam.org/item/ITA_1999__33_1_79_0.pdf).
  Treats online arithmetic in golden-ratio and Fibonacci representations.
- Connor Ahlbach, Jeremy Usatine, Christiane Frougny, and Nicholas Pippenger,
  *Efficient Algorithms for Zeckendorf Arithmetic*, Fibonacci Quarterly
  51(3), 249--255 (2013).
  [Paper](https://www.fq.math.ca/Papers1/51-3/AhlbachUsatineFrougnyPippenger.pdf).
  Gives linear-time, three-pass addition for the Zeckendorf normal form.
- Christiane Frougny and Anna Chiara Lai, *On Negative Bases* (2009).
  [Paper](https://www.irif.fr/~cf/publications/dlt-final.pdf).
  The negative-Pisot normalization background for the connection used here.

These establish substantial prior art for finite-state Fibonacci
arithmetic. This note supplies a concrete construction and implementation
for this repository's augmented even-shift representation, without a
novelty-priority claim.

## Balanced conversion and quadratic-ring follow-up

[FAST_ARITHMETIC.md](FAST_ARITHMETIC.md) derives a balanced encoder/decoder,
a separate conversion-based multiplier, and the Pell/Lucas factoring connection.
The direct digit multiplier described above remains useful as an arithmetic
construction; the new hybrid is substantially faster for large words. It uses
native whole integers and does not improve the underlying multiplication core.
