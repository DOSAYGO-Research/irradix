# Lean companion to the Irradix proof

[PhiPacking.lean](PhiPacking.lean) formalizes the **exact integer quotient/ceiling algorithm**, using mathlib's real golden ratio. Bits are `Bool`s in most-significant-first order (`true = 1`).

The project pins Lean `v4.34.0-rc2` and mathlib commit `0383a80e644c8b14e66fd137516001534006077f` in the adjacent configuration files.

**Verified September 7, 2026:** the source compiled successfully with the pinned toolchain and mathlib revision, with no errors or warnings. All six printed theorem dependency lists contain only `propext`, `Classical.choice`, and `Quot.sound`; none contains `sorryAx`. See [verification.txt](verification.txt) for the recorded command and output.

With [elan](https://github.com/leanprover/elan) installed:

```sh
cd research/lean
lake update
lake exe cache get Mathlib.NumberTheory.Real.GoldenRatio Mathlib.Algebra.Order.Floor.Ring Mathlib.Tactic.Linarith Mathlib.Tactic.Ring
lake build
```

## What the statements mean

- `A q` is `ceil(phi*q)`; `next q b` is `A q + b`.
- `Admissible q b` is the upper quotient bound for that step. The lower bound follows from the ceiling operation.
- `quotient_step` proves that an admissible step's actual floor quotient is `q`, and that flooring its remainder gives exactly the selected bit. Thus `Admissible` is tied to the arithmetic algorithm, rather than assuming a bit-pattern restriction.
- `Trace q bs` asserts admissibility of all steps when reading `bs` from prefix value `q`.
- `Encoded n w` starts with the leading `1`, follows such a trace, and finishes with decoded value `n`. Zero is handled separately as the public string `0`; it trivially has no odd gap.
- `exists_encoded` proves that every positive natural number has an encoding. Its proof follows decreasing floor quotients and derives the binary digit at each step.
- `zero_reflects` proves the central identity `phase(next q false)-c = -a*(phase(q)-c)`, with `a=phi-1` and `c=2-phi`.
- `trace_iff_accept` proves both directions of the equivalence with the two-state even-gap automaton, given the corresponding phase state.
- `language_iff` proves that every suffix accepted by that automaton occurs after the leading `1`, and every encoded suffix is accepted.
- `no_odd_gap` excludes `1 0^(2*k+1) 1` at every position in every encoded word.
- `no_101` is the `k=0` corollary.

The closing `#print axioms` commands expose the logical dependencies of the principal results. There are no `sorry`, `admit`, or user-declared axioms in the source.

## Scope

This formalizes the exact mathematical algorithm and its bit language. It does not formally verify Python/C++ floating-point execution, the integer-square-root or Fibonacci implementations, byte packing, delimiter repairs, timing measurements, the Fibonacci counting formula, or the prime-density discussion. Those are distinguished in the [readable PDF](../../output/pdf/phi-proof.pdf) and independently exercised where applicable by [analyze_phi.py](../analyze_phi.py).

For an existing checkout of the pinned mathlib revision with its cache installed, the source can also be checked directly from that checkout:

```sh
lake env lean /absolute/path/to/irradix/research/lean/PhiPacking.lean
```
