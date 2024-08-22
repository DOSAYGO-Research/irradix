from mpmath import mp
import random

# Assume irradix, derradix, and VALS have been defined as in the previous examples
from your_module import irradix, derradix, VALS  # replace `your_module` with the actual module name

# Initialize value
val = mp.mpf(10)

for i in range(200):
    basePhi = irradix(val, VALS['BigPHI'])
    regular = derradix(basePhi, VALS['BigPHI'])
    if regular != int(val):
        print(f"Divergence at {i+2}-digit random value.")
        vs = str(int(val))
        rs = str(int(regular))
        track = []
        for j in range(min(len(vs), len(rs))):
            if vs[j] != rs[j]:
                print(f"Values differ at the {j+1}th place:")
                track.append('^')
            else:
                track.append(' ')
        print(f"Original:  {vs}")
        print(f"Recovered: {rs}")
        print(f"           {''.join(track)}")
    else:
        print(f"{i+2}-digit values match: {regular}")

    digit = random.randint(0, 9)
    val *= 10
    val += digit

