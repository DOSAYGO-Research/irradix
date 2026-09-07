import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-!
The integer carry invariant used by `research/phi_arithmetic.py`.
This file proves the unrestricted carry equation and the addition acceptance
criterion for augmented Fibonacci-weight words, plus scaled Horner multiplication. The canonical-word identity,
finite carry bound, graph trimming, and Python solver are proved/discussed in
ARITHMETIC.md; they are not formalized in this file.
-/
namespace PhiArithmetic

def fib : Nat → Int
  | 0 => 0
  | 1 => 1
  | n + 2 => fib (n + 1) + fib n

theorem fib_step (n : Nat) : fib (n + 2) = fib (n + 1) + fib n := rfl

abbrev Carry := Int × Int

def step (c : Carry) (d : Int) : Carry := (c.2 + d, c.1 + c.2)

def run : Carry → List Int → Carry
  | c, [] => c
  | c, d :: ds => run (step c d) ds

/-- Fibonacci weights F_(j+1), with most significant digit first. -/
def weighted : List Int → Int
  | [] => 0
  | d :: ds => d * fib (ds.length + 1) + weighted ds

theorem run_value (c : Carry) (ds : List Int) :
    (run c ds).1 + (run c ds).2 =
      fib (ds.length + 1) * c.1 + fib (ds.length + 2) * c.2 + weighted ds := by
  induction ds generalizing c with
  | nil => simp [run, weighted, fib]
  | cons d ds ih =>
    simp only [run, weighted, List.length_cons]
    rw [ih]
    have hf : fib (ds.length + 3) = fib (ds.length + 2) + fib (ds.length + 1) := by
      simpa [Nat.add_assoc] using fib_step (ds.length + 1)
    simp only [step, Nat.add_assoc]
    rw [hf]
    ring

theorem run_zero_value (ds : List Int) :
    (run (0, 0) ds).1 + (run (0, 0) ds).2 = weighted ds := by
  simpa using run_value (0, 0) ds

abbrev Column := Int × Int × Int

def leftDigits (cs : List Column) : List Int := cs.map (fun c => c.1)
def rightDigits (cs : List Column) : List Int := cs.map (fun c => c.2.1)
def outputDigits (cs : List Column) : List Int := cs.map (fun c => c.2.2)
def differenceDigits (cs : List Column) : List Int :=
  cs.map (fun c => c.1 + c.2.1 - c.2.2)

theorem weighted_difference (cs : List Column) :
    weighted (differenceDigits cs) =
      weighted (leftDigits cs) + weighted (rightDigits cs) - weighted (outputDigits cs) := by
  induction cs with
  | nil => rfl
  | cons c cs ih =>
    simp only [differenceDigits, leftDigits, rightDigits, outputDigits,
      List.map_cons, weighted, List.length_map] at *
    rw [ih]
    ring

/-- Acceptance is equivalent to a+b=c whenever augmented words weigh n+1. -/
theorem addition_iff (cs : List Column) (a b c : Int)
    (ha : weighted (leftDigits cs) = a + 1)
    (hb : weighted (rightDigits cs) = b + 1)
    (hc : weighted (outputDigits cs) = c + 1) :
    let carry := run (0, 0) (differenceDigits cs)
    carry.1 + carry.2 = 1 ↔ a + b = c := by
  dsimp
  rw [run_zero_value, weighted_difference, ha, hb, hc]
  constructor <;> intro h <;> linarith

/-- Fibonacci-weight Horner step scaled by the multiplicand n. -/
def multiplyStep (n : Int) (c : Carry) (d : Int) : Carry :=
  (c.1 + c.2 + d * n, c.1)

def multiplyRun (n : Int) : Carry → List Int → Carry
  | c, [] => c
  | c, d :: ds => multiplyRun n (multiplyStep n c d) ds

theorem multiply_run_value (n : Int) (c : Carry) (ds : List Int) :
    (multiplyRun n c ds).1 =
      fib (ds.length + 1) * c.1 + fib ds.length * c.2 + n * weighted ds := by
  induction ds generalizing c with
  | nil => simp [multiplyRun, weighted, fib]
  | cons d ds ih =>
    simp only [multiplyRun, weighted, List.length_cons]
    rw [ih]
    simp only [multiplyStep, Nat.add_assoc]
    rw [fib_step ds.length]
    ring

/-- Remove the augmentation offset after scaled Horner evaluation. -/
theorem multiplication_value (n m : Int) (ds : List Int)
    (hm : weighted ds = m + 1) :
    (multiplyRun n (0, 0) ds).1 - n = n * m := by
  rw [multiply_run_value, hm]
  simp only [mul_zero, add_zero]
  ring

/-- The implementation starts after reading the augmentation bit. -/
theorem multiplication_initial (n : Int) (ds : List Int) :
    multiplyRun n (0, 0) (1 :: ds) = multiplyRun n (n, 0) ds := by
  simp [multiplyRun, multiplyStep]

#print axioms run_value
#print axioms weighted_difference
#print axioms addition_iff
#print axioms multiply_run_value
#print axioms multiplication_value

end PhiArithmetic
