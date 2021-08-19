import math

def ideal_thrust_coefficient(gamma, pressure_total, area_ratio, pressure_exit, pressure_atmos):
    r"""Calculates the thrust coefficient as a function of heat capacity ratio, total pressure, area ratio and 
        exit pressure

    .. math::
        C_F =  \sqrt{\frac{2\gamma^2}{\gamma-1}\left(\frac{2}{\gamma+1}\right)^{\frac{\gamma+1}{\gamma-1}}
                \left[1-\frac{p_e}{p_c}\right]^{\frac{\gamma-1}{\gamma}}} 
                + \left(\frac{p_e-p_a}{p_c}\right)\frac{A_e}{A_t}

    Args:
        specific heat (float): Heat capacity ratio
        pressure_total (float): Total pressure (simplified: chamber pressure)
        area_ratio (float): Ratio of exit area to throat area
        pressure_exit (float): Pressure at the end of the nozzle
        pressure_atmos (float): Atmospheric pressure at Nozzle exit

    Returns:
        Ideal thrust coefficient

    """

    ideal_thrust_coefficient = math.sqrt(2 * gamma**2 / (gamma - 1)*(2
                               / (gamma + 1))**((gamma + 1)/(gamma - 1))
                               * (1 - (pressure_exit / pressure_total)**((gamma
                               - 1) / gamma))) + ((pressure_exit - pressure_atmos)
                               / pressure_total) * area_ratio
                                
    return ideal_thrust_coefficient
