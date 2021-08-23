def temperature_to_temperature_total(pressure_to_pressure_total, gamma):
    r"""Calculates the temperature ratio given the mach number Ma.

    .. math::
        \frac{T}{T_{t}} = \left (\frac{p}{p_t}\right)^{\frac{gamma - 1}{gamma}}

    Args:
        pressure_to_pressure_total (float): Pressure ratio
        gamma (float): Specific heat ratio

    Returns:
        Temperature ratio
    """
    temperature_to_temperature_total = pressure_to_pressure_total ** ((gamma 
        - 1) / gamma)

    return temperature_to_temperature_total
