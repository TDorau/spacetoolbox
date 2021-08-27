import math

def rao_thrust_optimized(radius_throat, area_ratio, theta, theta_exit, theta_n, gamma):
    r"""Calculates a bell nozzle according to Rao Thrust optimized parabolic approach

    .. math::
        C_F =  \sqrt{\frac{2\gamma^2}{\gamma-1}\left(\frac{2}{\gamma+1}\right)^{\frac{\gamma+1}{\gamma-1}}
                \left[1-\frac{p_e}{p_c}\right]^{\frac{\gamma-1}{\gamma}}} 
                + \left(\frac{p_e-p_a}{p_c}\right)\frac{A_e}{A_t}

    Args:
        radius_throat (float): Heat capacity ratio
        area_ratio (float):  
        theta (float): 
        theta_exit (float): 
        theta_n (float): 
        gamma (float): 

    Returns:
        Rao bell nozzle contour

    """

    ideal_thrust_coefficient = math.sqrt(2 * gamma**2 / (gamma - 1)*(2
                               / (gamma + 1))**((gamma + 1)/(gamma - 1))
                               * (1 - (pressure_exit / pressure_total)**((gamma
                               - 1) / gamma))) + ((pressure_exit - pressure_atmos)
                               / pressure_total) * area_ratio
                                
    return ideal_thrust_coefficient


radius_throat = 30.5
area_ratio = 31.4754
theta = 50
theta_exit = 16.5
theta_n = theta * math.pi / 180
gamma = 0.8
