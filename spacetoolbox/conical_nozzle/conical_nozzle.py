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
    n_steps_1 = 10
    n_steps_2 = 20
    n_steps_3 = 10
    n_steps_4 = 20
    n_steps_5 = 50
    total_steps = n_steps_1 + n_steps_3 + n_steps_2 + n_steps_4 + n_steps_5

    nozzle_coordinates = np.zeros((total_steps, 2))
    x = np.zeros(total_steps)
    y = np.zeros(total_steps)

    y_3_start = radius_throat * beta - R_con * (1 - math.cos(theta * math.pi / 180))
    x_3_start = (y_3_start - b_3) / math.tan(-theta * math.pi / 180)
    x_2_start = x_3_start - math.sin(theta * math.pi / 180)

    # First curve, the chamber wall (cw) (y = beta * radius_throat)
    x_1 = np.arange(0, n_steps_1)
    y_1 = np.ones(n_steps_1) * (beta * radius_throat)
    c1_coordinates = np.zeros((n_steps_1, 2))

    # Process data into a local 2D array
    j = 0
    while j < n_steps_1:
        c1_coordinates[j] = (x_1[j], y_1[j])
        j = j + 1

    # Process data into the global 2d array
    i = 0
    current_step_count = n_steps_1
    while i < current_step_count:
        nozzle_coordinates[i] = c1_coordinates[i]
        i = i + 1

    # Second curve, the convergent transition arc (cr)
    start_angle_2 = math.pi / 2
    end_angle_2 = (theta * math.pi / 180)
    step_2 = (start_angle_2 - end_angle_2) / n_steps_3
    theta_2 = np.arange(end_angle_2, start_angle_2, step_2)

    x_2 = np.cos(theta_2) * R_con - x_2_start
    y_2 = np.sin(theta_2) * R_con + (radius_throat * beta - R_con)
    c2_coordinates = np.zeros((n_steps_3, 2))

    # Process data into a local 2d array
    j = 0
    while j < n_steps_3:
        c2_coordinates[j] = (x_2[j], y_2[j])
        j = j + 1

    # Process data into the global 2d array
    i = n_steps_1
    j = n_steps_3 - 1
    current_step_count = current_step_count + n_steps_3
    while i < current_step_count:
        nozzle_coordinates[i] = c2_coordinates[j]
        j = j - 1
        i = i + 1

    # Third curve, the converging straight diagonal (cc)
    x_3_end = (-radius_throat * arc_factor * math.sin(theta * math.pi / 180))
    y_3_end = radius_throat * (1 + arc_factor * (1 - math.cos(theta * math.pi / 180)))
    b_3 = y_3_end - math.tan(-theta * math.pi / 180) * x_3_end

    x_3 = np.arange(x_3_start, x_3_end, (x_3_end-x_3_start) / n_steps_2)
    y_3 = x_3 * math.tan(-theta * math.pi / 180) + b_3
    c3_coordinates = np.zeros((n_steps_2, 2))

    # Process data into local 2D array
    while j < n_steps_2:
        c3_coordinates[j] = (x_3[j], y_3[j])
        j = j + 1

    j = 0
    current_step_count = current_step_count + n_steps_2
    while i < current_step_count:
        nozzle_coordinates[i] = c3_coordinates[j]
        j = j + 1
        i = i + 1

    # Fourth curve, the circular arc at the throat (ar)
    start_angle_4 = -(math.pi / 2 + (theta * math.pi / 180))
    end_angle_4 = -(math.pi / 2 - alpha * math.pi / 180)
    step_4 = (end_angle_4 - start_angle_4) / n_steps_4
    theta_4 = np.arange(start_angle_4, end_angle_2, step_4)

    x_4 = np.cos(theta_4) * radius_throat * arc_factor
    y_4 = np.sin(theta_4) * radius_throat * arc_factor + (radius_throat * (1 + arc_factor))
    c4_coordinates = np.zeros((n_steps_4, 2))

    # Process data into a local 2d array
    j = 0
    while j < n_steps_4:
        c4_coordinates[j] = (x_4[j], y_4[j])
        j = j + 1

    # Process data into the global 2d array
    j = 0
    current_step_count = current_step_count + n_steps_4
    while i < current_step_count:
        nozzle_coordinates[i] = c4_coordinates[j]
        j = j + 1
        i = i + 1

    # Fifth curve, the diverging straight diagonal (dc)
    x_5 = np.arange(0, n_steps_5)
    y_5 = np.arange(0, n_steps_5) * math.tan(alpha * math.pi / 180) + 1
    c5_coordinates = np.zeros((n_steps_5, 2))

    # Process data into a local 2d array
    j = 0
    while j < n_steps_5:
        c5_coordinates[j] = (x_5[j], y_5[j])
        j = j + 1

    # Process data into global 2d array
    j = 0
    current_step_count = current_step_count + n_steps_5
    while i < current_step_count:
        nozzle_coordinates[i] = c5_coordinates[j]
        j = j + 1
        i = i + 1


    print(nozzle_coordinates)
    np.savetxt('chamberwall.csv', nozzle_coordinates, delimiter=";")


calculate_conical_nozzle(4.3263, 4.82, 15, 50, 1.5, 3.467166, 15, 5)