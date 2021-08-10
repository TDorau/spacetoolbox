def pressure_to_pressure_total_from_mach(mach, gamma):
    r"""Calculates the pressure ratio given the mach number Ma.
    .. math::
        \frac{p}{p_{t}} = \left ( 1 + \frac{\gamma -1}{2} M^2 \right )^{\frac{-\gamma}{(\gamma - 1)}}

    Parameters
    ----------
    mach : float
        Mach number

    gamma : float
        Specific heat ratio

    Returns
    -------
    pressure_to_pressure_total : float
        Pressure ratio   

    """
    pressure_to_pressure_total = (1 + ((gamma - 1) / 2) * mach**2) ** (-gamma /
                                 (gamma - 1))

    return pressure_to_pressure_total

