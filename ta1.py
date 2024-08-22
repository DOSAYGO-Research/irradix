#!/usr/bin/env python

from mpmath import mp
import random
from irradix import irradix, derradix, set_precision

set_precision(1000)
val = mp.mpf(10)

for i in range(1000):
    basePhi = irradix(val)
    regular = derradix(basePhi)
    if regular != int(val):
        print(f"Divergence at {i+2}-digit random value.")
        vs = str(int(val))
        rs = str(int(regular))
        track = []
        diff_places = []
        for j in range(min(len(vs), len(rs))):
            if vs[j] != rs[j]:
                diff_places.append(j+1)
                track.append('^')
            else:
                track.append(' ')
        print(f"Original:  {vs}")
        print(f"Recovered: {rs}")
        print(f"           {''.join(track)}")
        print(f"Values differ at places: {diff_places}")
        input("Press Enter to continue...")  # Pause for user input
    else:
        print(f"{i+2}-digit values match: {regular}")

    digit = random.randint(0, 9)
    val *= 10
    val += digit

