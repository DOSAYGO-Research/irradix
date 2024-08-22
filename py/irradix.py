from mpmath import mp, mpf, sqrt, floor, ceil, log, log10

# Initialize global variables for BigPHI
current_bigphi_dps = 1000
mp.dps = current_bigphi_dps
_bigphi_value = (mpf(1) + sqrt(mpf(5))) / 2

# Getter for BigPHI in VALS
def get_bigphi():
    return _bigphi_value

# Constants dictionary with dynamic getter
VALS = {
    'BigPHI': get_bigphi,
}

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
    nums = [irradix((n+1)*2) for n in nums]
    concatenated = '101'.join(nums)  # Concatenate with '101' as delimiter
    print("Concatenated sequence:", concatenated)

    # Convert the concatenated sequence into 8-bit chunks
    padded_sequence = concatenated + ('0' * (8 - len(concatenated) % 8))
    chunks = [padded_sequence[i:i+8] for i in range(0, len(padded_sequence), 8)]
    print("8-bit chunks:", chunks)

    # Convert each 8-bit chunk to an integer
    chunk_values = [int(chunk, 2) for chunk in chunks]
    print("Chunk values:", chunk_values)

    return chunk_values

def decode(chunks):
    # Convert chunks back to binary strings
    binary_chunks = [bin(chunk)[2:].zfill(8) for chunk in chunks]
    print("Binary chunks:", binary_chunks)

    # Reconstruct the full sequence
    reconstructed = ''.join(binary_chunks).rstrip('0')  # Remove padding zeros
    print("Reconstructed sequence:", reconstructed)

    # Split the sequence by the delimiter '101'
    rep_strings = reconstructed.split('101')
    print("Recovered reps:", rep_strings)

    # Decode each rep back to its original number
    numbers = [(derradix(rep) // 2) - 1 for rep in rep_strings if rep]
    print("Recovered numbers:", numbers)

    return numbers

