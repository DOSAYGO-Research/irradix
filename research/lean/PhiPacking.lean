import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Algebra.Order.Floor.Ring
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
# The exact quotient-based phi encoding and the even shift

Bits are read most significant first. `Trace q w` means that, starting
at integer q, each ceiling step has q as its actual phi quotient.
`Encoded n w` starts with 1 and follows such a trace to n.
No floating-point implementation is assumed or verified.
-/

namespace PhiPacking

set_option autoImplicit false

noncomputable section

def phi : ℝ := Real.goldenRatio
def a : ℝ := phi - 1
def c : ℝ := 2 - phi
def A (q : ℤ) : ℤ := ⌈phi * (q : ℝ)⌉
def phase (q : ℤ) : ℝ := Int.fract (phi * (q : ℝ))
def bit (b : Bool) : ℤ := if b then 1 else 0
def next (q : ℤ) (b : Bool) : ℤ := A q + bit b
def Admissible (q : ℤ) (b : Bool) : Prop :=
  (next q b : ℝ) < phi * ((q : ℝ) + 1)

lemma phi_gt_one : 1 < phi := Real.one_lt_goldenRatio
lemma phi_lt_two : phi < 2 := Real.goldenRatio_lt_two
lemma phi_pos : 0 < phi := Real.goldenRatio_pos
lemma phi_sq : phi ^ 2 = phi + 1 := Real.goldenRatio_sq
lemma a_pos : 0 < a := by dsimp [a]; linarith [phi_gt_one]
lemma a_lt_one : a < 1 := by dsimp [a]; linarith [phi_lt_two]
lemma a_gt_c : c < a := by
  dsimp [a, c]
  nlinarith [phi_sq, phi_gt_one]
lemma fixed_point : a * (1 - c) = c := by
  dsimp [a, c]
  nlinarith [phi_sq]

lemma phase_pos {q : ℤ} (hq : 0 < q) : 0 < phase q := by
  apply Int.fract_pos.mpr
  exact (Real.goldenRatio_irrational.mul_intCast (ne_of_gt hq)).ne_int _

lemma phase_lt_one (q : ℤ) : phase q < 1 := Int.fract_lt_one _

lemma A_eq {q : ℤ} (hq : 0 < q) : A q = ⌊phi * (q : ℝ)⌋ + 1 := by
  apply Int.ceil_eq_iff.mpr
  push_cast
  have ht := phase_pos hq
  have hu := phase_lt_one q
  simp only [phase, Int.fract] at ht hu
  constructor <;> linarith

lemma A_cast {q : ℤ} (hq : 0 < q) :
    (A q : ℝ) = phi * (q : ℝ) + 1 - phase q := by
  rw [A_eq hq]
  push_cast
  simp only [phase, Int.fract]
  ring

lemma zero_admissible (q : ℤ) : Admissible q false := by
  have h := Int.ceil_lt_add_one (phi * (q : ℝ))
  dsimp [Admissible, next, bit, A]
  norm_num
  nlinarith [phi_gt_one]

lemma one_admissible_iff {q : ℤ} (hq : 0 < q) :
    Admissible q true ↔ c < phase q := by
  dsimp [Admissible, next, bit]
  norm_num
  rw [A_cast hq]
  dsimp [c]
  constructor <;> intro h <;> linarith

lemma next_pos {q : ℤ} (hq : 0 < q) (b : Bool) : 0 < next q b := by
  have hc := Int.le_ceil (phi * (q : ℝ))
  have hq' : (0 : ℝ) < q := by exact_mod_cast hq
  have hp := mul_pos phi_pos hq'
  have hn : (0 : ℝ) < (A q : ℝ) := lt_of_lt_of_le hp hc
  have hn' : 0 < A q := by exact_mod_cast hn
  cases b <;> simp [next, bit] <;> omega

