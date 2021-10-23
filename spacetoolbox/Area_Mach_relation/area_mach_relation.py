import numpy
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def area_to_mach(radius_local):
    r"""
        Calculates the local mach number from a given local Radius input using quasi-one dimensional gas flow theory.
        Can be used, for example, to verify nozzle data by comparing simulated results with this analytical tool.

        | For more details:
        | [1] Modern Compressible Flow - Chapter 5 "Quasi-One-Dimensional Flow", J.D. Anderson

        It uses the following mathematical relation, the area mach relation:
        (LateX equation)
        \left( \frac{A}{A^*} \right)^2=\frac{1}{M^2}\left[ \frac{2}{\gamma+1}\left( 1+\frac{\gamma-1}{2}M^2 \right)
        \right]^\frac{\gamma+1}{\gamma-1}

        Output values can be verified using the Annex in [1].

        Returns
        a mach number value corresponding to the given local area's radius.
    """
gamma = 1.4
radius_throat = 4.3263
radius_local = 1
tolerance = 0.01
mach_no = 0.001
step_size = 0.001

# local area ratio is the local area divided by the throat area
local_area_ratio = (radius_local ** 2) / (radius_throat ** 2)

# left side "ls" of the area-mach relation equation
ls = local_area_ratio**2

# right side "rs" of the area-mach relation equation
rs = (1/mach_no**2)*(2*(1+((gamma-1)*mach_no**2)/2)/(gamma+1))**((gamma+1)/(gamma-1))

# following, a while loop that compares the right side and the left side,
# when the ratio rs/ls != 1 (within a specified tolerance, e.g. 1%), the mach number mach_no is changed
# this is iterated until the corresponding mach number is found

i = rs / ls

while i < (1 - tolerance) or i > (1 + tolerance)
    mach_no = mach_no + step_size
else:
    print(mach_no)
    return mach_no