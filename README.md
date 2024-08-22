# Properties of a Novel Binary Representation of Integers using Base $\phi$

## Introduction

This project explores a novel method for encoding integers using a representation based on the golden ratio ($\phi$), known as the irrational base $\phi$. This encoding method leverages the unique mathematical properties of $\phi$ to create a binary-like representation that inherently avoids certain binary sequences. The exploration focuses on analyzing the characteristics of this representation, particularly when reinterpreted as standard binary numbers, and the unexpected findings related to prime density in the transformed number set.

## Mathematical Foundation

### Base $\phi$ Representation

The golden ratio $\phi$ is defined as:

$$phi = \frac{1 + \sqrt{5}}{2} \approx 1.618033988749895$$

Encoding integers using base $\phi$ involves representing numbers in a non-standard manner, where the expansion factor in terms of binary bits is approximately:

$$frac{\log(2)}{\log(\phi)} \approx 1.44$$

This suggests that base $\phi$ encoding requires around 44% more bits than traditional binary encoding. Despite this apparent inefficiency, base $\phi$ encoding has unique properties, such as naturally excluding the sequence "101," which we use as a delimiter.

### Conversion Algorithms for Base $\phi$ Encoding: `irradix` and `derradix`

This section provides a detailed explanation of the conversion algorithms used in the `irradix` and `derradix` functions, including their mathematical foundations. Both algorithms revolve around the idea of encoding and decoding integers using a base $\phi$ representation, where $\phi$ is the golden ratio.

#### `irradix` Algorithm

The `irradix` function converts a positive integer $\( n \)$ into its base $\phi$ representation. The process involves iterative calculations that decompose the number into a series of coefficients that correspond to powers of $\phi$.

```math
\text{irradix}(n) =
\begin{aligned}
  & w_0 = n, \quad r = [] \\
  & \text{while } |w_0| > \text{thresh}: \\
  & \quad r_i = \left\lfloor w_0 \mod \phi \right\rfloor \\
  & \quad w_1 = \frac{w_0 - r_i}{\phi} \\
  & \quad \text{update } r = [r_i] + r \\
  & \quad w_0 \leftarrow w_1
\end{aligned}
```

The result, $\( r \)$, is the string of digits that represents $\( n \)$ in base $\phi$.

#### `derradix` Algorithm

The `derradix` function performs the inverse operation, converting a base $\phi$ representation back into the original integer. It interprets the base $\phi$ digits and reconstructs the number through a series of multiplication and summation steps, applying the ceiling function at each step.

```math
\text{derradix}(r) = \left\lceil \sum_{i=0}^{k} r_i \phi^{k-i} \right\rceil
```

In this equation, $\( r_i \)$ represents the digits of the base $\phi$ encoded number, and the sum reconstructs the original integer.

### Iterative Radix Conversion with Ceil Function

As discussed earlier, in the `derradix` function, we must apply the ceiling operation iteratively at each step of the summation:

```math
n = \left\lceil a_0 + \left\lceil \phi \cdot \left( a_1 + \left\lceil \phi \cdot \left( a_2 + \cdots \right) \right\rceil \right) \right\rceil \right\rceil
```

This corresponds to the code, where the ceiling is applied after each multiplication by $\phi$ and addition of the next digit.

### Notes

- **Sign Handling**: The above algorithms omit sign handling for clarity. In practice, if the original integer is negative, the algorithm first converts it to a positive number, performs the conversion, and then adds a negative sign to the final result.
  
- **Termination Conditions in `irradix`**:
  - **$\(\text{thresh}\)$**: A small threshold value that stops the loop once the magnitude of $\( w_0 \)$ is sufficiently small.
  - **$\(\text{quanta}\)$**: Represents a precision level, ensuring that the algorithm's results are accurate.
  - **$\(\epsilon\)$**: A small value related to the precision of floating-point arithmetic, ensuring that the loop halts when further iterations no longer contribute meaningful digits.

## Exploring Base $\phi$ Representation

### Analysis and Observations

We analyzed the first 1,000 integers encoded using the base $\phi$ system, converting these representations back into integers by treating them as binary numbers. The analysis revealed unexpected behavior in the distribution and density of prime numbers in the transformed set, particularly when compared to the original integer set.

### Prime Density Anomaly

