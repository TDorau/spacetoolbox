import math
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def calculate_rao_nozzle(radius_throat, epsilon, alpha,
                        theta, beta, l_ch, R_con):

    r"""
    Creates a rao nozzle or a "parabolic approximation of the bell nozzle" contour and exports it as a CSV file.

    "One convenient way of designing a near-optimum thrust bell nozzle contour uses the parabolic
    approximation procedures suggested by G. V. R. Rao. (...) The nozzle contour immediately upstream
    of the throat is a circular arc with a radius of 1.5 * R_t. The divergent section nozzle contour is
    made up of a circular entrance section with a radius of 0.382 R_t from the throat to the inflection point
    and parabola from there to the exit." [1]

    | For more details:
    | [1] Huzel - Modern Engineering for Design of Liquid-propellant Rocket Engines; Ch. 4

    Input parameters include:
        + the throat radius 'radius_throat'
        + the expansion ratio 'epsilon' (exit radius^2 / throat radius^2)
        + the divergent inflection angle 'theta_n'  (from 12 to 18 deg)
        + the convergent half angle 'theta' (from 20 to 45 deg)
        + the convergent arc radius factor 'arc_con' (= 1,5)
        + the divergent arc radius factor 'arc_div' (= 0.382)
        + the convergence ratio 'beta' (combustion chamber radius / throat radius)
        + combustion chamber length 'l_ch' [mm]
        + combustion chamber to convergent section transition radius 'R_con' [mm]

    The geometry or contour consists of 6 different curves:
        1. A straight line from the combustion chamber wall (c1)
        2. An circular arc transitioning to the converging straight diagonal (c2)
        3. The converging straight diagonal (c3)
        4. The throat converging circular arc (c4)
        5. The throat diverging circular arc (c5)
        6. And the diverging parabola (c6)

    The throat center is defined as the origin of the coordinate system.


    Returns:
        CSV-File and Graph containing the nozzle x and y coordinates

    """
    # parameter definition
    arc_4 = 1.5
    arc_5 = 0.382

    # setup the 2D array containing the nozzle's coordinates
    n_steps_1 = 10
    n_steps_2 = 10
    n_steps_3 = 20
    n_steps_4 = 10
    n_steps_5 = 10
    n_steps_6 = 50
    total_steps = n_steps_1 + n_steps_2 + n_steps_3 + n_steps_4 + n_steps_5 + n_steps_6 + 1

    nozzle_coordinates = np.zeros((total_steps, 2))

    


calculate_rao_nozzle(4.3263, 4.82, 15, 50, 3.467166, 8, 5)