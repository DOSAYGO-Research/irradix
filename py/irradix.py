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
    # Add other constants here as needed
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

    bigphi = VALS['BigPHI']()  # Use the getter to get the current BigPHI value
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

    bigphi = VALS['BigPHI']()  # Use the getter to get the current BigPHI value

    # Ensure the rep string is correctly split into integers
    rep = [mpf(int(u, 10)) for u in rep]
    num = mpf(0)
    for u in rep:
        num = num * bigphi
        num = ceil(num + u)

    return int(num * S)

