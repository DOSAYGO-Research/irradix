from mpmath import mp, mpf, sqrt, floor, log

# Set precision
mp.dps = 400  # digits of precision

# Generate BigPHI programmatically (phi = (1 + sqrt(5)) / 2)
BigPHI = (mpf(1) + sqrt(mpf(5))) / 2

# Constants dictionary
VALS = {
    'BigPHI': BigPHI,
    # Add other constants here as needed
}

def irradix(num, radic=BigPHI):
    num = mpf(num)
    if num == 0:
        return "0"

    if not num % 1 == 0:
        raise TypeError("Sorry cannot convert non-integer numbers.")

    radic = mpf(radic)
    if abs(radic) <= 1:
        raise TypeError("Sorry we don't support radices less than or equal to 1")

    S = mp.sign(num)

    if S == -1:
        num = num * S

    w = [num, 0]
    r = []
    lastW = list(w)

    quanta = radic ** -(log(num) / log(radic))
    epsilon = mpf(2) ** -mp.prec

    thresh = min(quanta, epsilon)

    while True:
        if abs(w[0]) <= thresh:
            break

        w[1] = w[0] % radic

        if w[1] < 0:
            w[1] = w[1] - radic

        w[0] = (w[0] - w[1]) / radic

        if abs(w[0]) >= abs(lastW[0]):
            if mp.sign(radic) == -1:
                if w[0] == 0:
                    break
            else:
                break

        unit = floor(abs(w[1]))
        r.insert(0, str(unit))

        lastW = list(w)

    if S == -1:
        r.insert(0, '-')

    return ''.join(r)

def derradix(rep, radic=BigPHI):
    S = -1 if rep[0] == '-' else 1

    if S == -1:
        rep = rep[1:]

    radic = mpf(radic)

    rep = [mpf(int(u, 36)) for u in rep.split(',')]
    num = mpf(0)
    for u in rep:
        num = num * radic
        num = ceil(num + u)

    return int(num * S)

# Example usage
encoded = irradix(12345)
decoded = derradix(encoded)

print("Encoded:", encoded)
print("Decoded:", decoded)

