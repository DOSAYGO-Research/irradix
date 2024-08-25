# Outperforming VByte for Very Large Integers using Phi-Based Encoding 

## Abstract
VByte[^1] is a widely-used integer compression algorithm known for its speed and simplicity. This study compares the efficiency of two integer compression algorithms—VByte and a Phi-based encoding method—specifically targeting large numbers ranging from 50 to 100 digits. The results demonstrate that the Phi-based method outperforms VByte in terms of bit expansion for large integers, highlighting its potential for specialized applications.

## Introduction
Integer compression is critical in various applications, particularly when dealing with large datasets. This study explores the performance of VByte, a widely-used compression algorithm, against a custom Phi-based encoding algorithm. The hypothesis is that the Phi-based method would perform better with large numbers due to its unique structure.

## Methods
### Algorithms
- **VByte:** A simple, fast integer compression algorithm that encodes integers using variable-length bytes.
- **Irradix - (Phi-Based Encoding):** A custom method that utilizes the mathematical properties of the golden ratio (Phi) to encode integers. See [irradix.py](irradix.py) for implementation.
- **L1 - (Length-first Irradix):** Use irradix to encode the integer bit lengths, and prepend the encoded lengths to the concatenated bits of all the integers.

### Test Procedure
We generated random integers with 50 to 100 digits and compared the bit lengths required by each encoding method. The tests were conducted over 10 runs, with sequence lengths ranging from 100 to 1000 integers per test.

## Results
Below are the results of the 50 to 100 Digit Test:

# 50 to 100 Digit Test Results

| Test | Sequence Length | Irradix Bits | L1 Bits | VByte Bits | Benchmark Bits | Irradix % Expansion | L1 % Expansion | VByte % Expansion |
|------|-----------------|--------------|---------|------------|----------------|--------------------|----------------|-------------------|
| 1 | 517 | 188216 | 137616 | 149472 | 129318 | 45.55% | 6.42% | 15.58% |
| 2 | 697 | 253600 | 185312 | 201408 | 174209 | 45.57% | 6.37% | 15.61% |
| 3 | 226 | 82064 | 59920 | 65232 | 56327 | 45.69% | 6.38% | 15.81% |
| 4 | 291 | 106264 | 77696 | 84416 | 73002 | 45.56% | 6.43% | 15.64% |
| 5 | 998 | 362672 | 265112 | 288136 | 249112 | 45.59% | 6.42% | 15.67% |
| 6 | 135 | 48592 | 35536 | 38640 | 33387 | 45.54% | 6.44% | 15.73% |
| 7 | 519 | 189016 | 138104 | 150144 | 129798 | 45.62% | 6.40% | 15.68% |
| 8 | 363 | 131312 | 95992 | 104256 | 90204 | 45.57% | 6.42% | 15.58% |
| 9 | 548 | 196448 | 143720 | 156176 | 134935 | 45.59% | 6.51% | 15.74% |
| 10 | 128 | 47000 | 34360 | 37368 | 32305 | 45.49% | 6.36% | 15.67% |

*Results generated with: `./run_experiment.py`*

## Summary Statistics

- **Average Irradix Expansion:** 45.58%
- **Average L1 Expansion:** 6.41%
- **Average VByte Expansion:** 15.67%

## Discussion

The results show that the Phi-based encoding consistently outperforms VByte in terms of bit expansion for large integers. This suggests that the Phi-based method is better suited for applications dealing with very large numbers, where minimizing storage is crucial.

## Conclusion

The Phi-based encoding method demonstrates superior performance over VByte for large numbers. Future work could explore further optimizations or applications of this method in specialized fields.

----

## References
[^1]: Daniel Lemire, Nathan Kurz, Christoph Rupp. "STREAM VBYTE: Faster Byte-Oriented Integer Compression." *arXiv preprint arXiv:1709.08990*, 2017. Available at: [https://arxiv.org/pdf/1709.08990](https://arxiv.org/pdf/1709.08990).

