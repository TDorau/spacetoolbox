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
