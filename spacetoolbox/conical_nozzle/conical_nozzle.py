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
        + the expansion ratio 'epsilon' (exit radius^2 / throat radius^2)
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


    Returns:
        CSV-File and Graph containing the nozzle x and y coordinates

    """
    # setup the 2D array containing the nozzle's coordinates
    N_STEPS_CW = 10
    N_STEPS_CR = 10
    N_STEPS_CC = 20
    N_STEPS_AR = 20
    N_STEPS_DC = 50
    total_steps = N_STEPS_CW + N_STEPS_CR #+ N_STEPS_CC + N_STEPS_AR + N_STEPS_DC

    nozzle_coordinates = np.zeros((total_steps, 2))
    x = np.zeros(total_steps)
    y = np.zeros(total_steps)

    # First curve, the chamber wall (cw) (y = beta * radius_throat)
    x_cw = np.arange(0,N_STEPS_CW)
    y_cw = np.ones(N_STEPS_CW) * (beta * radius_throat)

    # Process data into the 2d array
    i = 0
    while i < N_STEPS_CW:
        x[i] = x_cw[i]
        y[i] = y_cw[i]
        nozzle_coordinates[i] = (x[i], y[i])
        i = i + 1

    # Second curve, the convergent transition arc (cr) (not working)
    angle_cr = -(math.pi + (theta * math.pi / 180))
    step_cr = (-math.pi / 2 - angle_cr) / N_STEPS_CR
    theta_cr = np.arange(math.pi / 2, math.pi * 3 / 4, step_cr)

    x_cr = np.cos(theta_cr) * R_con
    y_cr = np.sin(theta_cr) * R_con + (R_con + radius_throat * beta)


    # Process data into the 2d array
    i = N_STEPS_CW + 1
    while i < N_STEPS_CW + N_STEPS_CR:
        x[i] = x_cr[i]
        y[i] = y_cr[i]
        nozzle_coordinates[i] = (x[i], y[i])
        i = i + 1

    print(x)
    print(y)
    np.savetxt('chamberwall.csv', nozzle_coordinates, delimiter=";")


calculate_conical_nozzle(4.3263, 4.82, 15, 50, 1.5, 3.467166, 15, 5)