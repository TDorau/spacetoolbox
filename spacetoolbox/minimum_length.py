import math
import numpy as np
import random
from scipy.optimize import fsolve

def prandtl_meyer_function_from_angle(gamma, prandtl_meyer_angle):
    r"""Calculates the Mach number given the Prandtl-Meyer angle

    Args:
        prandtl_meyer_angle: Prandtl meyer angle in degree 
        gamma: Heat capacity ratio 
            
    Returns:
        Mach number

    """
    N_MACH = 100000
    for i in range(1, N_MACH  + 1):
        mach = random.uniform(0, 5)
    


    return mach

def prandtl_meyer_function_solver_form(mach, gamma):
    r"""Calculates the Prandtl-Meyer angle given the mach number

    Args:
        mach: Mach number
        gamma: Heat capacity ratio 
            
    Returns:
        Prandtl-Meyer angle in radians
    """
    prandtl_meyer_angle = math.sqrt((gamma + 1) / (gamma - 1)) * \
        math.atan(math.sqrt((gamma - 1) / (gamma + 1)
        * (mach ** 2 - 1))) - math.atan(math.sqrt(mach ** 2
        - 1))

    return prandtl_meyer_angle

prandtl_meyer_function_from_angle(36, 1.4)