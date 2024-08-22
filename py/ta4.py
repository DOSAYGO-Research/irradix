from mpmath import mp, mpf, sqrt
import matplotlib.pyplot as plt

# Initialize global variables for BigPHI
mp.dps = 100
_bigphi_value = (mpf(1) + sqrt(mpf(5))) / 2

def get_bigphi():
    return _bigphi_value

VALS = {
    'BigPHI': get_bigphi,
}

def irradix(num):
    num = mpf(num)
    S = mp.sign(num)
    if S == -1:
        num = num * S
    w = [num, 0]
    r = []
    bigphi = VALS['BigPHI']()
    while num > 0:
        w[1] = w[0] % bigphi
        if w[1] < 0:
            w[1] = w[1] - bigphi
        w[0] = (w[0] - w[1]) / bigphi
        unit = int(w[1])
        r.insert(0, str(unit))
        w[0] = int(w[0])
    return ''.join(r)

def test_irradix_binary_equivalence():
    max_num = 1000
    original_nums = []
    irradix_nums = []
    binary_as_irradix_nums = []

    for i in range(1, max_num + 1):
        irradix_rep = irradix(i)
        binary_interpretation = int(irradix_rep, 2)
        original_nums.append(i)
        irradix_nums.append(irradix_rep)
        binary_as_irradix_nums.append(binary_interpretation)

    plt.figure(figsize=(10, 5))
    plt.plot(original_nums, binary_as_irradix_nums, label="Binary interpreted as Base-2", marker='o')
    plt.plot(original_nums, original_nums, label="Original", linestyle='--')
    plt.xlabel("Original Integer")
    plt.ylabel("Interpreted as Binary")
    plt.title("Base-φ Representation Interpreted as Binary")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_irradix_binary_equivalence()

