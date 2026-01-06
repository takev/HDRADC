

def calculate_gain(Rsw, Rout, ladder, index):
    Rg = 1 / ladder[0]
    if (index >> 0) & 1:
        Rg += 1 / (ladder[1] + Rsw)
    Rg = 1 / Rg

    Rf = 1 / ladder[2]
    if (index >> 1) & 1:
        Rf += 1 / (ladder[3] + Rsw)
    if (index >> 2) & 1:
        Rf += 1 / (ladder[4] + Rsw)
    if (index >> 3) & 1:
        Rf += 1 / (ladder[5] + Rsw)
    Rf = 1 / Rf

    return (Rout + Rf) / Rg


def calculate_gains(Rsw, Rout, ladder):
    """
    @param resistances A list of resistance values, the last is fixed the rest is switched.
    """
    r = []

    for index in range(2 ** 4):
        r.append((calculate_gain(Rsw, Rout, ladder, index), index))

    return r

def match(expected_gains, gain_results, print_this = False):
    eg = expected_gains[:]
    for gain, switch_state in gain_results:
        for i in range(len(eg)):
            value, error = eg[i]
            if gain >= (value - value*error) and gain <= (value + value*error):
                del eg[i]
                if print_this:
                    print(switch_state, gain, value)
                break

    return len(eg) == 0

def test(expected_gains, Rsw, Rout, ladder):
   gain_results = calculate_gains(Rsw, Rout, ladder) 
   if match(expected_gains, gain_results):
       print(ladder)
       match(expected_gains, gain_results, True)



Rout = 0
Rsw = 2

expected_gains = [
    (16.0, 0.5),     # Microphone cascade (low)
    (4.0, 0.5),     # Microphone cascade (low)
    (1.0, 0.5),    # Unity, 10 dBv
    #(0.161, 0.05),  # Pro +24dBu
    (0.250, 0.5),  # Pro +20dBu
]

# Common resistances array values
various_resistances = [
    100,
    200,
    250,
    300,
    400,
    500,
    600,
    750,
    800,
    900,
    1000,
    1500,
    2000,
    2500,
    4000,
    5000,
    6000,
    8000,
    10000,
]

for i in range(len(various_resistances)):
    for j in range(i, len(various_resistances)):
        for k in range(len(various_resistances)):
            for l in range(k, len(various_resistances)):
                for m in range(l, len(various_resistances)):
                    for n in range(m, len(various_resistances)):
                        r0 = various_resistances[i]
                        r1 = various_resistances[j]
                        r2 = various_resistances[k]
                        r3 = various_resistances[l]
                        r4 = various_resistances[m]
                        r5 = various_resistances[n]
                        test(expected_gains, Rsw, Rout, [r0, r1, r2, r3, r4, r5])