/-- This connects a ceiling step to the exact quotient and remainder. -/
theorem quotient_step {q : ℤ} (b : Bool) (h : Admissible q b) :
    ⌊(next q b : ℝ) / phi⌋ = q ∧
    ⌊(next q b : ℝ) - phi * (q : ℝ)⌋ = bit b := by
  have hlo := Int.le_ceil (phi * (q : ℝ))
  have hhi := Int.ceil_lt_add_one (phi * (q : ℝ))
  have hb : (0 : ℝ) ≤ (bit b : ℝ) := by cases b <;> norm_num [bit]
  have hn : (next q b : ℝ) = (A q : ℝ) + (bit b : ℝ) := by simp [next]
  change (A q : ℝ) < phi * (q : ℝ) + 1 at hhi
  change phi * (q : ℝ) ≤ (A q : ℝ) at hlo
  constructor
  · apply Int.floor_eq_iff.mpr
    constructor
    · apply (le_div_iff₀ phi_pos).mpr
      nlinarith
    · apply (div_lt_iff₀ phi_pos).mpr
      dsimp [Admissible] at h
      nlinarith
  · apply Int.floor_eq_iff.mpr
    constructor <;> linarith

lemma phase_zero {q : ℤ} (hq : 0 < q) :
    phase (next q false) = a * (1 - phase q) := by
  have ht := phase_pos hq
  have hu := phase_lt_one q
  have hlow : 0 < a * (1 - phase q) := mul_pos a_pos (by linarith)
  have hhigh : a * (1 - phase q) < 1 := by
    nlinarith [a_pos, a_lt_one, mul_pos a_pos ht]
  apply Int.fract_eq_iff.mpr
  refine ⟨le_of_lt hlow, hhigh, ?_⟩
  refine ⟨⌊phi * (q : ℝ)⌋ + q + 1, ?_⟩
  simp only [next, bit, Bool.false_eq_true, ↓reduceIte, add_zero]
  rw [A_eq hq]
  push_cast
  simp only [a, phase, Int.fract]
  nlinarith [congrArg (fun x : ℝ => x * (q : ℝ)) phi_sq]

lemma phase_one {q : ℤ} (hq : 0 < q) (h : Admissible q true) :
    phase (next q true) = a * (2 - phase q) := by
  have ht := phase_pos hq
  have hu := phase_lt_one q
  have hc := (one_admissible_iff hq).mp h
  have hlow : 0 < a * (2 - phase q) := mul_pos a_pos (by linarith)
  have hhigh : a * (2 - phase q) < 1 := by
    have hid : a * (2 - c) = 1 := by dsimp [a, c]; nlinarith [phi_sq]
    nlinarith [mul_pos a_pos (sub_pos.mpr hc)]
  apply Int.fract_eq_iff.mpr
  refine ⟨le_of_lt hlow, hhigh, ?_⟩
  refine ⟨⌊phi * (q : ℝ)⌋ + q + 2, ?_⟩
  simp only [next, bit, ↓reduceIte]
  rw [A_eq hq]
  push_cast
  simp only [a, phase, Int.fract]
  nlinarith [congrArg (fun x : ℝ => x * (q : ℝ)) phi_sq]

theorem zero_reflects {q : ℤ} (hq : 0 < q) :
    phase (next q false) - c = -a * (phase q - c) := by
  rw [phase_zero hq]
  nlinarith [fixed_point]

lemma after_one_high {q : ℤ} (hq : 0 < q) (h : Admissible q true) :
    c < phase (next q true) := by
  rw [phase_one hq h]
  have hh := mul_pos a_pos (sub_pos.mpr (phase_lt_one q))
  nlinarith [a_gt_c]

lemma initial_phase : phase 1 = a := by
  apply Int.fract_eq_iff.mpr
  refine ⟨le_of_lt a_pos, a_lt_one, 1, ?_⟩
  norm_num [a]

/-- `true` means an odd zero run; `false` means an even zero run. -/
def State (q : ℤ) (odd : Bool) : Prop :=
  if odd then phase q < c else c < phase q

lemma zero_flips {q : ℤ} (hq : 0 < q) {s : Bool} (hs : State q s) :
    State (next q false) (!s) := by
  have he := zero_reflects hq
  cases s <;> simp [State] at hs ⊢
  · nlinarith [mul_pos a_pos (sub_pos.mpr hs)]
  · nlinarith [mul_pos a_pos (sub_pos.mpr hs)]

def Trace (q : ℤ) : List Bool → Prop
  | [] => True
  | b :: bs => Admissible q b ∧ Trace (next q b) bs

def Accept (odd : Bool) : List Bool → Prop
  | [] => True
  | false :: bs => Accept (!odd) bs
  | true :: bs => odd = false ∧ Accept false bs

