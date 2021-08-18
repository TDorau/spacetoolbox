def pressure_to_pressure_total(mach, gamma):
    r"""Calculates the pressure ratio given the mach number Ma.

    .. math::
        \frac{p}{p_{t}} = \left ( 1 + \frac{\gamma -1}{2} M^2 \right )^{\frac{-\gamma}{(\gamma - 1)}}

    Args:
        mach (float): Mach number
        gamma (float): Specific heat ratio

    Returns:
        Pressure ratio

    """
    pressure_to_pressure_total = (1 + ((gamma - 1) / 2) * mach**2) ** (-gamma /
                                 (gamma - 1))

    return pressure_to_pressure_total


def temperature_to_temperature_total(mach, gamma):
    r"""Calculates the temperature ratio given the mach number Ma.

    .. math::
        \frac{T}{T_{t}} = \left ( 1 + \frac{\gamma -1}{2} M^2 \right )^{-1}

    Args:
        mach (float): Mach number
        gamma (float): Specific heat ratio

    Returns:
        Temperature ratio
    """
    temperature_to_temperature_total = (1 + ((gamma - 1) / 2) * mach**2) ** (-1)

    return temperature_to_temperature_total


def rho_to_rho_total(mach, gamma):
    r"""Calculates the density ratio given the mach number Ma.

    .. math::
        \frac{\rho}{\rho_{t}} = \left ( 1 + \frac{\gamma -1}{2} M^2 \right )
            ^{\frac{-1}{(\gamma - 1)}}

    Args:
        mach (float): Mach number
        gamma (float): Specific heat ratio

    Returns:
        Density ratio

    """
    rho_to_rho_total = (1 + ((gamma - 1) / 2) * mach**2) ** (-1 / (gamma - 1))

    return rho_to_rho_total

