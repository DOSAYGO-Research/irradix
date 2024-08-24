#!/usr/bin/env python
from mpmath import mp, mpf, sqrt, floor, ceil, log, log10

# Initialize global variables for BigPHI
current_bigphi_dps = 100
mp.dps = current_bigphi_dps
_bigphi_value = (mpf(1) + sqrt(mpf(5))) / 2

# Getter for BigPHI in VALS
def get_bigphi():
    return _bigphi_value

# Constants dictionary with dynamic getter
VALS = {
    'BigPHI': get_bigphi,
}

# Debug flag
DEBUG = False

# API to set the precision (dps) dynamically
def set_precision(dps):
    global current_bigphi_dps, _bigphi_value
    current_bigphi_dps = dps
    mp.dps = current_bigphi_dps
    _bigphi_value = (mpf(1) + sqrt(mpf(5))) / 2  # Recalculate BigPHI with new precision

def irradix(num):
    num = mpf(num)
    if num == 0:
        return "0"

    if not num % 1 == 0:
        raise TypeError("Sorry cannot convert non-integer numbers.")

    S = mp.sign(num)

    if S == -1:
        num = num * S

    w = [num, 0]
    r = []
    lastW = list(w)

    bigphi = VALS['BigPHI']()  
    quanta = bigphi ** -(log(num) / log(bigphi))
    epsilon = mpf(2) ** -mp.prec

    thresh = min(quanta, epsilon)

    while True:
        if abs(w[0]) <= thresh:
            break

        w[1] = w[0] % bigphi

        if w[1] < 0:
            w[1] = w[1] - bigphi

        w[0] = (w[0] - w[1]) / bigphi

        if abs(w[0]) >= abs(lastW[0]):
            if mp.sign(bigphi) == -1:
                if w[0] == 0:
                    break
            else:
                break

        unit = floor(abs(w[1]))
        r.insert(0, str(int(unit)))

        lastW = list(w)

    if S == -1:
        r.insert(0, '-')

    return ''.join(r)

def derradix(rep):
    S = -1 if rep[0] == '-' else 1

    if S == -1:
        rep = rep[1:]

    bigphi = VALS['BigPHI']()  

    # Ensure the rep string is correctly split into integers
    rep = [mpf(int(u, 10)) for u in rep]
    num = mpf(0)
    for u in rep:
        num = num * bigphi
        num = ceil(num + u)

    return int(num * S)

def encode(nums):
    encoded_list = []
    for num in nums:
        binary_rep = irradix((num + 1) * 2)
        if DEBUG:
            print(f"Initial Binary Representation for {num}: {binary_rep}")

        if binary_rep.endswith('10'):
            binary_rep += '0101'
            if DEBUG:
                print(f"Appended 0101 for {num} because it ends with 10: {binary_rep}")

        encoded_list.append(binary_rep)

    concatenated = '101'.join(encoded_list)
    if DEBUG:
        print(f"Concatenated Sequence Before Padding: {concatenated}")

    padding_length = (8 - len(concatenated) % 8) % 8
    padded_sequence = '0' * padding_length + concatenated
    if DEBUG:
        print(f"Padded Sequence (left padding with zeros): {padded_sequence} (Padding Length: {padding_length})")

    chunks = [padded_sequence[i:i + 8] for i in range(0, len(padded_sequence), 8)]
    if DEBUG:
        print(f"8-bit Chunks: {chunks}")

    chunk_values = [int(chunk, 2) for chunk in chunks]
    if DEBUG:
        print(f"Encoded Chunk Values: {chunk_values}")

    return chunk_values

def decode(chunks):
    binary_chunks = [bin(chunk)[2:].zfill(8) for chunk in chunks]
    if DEBUG:
        print(f"Binary Chunks: {binary_chunks}")

    reconstructed = ''.join(binary_chunks)
    if DEBUG:
        print(f"Reconstructed Sequence Before Removing Padding: {reconstructed}")

    leading_zeros = len(reconstructed) - len(reconstructed.lstrip('0'))
    if DEBUG:
        print(f"Identified Leading Zeros (Padding Length): {leading_zeros}")

    reconstructed = reconstructed[leading_zeros:]
    if DEBUG:
        print(f"Reconstructed Sequence (after removing leading zeros): {reconstructed}")

    rep_strings = reconstructed.split('101')
    if DEBUG:
        print(f"Split Representation Strings: {rep_strings}")

    numbers = []
    for i in range(len(rep_strings)):

        if rep_strings[i]:
            if i < len(rep_strings) - 1 and not rep_strings[i+1]:
                if DEBUG:
                    print(f"\n\nEmpty spot found, adjusting representation: {rep_strings[i]}")
                rep_strings[i] = rep_strings[i][:-1]
                if DEBUG:
                    print(f"Empty spot found, adjusting representation: {rep_strings[i]}\n\n")
            num = (derradix(rep_strings[i]) // 2) - 1
            numbers.append(num)

    if DEBUG:
        print(f"Decoded Numbers: {numbers}")
    return numbers

# online variants, suitable for streaming
# online encode
def olencode(nums):
  return encode(nums)

# online decode 
def oldecode(chunks):
  return decode(chunks)

# l1 - length first variants, suitable when numbers are known ahead of time
# length first encode and decode
def l1encode(nums):
    # Step 1: Calculate the bit lengths of the numbers in base-2
    lengths = [num.bit_length() for num in nums]
    
    # Step 2: Encode the lengths using olencode
    encoded_lengths = olencode(lengths)
    
    # Step 3: Concatenate the bit strings of the numbers themselves
    concatenated_bits = ''.join(bin(num)[2:] for num in nums)
    
    # Step 4: Append the triple '101' sequence and the concatenated bits
    triple_101 = '101101101'
    full_bit_sequence = triple_101 + concatenated_bits

    # Step 5: Convert the full bit sequence into 8-bit chunks
    padded_sequence = '0' * ((8 - len(full_bit_sequence) % 8) % 8) + full_bit_sequence
    chunked_sequence = [padded_sequence[i:i+8] for i in range(0, len(padded_sequence), 8)]
    
    # Step 6: Convert the 8-bit chunks to integers and concatenate with encoded lengths
    final_sequence = encoded_lengths + [int(chunk, 2) for chunk in chunked_sequence]
    
    return final_sequence

def l1decode(chunks):
    # Step 1: Convert chunks to binary strings
    binary_chunks = [bin(chunk)[2:].zfill(8) for chunk in chunks]
    full_sequence = ''.join(binary_chunks)

    # Step 2: Split by '101' delimiter to separate the encoded lengths and concatenated bits
    parts = full_sequence.split('101')

    # Step 3: Find the triple '101' sequence and determine the separation point
    triple_101_idx = next(i for i in range(len(parts) - 2) if parts[i] == parts[i+1] == parts[i+2] == '')

    # Step 4: Decode the lengths sequence using oldecode
    encoded_lengths = [int(part, 2) for part in parts[:triple_101_idx]]
    lengths = oldecode(encoded_lengths)

    # Step 5: The remaining part is the concatenated bits of the integers
    concatenated_bits = ''.join(parts[triple_101_idx+3:])

    # Step 6: Reconstruct the original numbers using the decoded lengths
    numbers = []
    pos = 0
    for length in lengths:
        num_bits = concatenated_bits[pos:pos + length]
        num = int(num_bits, 2)
        numbers.append(num)
        pos += length
    
    return numbers

