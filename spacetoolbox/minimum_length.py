import math
import numpy as np
import random

def prandtl_meyer_function_from_angle(prandtl_meyer_angle, gamma):
    r"""Calculates the Mach number given the Prandtl-Meyer angle

    Args:
        prandtl_meyer_angle: Prandtl meyer angle in degree 
        gamma: Heat capacity ratio 
            
    Returns:
        Mach number

    """
    N_MACH = 10000
    minimum = 1
    for i in range(1, N_MACH  + 1):
        mach_i = random.uniform(1, 5)
        prandtl_meyer_angle_radians = prandtl_meyer_angle / 180 * math.pi
        prandtl_meyer_angle_compare = prandtl_meyer_function_from_mach(mach_i, 
                                          gamma)
        delta_prandtl_meyer_angle = abs(prandtl_meyer_angle_radians \
                                    - prandtl_meyer_angle_compare)
        if delta_prandtl_meyer_angle < minimum:
            mach = mach_i
            minimum = delta_prandtl_meyer_angle

    return mach

def prandtl_meyer_function_from_mach(mach, gamma):
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
