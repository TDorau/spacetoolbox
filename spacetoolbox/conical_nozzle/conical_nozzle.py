import math
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def calculate_conical_nozzle(radius_throat, epsilon, alpha,
                        theta, arc_factor, beta, l_ch, R_con):

r"""
    Creates a standard conical nozzle contour and exports it as a CSV file.

    "In early rocket-engine applications, the conical nozzle, which proved satisfactory in
    most respects, was used almost exclusively. A conical nozzle allows ease of manufacture and flexibility in
    converting an existing design to higher or lower expansion area ratio without major redesign." [1]

    In a conical nozzle, the throat section has the contour of a circular arc with a radius 'R_arc',
    ranging from 0.5 to 1.5 times the throat radius 'R_t'. The half angle of the nozzle convergent cone section
    can range from 20 to 45 degrees. The divergent cone half-angle 'alpha' varies from 12 to 18 degrees.
    The conical nozzle with a 15-deg divergent angle has become almost a standard because it is a good compromise
    on the basis of weight, length, and performance.

    | For more details:
    | [1] Huzel - Modern Engineering for Design of Liquid-propellant Rocket Engines; Ch. 4

    Input parameters include:
        + the throat radius 'radius_throat'
        + the expansion ratio 'epsilon' (exit radius / throat radius)
        + the divergent half angle 'alpha'  (from 12 to 18 deg)
        + the convergent half angle 'theta' (from 20 to 45 deg)
        + the arc radius factor 'arc_factor' ((from 0,5 to 1,5)
        + the convergence ratio 'beta' (combustion chamber radius / throat radius)
        + combustion chamber length 'l_ch' [mm]
        + combustion chamber to convergent section transition radius 'R_con' [mm]

    The geometry or contour consists of 5 different curves:
        1. A straight line from the combustion chamber wall
        2. An circular arc transitioning to the converging straight diagonal
        3. The converging straight diagonal
        4. The throat circular arc
        5. And the diverging straight diagonal

    The throat center is defined as the origin of the coordinate system.



    Figure 1: Definition of geometric parameters [1]


    Returns:
        CSV-File and Graph containing the nozzle x and y coordinates

    """
