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
        1. A straight line from the combustion chamber wall (cw)
        2. An circular arc transitioning to the converging straight diagonal (cr)
        3. The converging straight diagonal (cc)
        4. The throat circular arc (ar)
        5. And the diverging straight diagonal (dc)

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
    total_steps = N_STEPS_CW + N_STEPS_CR + N_STEPS_CC + N_STEPS_AR + N_STEPS_DC

    nozzle_coordinates = np.zeros((total_steps, 2))
    x = np.zeros(total_steps)
    y = np.zeros(total_steps)

    # First curve, the chamber wall (cw) (y = beta * radius_throat)
    x_cw = np.arange(0, N_STEPS_CW)
    y_cw = np.ones(N_STEPS_CW) * (beta * radius_throat)
    cw_coordinates = np.zeros((N_STEPS_CW, 2))

    # Process data into a local 2D array
    j = 0
    while j < N_STEPS_CW:
        cw_coordinates[j] = (x_cw[j], y_cw[j])
        j = j + 1

    # Process data into the global 2d array
    i = 0
    current_step_count = N_STEPS_CW
    while i < current_step_count:
        nozzle_coordinates[i] = cw_coordinates[i]
        i = i + 1

    # Second curve, the convergent transition arc (cr)
    start_angle_cr = math.pi / 2
    end_angle_cr = (theta * math.pi / 180)
    step_cr = (start_angle_cr - end_angle_cr) / N_STEPS_CR
    theta_cr = np.arange(end_angle_cr, start_angle_cr, step_cr)

    x_cr = np.cos(theta_cr) * R_con
    y_cr = np.sin(theta_cr) * R_con + (radius_throat * beta - R_con)
    cr_coordinates = np.zeros((N_STEPS_CR, 2))

    # Process data into a local 2d array
    j = 0
    while j < N_STEPS_CR:
        cr_coordinates[j] = (x_cr[j], y_cr[j])
        j = j + 1

    # Process data into the global 2d array
    i = N_STEPS_CW
    j = N_STEPS_CR - 1
    current_step_count = current_step_count + N_STEPS_CR
    while i < current_step_count:
        nozzle_coordinates[i] = cr_coordinates[j]
        j = j - 1
        i = i + 1

    # Third curve, the converging straight diagonal (cc)
    x_cc_end = (-radius_throat * arc_factor * math.sin(theta * math.pi / 180))
    y_cc_end = radius_throat * (1 + arc_factor * (1 - math.cos(theta * math.pi / 180)))
    b_3 = y_cc_end - math.tan(-theta * math.pi / 180) * x_cc_end
    y_cc_start = radius_throat * beta - R_con * (1 - math.cos(theta * math.pi / 180))
    x_cc_start = (y_cc_start - b_3) / math.tan(-theta * math.pi / 180)
    x_cc = np.arange(x_cc_start, x_cc_end, (x_cc_end-x_cc_start)/N_STEPS_CC)
    y_cc = x_cc * math.tan(-theta * math.pi / 180) + b_3
    cc_coordinates = np.zeros((N_STEPS_CC, 2))

    # Process data into local 2D array
    while j < N_STEPS_CC:
        cc_coordinates[j] = (x_cc[j], y_cc[j])
        j = j + 1

    j = 0
    current_step_count = current_step_count + N_STEPS_CC
    while i < current_step_count:
        nozzle_coordinates[i] = cc_coordinates[j]
        j = j + 1
        i = i + 1

    # Fourth curve, the circular arc at the throat (ar)
    start_angle_ar = -(math.pi / 2 + (theta * math.pi / 180))
    end_angle_ar = -(math.pi / 2 - alpha * math.pi / 180)
    step_ar = (end_angle_ar - start_angle_ar) / N_STEPS_AR
    theta_ar = np.arange(start_angle_ar, end_angle_cr, step_ar)

    x_ar = np.cos(theta_ar) * radius_throat * arc_factor
    y_ar = np.sin(theta_ar) * radius_throat * arc_factor + (radius_throat * (1 + arc_factor))
    ar_coordinates = np.zeros((N_STEPS_AR, 2))

    # Process data into a local 2d array
    j = 0
    while j < N_STEPS_AR:
        ar_coordinates[j] = (x_ar[j], y_ar[j])
        j = j + 1

    # Process data into the global 2d array
    j = 0
    current_step_count = current_step_count + N_STEPS_AR
    while i < current_step_count:
        nozzle_coordinates[i] = ar_coordinates[j]
        j = j + 1
        i = i + 1

    # Fifth curve, the diverging straight diagonal (dc)
    x_dc = np.arange(0, N_STEPS_DC)
    y_dc = np.arange(0, N_STEPS_DC) * math.tan(alpha * math.pi / 180) + 1
    dc_coordinates = np.zeros((N_STEPS_DC, 2))

    # Process data into a local 2d array
    j = 0
    while j < N_STEPS_DC:
        dc_coordinates[j] = (x_dc[j], y_dc[j])
        j = j + 1

    # Process data into global 2d array
    j = 0
    current_step_count = current_step_count + N_STEPS_DC
    while i < current_step_count:
        nozzle_coordinates[i] = dc_coordinates[j]
        j = j + 1
        i = i + 1


    print(nozzle_coordinates)
    np.savetxt('chamberwall.csv', nozzle_coordinates, delimiter=";")


calculate_conical_nozzle(4.3263, 4.82, 15, 50, 1.5, 3.467166, 15, 5)