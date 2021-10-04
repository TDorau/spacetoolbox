import math
import numpy as np
import random

def prandtl_meyer_function_from_angle(gamma, prandtl_meyer_angle):
    r"""Calculates the Mach number given the Prandtl-Meyer angle

    Args:
        prandtl_meyer_angle: 
            (along nozzle axis)
        gamma:  
            
    Returns:
        Mach number

    """
    N_MACH = 100000
    for i in range(1, N_MACH  + 1):
        mach = random.uniform(0, 5)

    return mach

def prandtl_meyer_function_from_mach(mach, gamma):

prandtl_meyer_function_from_angle(36, 1.4)