/-- Complete equivalence, not just necessity, with the two-state language. -/
theorem trace_iff_accept {q : ℤ} (hq : 0 < q) {s : Bool} (hs : State q s)
    (w : List Bool) : Trace q w ↔ Accept s w := by
  induction w generalizing q s with
  | nil => simp [Trace, Accept]
  | cons b bs ih =>
    cases b
    · simpa [Trace, Accept, zero_admissible] using
        ih (next_pos hq false) (zero_flips hq hs)
    · have heq : Admissible q true ↔ s = false := by
        rw [one_admissible_iff hq]
        cases s <;> simp [State] at hs ⊢ <;> linarith
      simp only [Trace, Accept]
      constructor
      · rintro ⟨ha, ht⟩
        exact ⟨heq.mp ha, (ih (next_pos hq true)
          (show State (next q true) false from after_one_high hq ha)).mp ht⟩
      · rintro ⟨he, ht⟩
        have ha := heq.mpr he
        exact ⟨ha, (ih (next_pos hq true)
          (show State (next q true) false from after_one_high hq ha)).mpr ht⟩

def decodeFrom (q : ℤ) : List Bool → ℤ
  | [] => q
  | b :: bs => decodeFrom (next q b) bs

def Encoded (n : ℤ) (w : List Bool) : Prop :=
  ∃ bs, w = true :: bs ∧ Trace 1 bs ∧ decodeFrom 1 bs = n

lemma trace_append (q : ℤ) (u v : List Bool) :
    Trace q (u ++ v) ↔ Trace q u ∧ Trace (decodeFrom q u) v := by
  induction u generalizing q with
  | nil => simp [Trace, decodeFrom]
  | cons b bs ih => simp [Trace, decodeFrom, ih, and_assoc]

lemma decode_append (q : ℤ) (u v : List Bool) :
    decodeFrom q (u ++ v) = decodeFrom (decodeFrom q u) v := by
  induction u generalizing q with
  | nil => rfl
  | cons b bs ih => simpa [decodeFrom] using ih (next q b)

lemma encoded_snoc {q : ℤ} {w : List Bool} (h : Encoded q w)
    (b : Bool) (ha : Admissible q b) : Encoded (next q b) (w ++ [b]) := by
  obtain ⟨bs, rfl, ht, hd⟩ := h
  refine ⟨bs ++ [b], rfl, ?_, ?_⟩
  · rw [trace_append, hd]
    exact ⟨ht, ha, trivial⟩
  · rw [decode_append, hd]
    rfl

