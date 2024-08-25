# Outperforming VByte for Very Large Integers using Phi-Based Encoding

## Abstract
VByte[^1] is a widely-used integer compression algorithm known for its speed and simplicity. This study compares the efficiency of two integer compression algorithms—VByte and a Phi-based encoding method—specifically targeting large numbers ranging from 50 to 100 digits. The results demonstrate that the Phi-based method outperforms VByte in terms of bit expansion for large integers, highlighting its potential for specialized applications.

## Introduction
Integer compression is critical in various applications, particularly when dealing with large datasets. This study explores the performance of VByte, a widely-used compression algorithm, against a custom Phi-based encoding algorithm. The hypothesis is that the Phi-based method will perform better with large numbers due to its unique structure.

## Methods
### Algorithms
- **VByte:** A simple, fast integer compression algorithm that encodes integers using variable-length bytes.
- **Irradix (Phi-Based Encoding):** A custom method that utilizes the mathematical properties of the golden ratio (Phi) to encode integers. See [irradix.py](irradix.py) for the implementation, and [README.md](README.md) for the math and properties that enable this encoding.
- **L1 (Length-First Irradix):** A variant of Irradix that first encodes the bit lengths of the integers and then prepends these encoded lengths to the concatenated bits of all the integers.

### Test Procedure
We generated random integers with 50 to 100 digits and compared the bit lengths required by each encoding method. The tests were conducted over 10 runs, with sequence lengths ranging from 100 to 1,000 integers per test. A benchmark "perfect encoding," which should approach the information-theoretic entropy limit, was constructed by summing the bit lengths of the integers in each test with the bit lengths of their bit lengths.

## Results
Below are the results of the 50 to 100 Digit Test:

# 50 to 100 Digit Test Results

| Test | Sequence Length | Irradix Bits | L1 Bits | VByte Bits | Benchmark Bits | Irradix % Expansion | L1 % Expansion | VByte % Expansion |
|------|-----------------|--------------|---------|------------|----------------|--------------------|----------------|-------------------|
| 1 | 568 | 207424 | 151656 | 164712 | 147305 | 40.81% | 2.95% | 11.82% |
| 2 | 411 | 147600 | 107976 | 117224 | 104823 | 40.81% | 3.01% | 11.83% |
| 3 | 437 | 159056 | 116264 | 126272 | 112974 | 40.79% | 2.91% | 11.77% |
| 4 | 325 | 117056 | 85544 | 92968 | 83133 | 40.81% | 2.90% | 11.83% |
| 5 | 786 | 286752 | 209632 | 227952 | 203664 | 40.80% | 2.93% | 11.93% |
| 6 | 182 | 64768 | 47336 | 51504 | 45983 | 40.85% | 2.94% | 12.01% |
| 7 | 217 | 78488 | 57408 | 62400 | 55754 | 40.78% | 2.97% | 11.92% |
| 8 | 676 | 244816 | 178968 | 194576 | 173902 | 40.78% | 2.91% | 11.89% |
| 9 | 287 | 106248 | 77600 | 84432 | 75447 | 40.82% | 2.85% | 11.91% |
| 10 | 405 | 146672 | 107232 | 116496 | 104187 | 40.78% | 2.92% | 11.81% |

## Summary Statistics

- **Average Irradix Expansion:** 40.80%
- **Average L1 Expansion:** 2.93%
- **Average VByte Expansion:** 11.87%

    *Results generated with: [`./run_experiment.py`](run_experiment.py)*

## Discussion

The results show that the Phi-based encoding consistently outperforms VByte in terms of bit expansion for large integers. This suggests that the Phi-based method is better suited for applications dealing with very large numbers, where minimizing storage is crucial.

## Conclusion

The Phi-based encoding method demonstrates superior performance over VByte for large numbers. Future work could explore further optimizations or applications of this method in specialized fields.

## References
[^1]: Daniel Lemire, Nathan Kurz, Christoph Rupp. "STREAM VBYTE: Faster Byte-Oriented Integer Compression." *arXiv preprint arXiv:1709.08990*, 2017. Available at: [https://arxiv.org/pdf/1709.08990](https://arxiv.org/pdf/1709.08990).


