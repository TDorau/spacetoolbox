import numpy
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import cProfile

def area_to_mach(x_pos, radius_local):
    r"""
        Calculates the local mach number from a given axial position and local area input (in terms of its
        corresponding radius) using quasi-one dimensional (Q1D) gas flow theory.
        This code can be used, for example, to verify nozzle data by comparing simulated results
        with the analytical Q1D flow solution.

        | For more details:
        | [1] Modern Compressible Flow - Chapter 5 "Quasi-One-Dimensional Flow", J.D. Anderson
        | [2] Compressible Flow in a Nozzle, ANSYS Innovation Course.
              courses.ansys.com/index.php/courses/compressible-flow-in-a-nozzle/

        It uses the following mathematical relation, the area mach relation:
        (LateX equation)
        \left( \frac{A}{A^*} \right)^2=\frac{1}{M^2}\left[ \frac{2}{\gamma+1}\left( 1+\frac{\gamma-1}{2}M^2 \right)
        \right]^\frac{\gamma+1}{\gamma-1}

        Output values can be verified using the Appendix A in [1].

        Returns
        a mach number value corresponding to the given local area's radius.
    """
    gamma = 1.4
    radius_throat = 4.3263
    tolerance = 0.000001
    lower_limit = 1 - tolerance
    upper_limit = 1 + tolerance
    decimals = 5

    # initial values for the numerical approximation
    mach_no = 1
    step_size = -0.1
    supersonic = False

    # check if the input is valid
    if radius_local < radius_throat:
        raise Exception("Input must be >= than {}".format(radius_throat))

    # check if the local area position is upstream (negative x_pos; subsonic and convergent)
    # or downstream (positive x_pos; supersonic and divergent) from the throat
    # the x axis origin lies on the throat
    if x_pos < 0:
        supersonic = False
    else:
        supersonic = True

    # local area ratio (=squared local radius ratio) is the local area divided by the throat area
    local_area_ratio = (radius_local ** 2) / (radius_throat ** 2)

    # left side "ls" of the area-mach relation equation
    ls = local_area_ratio**2

    # right side "rs" of the area-mach relation equation
    rs = (1 / mach_no ** 2) * (2 * (1 + ((gamma - 1) * mach_no ** 2) / 2) / (gamma + 1)) ** ((gamma + 1)/(gamma - 1))

    i = rs / ls
    # following, a while loop that compares the right side and the left side,
    # when the ratio rs/ls != 1 (within a specified tolerance, e.g. 1%), the mach number mach_no is changed
    # this is iterated until the corresponding mach number is found

    # check if both sides of the equation match within the given tolerance
    # First check the trivial case where the local_area_ratio=1 (at the throat. x_pos=0)
    if i > lower_limit and i < upper_limit:
        print(mach_no)
        return mach_no

    # second, check if the flow is subsonic, find the corresponding Mach number numerically
    # this method guesses a Mach_number and refines the guess with each iteration.
    elif not supersonic:
        while i < lower_limit or i > upper_limit:
            while i > upper_limit:
                mach_no = mach_no + step_size
                rs = (1 / mach_no ** 2) * (2 * (1 + ((gamma - 1) * mach_no ** 2) / 2) / (gamma + 1)) ** (
                        (gamma + 1) / (gamma - 1))
                i = rs / ls
                if i < lower_limit:
                    step_size = step_size * -0.1
            while i < lower_limit:
                mach_no = mach_no + step_size
                rs = (1 / mach_no ** 2) * (2 * (1 + ((gamma - 1) * mach_no ** 2) / 2) / (gamma + 1)) ** (
                        (gamma + 1) / (gamma - 1))
                i = rs / ls
                if i > upper_limit:
                    step_size = step_size * -0.1

        else:
            mach_no = np.around(mach_no, decimals=5)
            print(mach_no)
            return mach_no
    elif supersonic:
        step_size = step_size*-1
        while i < lower_limit or i > upper_limit:
            while i < lower_limit:
                mach_no = mach_no + step_size
                rs = (1 / mach_no ** 2) * (2 * (1 + ((gamma - 1) * mach_no ** 2) / 2) / (gamma + 1)) ** (
                        (gamma + 1) / (gamma - 1))
                i = rs / ls
                if i > upper_limit:
                    step_size = step_size * -0.1
            while i > upper_limit:
                mach_no = mach_no + step_size
                rs = (1 / mach_no ** 2) * (2 * (1 + ((gamma - 1) * mach_no ** 2) / 2) / (gamma + 1)) ** (
                        (gamma + 1) / (gamma - 1))
                i = rs / ls
                if i < lower_limit:
                    step_size = step_size * -0.1
        else:
            mach_no = np.around(mach_no, decimals=5)
            print(mach_no)
            return mach_no

#test run
area_to_mach(0, 4.3263)