Interestingly, when we mapped the first 1,000 integers through the base $\phi$ representation, we observed an unexpected prime density in the reinterpreted binary set. Given the nature of the expansion factor, one would anticipate a decrease in prime density by a factor corresponding to the expansion ratio. However, our findings suggest that the prime density in the reinterpreted set is significantly higher than expected.

This anomaly indicates that the base $\phi$ mapping may lead to a disproportionately higher number of primes in the transformed set compared to a uniform distribution. This finding could imply deeper number-theoretic properties associated with base $\phi$ representations, potentially linked to how $\phi$ interacts with the distribution of primes.

### Statistical Considerations

From a statistical number theory perspective, the observed increase in prime density could be an artifact of how base $\phi$ encoding clusters certain types of integers. Given that base $\phi$ avoids certain sequences, it might be preferentially preserving numbers that are prime when interpreted as binary, thus inflating the prime density in the resulting set. Further exploration into this phenomenon could involve analyzing whether similar patterns emerge with other irrational bases or if this effect is unique to $\phi$.

## Integer Packaging and Efficiency

### Delimiter-Based Packing

One of the key applications of the base $\phi$ representation explored in this project is integer packaging. The exclusion of the "101" sequence in the base $\phi$ encoded strings makes this encoding suitable for delimiter-based packing schemes, where "101" serves as a marker for separating individual encoded integers. This approach is particularly space-efficient as it avoids the need for additional length signifiers that are common in traditional length-type-value or length-value encoding schemes.

### Efficiency of Packing

The practical efficiency of this packing method lies in its ability to represent multiple integers in a compressed format, using the inherent properties of the base $\phi$ system to delimit sequences without explicit markers. However, this method does introduce some redundancy, particularly when sequences must be padded to prevent unintentional "101" patterns. Despite this, the space savings from avoiding explicit length markers can be significant, making this method advantageous in certain contexts.

### Connection to Binary Representation of 5

It is noteworthy that the sequence "101" corresponds to the binary representation of the number 5. In the context of base $\phi$ encoding, the exclusion of this sequence as a delimiter creates an interesting intersection between number theory and binary encoding. This connection suggests potential links to other irrational bases derived from primes, such as $\(\sqrt{7}\)$, which might naturally avoid other specific sequences like "111" (binary for 7).

## Implications for Prime Density and Number Theory

### Expected vs. Observed Prime Density

Given the expansion factor of approximately 1.44 in base $\phi$ encoding, one would expect the density of primes in the reinterpreted binary set to decrease proportionally. Specifically, if the prime density in the original set is around 16.8%, the expected prime density in the binary reinterpreted set should be approximately:

$$\frac{16.8\%}{8} \approx 2.1\%$$

However, the observed prime density in the binary set is significantly higher, around 9.5%. This discrepancy suggests that the base $\phi$ mapping might be influencing the distribution of primes in a way that is not immediately apparent from a uniform distribution perspective.

### Statistical Number Theory Perspective

This unexpected increase in prime density raises intriguing questions about the nature of the base $\phi$ encoding and its impact on number theory. It is possible that the encoding method selectively preserves or amplifies the presence of primes due to the unique properties of $\phi$. Further research could explore whether this phenomenon is specific to base $\phi$ or if similar effects are observed with other irrational bases.

## Conclusion and Future Directions

The exploration of base $\phi$ as a novel binary encoding method has uncovered intriguing and unexpected properties, particularly regarding prime density and integer packaging efficiency. While the practical applications may be limited due to the complexity of base $\phi$ arithmetic, the theoretical implications are compelling and warrant further investigation.

### Summary of Python API

The Python API provided here leverages the mathematical properties of the golden ratio $\phi$ for encoding and decoding integers using a base $\phi$ representation. The key functions included in this API are as follows:

- **`irradix(num)`**: Converts a given integer into its base $\phi$ representation. This function handles the decomposition of the number into coefficients that correspond to powers of $\phi$, returning a string that represents the number in base $\phi$.

- **`derradix(rep)`**: Decodes a base $\phi$ encoded string back into the original integer. It reconstructs the number by summing the products of the coefficients and powers of $\phi$, with a ceiling operation applied at each step to ensure accuracy.

- **`encode(nums)`**: Packs a list of arbitrarily-sized integers using the base $\phi$ encoding scheme. This function concatenates the encoded integers, handles padding, and converts the final sequence into an array of bytes.

- **`decode(chunks)`**: Unpacks a sequence of encoded integers from an input of bytes, by reconstructing the original sequence, and decoding it back into the list of integers.