/-- A forward quotient step always has a unique binary child digit. -/
lemma forward_step {n : ℤ} (hn : 0 < n) :
    let q := ⌊(n : ℝ) / phi⌋
    0 ≤ q ∧ q < n ∧ ∃ b : Bool, next q b = n ∧ Admissible q b := by
  let q : ℤ := ⌊(n : ℝ) / phi⌋
  have hn' : (0 : ℝ) < n := by exact_mod_cast hn
  have hqlo := Int.floor_le ((n : ℝ) / phi)
  have hqhi := Int.lt_floor_add_one ((n : ℝ) / phi)
  change (q : ℝ) ≤ (n : ℝ) / phi at hqlo
  change (n : ℝ) / phi < (q : ℝ) + 1 at hqhi
  have hlo : phi * (q : ℝ) ≤ n := by
    have := (le_div_iff₀ phi_pos).mp hqlo
    nlinarith
  have hhi : (n : ℝ) < phi * ((q : ℝ) + 1) := by
    have := (div_lt_iff₀ phi_pos).mp hqhi
    nlinarith
  have hq0 : 0 ≤ q := Int.floor_nonneg.mpr (le_of_lt (div_pos hn' phi_pos))
  have hqlt : q < n := by
    have hdiv : (n : ℝ) / phi < n := by
      apply (div_lt_iff₀ phi_pos).mpr
      nlinarith [mul_pos hn' (sub_pos.mpr phi_gt_one)]
    have hreal : (q : ℝ) < n := lt_of_le_of_lt hqlo hdiv
    exact_mod_cast hreal
  have hAlo : A q ≤ n := Int.ceil_le.mpr hlo
  have hc := Int.le_ceil (phi * (q : ℝ))
  change phi * (q : ℝ) ≤ (A q : ℝ) at hc
  have hAhi : n < A q + 2 := by
    have hr : (n : ℝ) < (A q : ℝ) + 2 := by nlinarith [phi_lt_two]
    exact_mod_cast hr
  refine ⟨hq0, hqlt, ?_⟩
  by_cases he : n = A q
  · refine ⟨false, ?_, ?_⟩
    · change A q + 0 = n
      omega
    · exact zero_admissible q
  · have he' : n = A q + 1 := by omega
    refine ⟨true, ?_, ?_⟩
    · exact he'.symm
    · have hv : next q true = n := he'.symm
      unfold Admissible
      rw [hv]
      exact hhi

/-- Every positive integer has an exact encoding; the specification is inhabited. -/
theorem exists_encoded (n : ℕ) (hn : 0 < n) : ∃ w, Encoded (n : ℤ) w := by
  revert hn
  induction n using Nat.strong_induction_on with
  | h n ih =>
    intro hn
    have hnz : (0 : ℤ) < n := by exact_mod_cast hn
    obtain ⟨hq0, hqlt, b, hb, ha⟩ := forward_step hnz
    let q : ℤ := ⌊((n : ℤ) : ℝ) / phi⌋
    change 0 ≤ q at hq0
    change q < n at hqlt
    change next q b = n at hb
    change Admissible q b at ha
    by_cases hq : q = 0
    · have hn1 : n = 1 := by
        cases b <;> simp [hq, next, bit, A] at hb <;> omega
      subst n
      exact ⟨[true], [], rfl, trivial, rfl⟩
    · have hqp : 0 < q.toNat := by omega
      have hqn : q.toNat < n := by omega
      obtain ⟨w, hw⟩ := ih q.toNat hqn hqp
      have hcast : (q.toNat : ℤ) = q := Int.toNat_of_nonneg hq0
      rw [hcast] at hw
      exact ⟨w ++ [b], hb ▸ encoded_snoc hw b ha⟩

theorem encoded_language {n : ℤ} {w : List Bool} (h : Encoded n w) : Accept false w := by
  obtain ⟨bs, rfl, ht, _⟩ := h
  have hs : State 1 false := by simpa [State, initial_phase] using a_gt_c
  exact ⟨rfl, (trace_iff_accept (by norm_num) hs bs).mp ht⟩

/-- Every accepted suffix really occurs, so the language characterization is exact. -/
theorem language_iff (bs : List Bool) :
    (∃ n : ℤ, Encoded n (true :: bs)) ↔ Accept false bs := by
  constructor
  · rintro ⟨n, hn⟩
    exact (encoded_language hn).2
  · intro ha
    have hs : State 1 false := by simpa [State, initial_phase] using a_gt_c
    refine ⟨decodeFrom 1 bs, bs, rfl, ?_, rfl⟩
    exact (trace_iff_accept (by norm_num) hs bs).mpr ha

lemma accept_suffix {s : Bool} (u v : List Bool) (h : Accept s (u ++ v)) :
    ∃ t, Accept t v := by
  induction u generalizing s with
  | nil => exact ⟨s, h⟩
  | cons b bs ih =>
    cases b
    · exact ih h
    · exact ih h.2

lemma odd_zeros (k : ℕ) (s : Bool) (v : List Bool) :
    Accept s (List.replicate (2*k+1) false ++ v) ↔ Accept (!s) v := by
  induction k generalizing s with
  | zero => simp [Accept]
  | succ k ih =>
    have hk : 2 * (k + 1) + 1 = 2 + (2*k+1) := by omega
    rw [hk, List.replicate_add, List.append_assoc]
    simpa [List.replicate_succ, Accept] using ih s

/-- No odd-length run of zeros can be bounded by ones anywhere in a codeword. -/
theorem no_odd_gap {n : ℤ} {w : List Bool} (h : Encoded n w)
    (u v : List Bool) (k : ℕ) :
    w ≠ u ++ (true :: (List.replicate (2*k+1) false ++ true :: v)) := by
  intro hw
  have ha := encoded_language h
  rw [hw] at ha
  obtain ⟨s, hs⟩ := accept_suffix u _ ha
  have ht := (odd_zeros k false (true :: v)).mp hs.2
  simp [Accept] at ht

theorem no_101 {n : ℤ} {w : List Bool} (h : Encoded n w)
    (u v : List Bool) : w ≠ u ++ [true, false, true] ++ v := by
  simpa using no_odd_gap h u v 0

#print axioms no_101
#print axioms no_odd_gap
#print axioms trace_iff_accept
#print axioms quotient_step
#print axioms exists_encoded
#print axioms language_iff

end
end PhiPacking
