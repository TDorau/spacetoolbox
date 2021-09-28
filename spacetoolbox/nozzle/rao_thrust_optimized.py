import math
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def calculate_parabolic(radius_throat, area_ratio, theta_i, 
                        theta_exit, percent_length_conical):
    r"""
    Calculates a bell nozzle according to Rao thrust-optimized parabolic
    approach. Rao applied the Method of characteristics to determine bell 
    nozzle contours. He later found out that a parabola is a good 
    approximation for the bell-shaped contour curve.

    | For more details: 
    | [1] Sutton - Rocket Propulsion elements - Nozzle configurations
    | [2] Rao - Exhaust Nozzle Contour for Optimum Thrust
    | [3] Kulhanek -  Design Analysis And Simulation of Rocket Propulsion System
    | [4] Agrawal - Parametric Output of Penetraition Length in De-Laval Nozzle using CFD

    Typical values of the parameters can be found in [1]. The calculation
    requires two angles. The infliction angle :math:`{\theta}_i` and the
    exit angle :math:`{\theta}_e` visible in Figure 1. 
    
    .. figure:: /images/Sutton_RaoBellNozzle.jpg
       :width: 600
       :align: center
       :alt: Image not available - please report

    Figure 1: Definition of geometric parameters

    The length of the nozzle L is defined as:

    .. math::
        L = \frac{k\left(\sqrt{\varepsilon - 1}\right)r_t}{tan(\theta_e)}

    where :math:`r_t` is the throat radius, k is the length percentage of an
    equivilant cone nozzle with 15° half angle and :math:`\varepsilon` is the
    nozzle expansion ratio. The nozzle geometry consists of three separate
    curves. The coordinates of the first convergent curve (index fc) are 
    determined by the following formulas:

    .. math::
        \begin{eqnarray}
            x_{fc} &=& cos(\theta_{fc})\cdot 1.5 \cdot r_t \\
            y_{fc} &=& sin(\theta_{fc})\cdot 1.5 \cdot r_t + (1.5 \cdot r_t + r_t)
        \end{eqnarray}

    Both equations are solved at a number of different angles :math:`{\theta}_{fc}` 
    that are determined with the help of a defined step size. Decreasing the
    step size increases the number of points in each curve. The second divergent
    curve (sc) is defined as:

    .. math::
        \begin{eqnarray}
            x_{sc} &=& cos(\theta_{sc})\cdot 0.382 \cdot r_t \\
            y_{sc} &=& sin(\theta_{sc})\cdot 0.382 \cdot r_t + (0.382 \cdot r_t + r_t)
        \end{eqnarray}

    The third curve (tc) is defined by a parabolic curve equation.

    .. math::
        \begin{eqnarray}
            x_{tc} &=& ay^2 + by + c \\
            y_{tc} &=& \sqrt{\varepsilon}r_t
        \end{eqnarray}

    The coefficients of the parabolic equations are solved by a matrix equation.
    To solve the equation, the coordinates of the endpoints (ep) of the second
    and third curve are needed.

    .. math::
        \begin{bmatrix}
            y_{sc,ep}^2 & y_{sc,ep} & 1 \\ 
            y_{tc,ep}^2 & y_{tc,ep} & 1 \\ 
            2y_{sc,ep} & 1 & 0
        \end{bmatrix}^{-1} 
        \cdot
        \begin{bmatrix}
            x_{sc,ep}\\
            x_{tc,ep}\\
            1 / tan(\theta_i)
        \end{bmatrix}^{-1}     
        =  
        \begin{bmatrix}
            a\\
            b\\
            c
        \end{bmatrix}^{-1}    

    Args:
        radius_throat (float): throat radius :math:`r_t`
        area_ratio (float):  Ratio of exit area to throat area :math:`\varepsilon`
        theta_exit (float): final parabola angle (see Fig. 1) :math:`{\theta}_e`
        theta_i (float): infliction / diverngence angle, where divergent curve 
            and parabolic curve intersect typically 20-50°, right downstream of
            the nozzle throat (see Fig. 1) :math:`{\theta}_i`
        percent_length_conical (float): length percentage of equivilant conical 
            nozzle e.g. a 80% bell nozzle has a length that is 20% shorter 
            than a comparable 15° cone half angle nozzle of the same area 
            ratio (see Fig. 1)
            
    Returns:
        CSV-File and Graph containing the nozzle x and y coordinates

    """

    # First curve (fc)
    length_nozzle = percent_length_conical * (math.sqrt(area_ratio) - 1) \
                    * radius_throat / math.tan(15 * math.pi / 180)

    angle_fc =  -(math.pi + (45 * math.pi / 180))
    N_STEPS_FC = 300
    step_fc = (-math.pi / 2 - angle_fc) / N_STEPS_FC
    theta_fc = np.arange(-3 / 4 * math.pi, -math.pi / 2 + 0.001, step_fc)

    x_fc = np.cos(theta_fc) * 1.5 * radius_throat
    y_fc = np.sin(theta_fc) * 1.5 * radius_throat + (1.5 * radius_throat
           + radius_throat)

    # np.savetxt('firstCurve.csv', (x_fc, y_fc), delimiter=";")

    # Second curve (sc)
    angle_sc = -math.pi / 2
    N_STEPS_SC = 300
    step_sc = theta_i / N_STEPS_SC
    theta_sc = np.arange(angle_sc, theta_i - math.pi / 2 + step_sc, step_sc)

    x_sc = np.cos(theta_sc) * 0.382 * radius_throat
    y_sc = np.sin(theta_sc) * 0.382 * radius_throat + (0.382 * radius_throat
           + radius_throat)

    # np.savetxt('secondCurve.csv', (x_sc, y_sc), delimiter=";")

    # Third curve (tc)
    x_sc_endpoint = math.cos(theta_i - math.pi / 2) * 0.382 * radius_throat
    y_sc_endpoint = math.sin(theta_i - math.pi / 2) * 0.382 * radius_throat \
           + (0.382 * radius_throat + radius_throat)

    y_exit = math.sqrt(area_ratio) * radius_throat

    matrix_y = np.array([[y_sc_endpoint ** 2, y_sc_endpoint, 1], 
                         [y_exit ** 2, y_exit, 1],
                         [2 * y_sc_endpoint, 1, 0]])
    matrix_x = np.array([x_sc_endpoint, length_nozzle, 1 / math.tan(theta_i)])
    inverse_matrix_y = np.linalg.inv(matrix_y)
    parabola_coefficients = inverse_matrix_y.dot(matrix_x) 

    coefficient_a = parabola_coefficients[0]
    coefficient_b = parabola_coefficients[1]
    coefficient_c = parabola_coefficients[2]

    STEPSIZE_Y_TC = 0.001
    y_tc = np.arange(y_sc_endpoint, y_exit + STEPSIZE_Y_TC, STEPSIZE_Y_TC)
    x_tc = coefficient_a * y_tc**2 + coefficient_b * y_tc + coefficient_c

    # np.savetxt('thirdCurve.csv', (x_tc, y_tc), delimiter=";")

    x_nozzle = np.concatenate((x_fc,x_sc, x_tc),axis=0)
    y_nozzle = np.concatenate((y_fc,y_sc, y_tc),axis=0)

    np.savetxt('rao_thrust_optimized_parabola.csv',
              (x_nozzle, y_nozzle), delimiter=";")

    export_parabolic(x_nozzle, y_nozzle)

    plot_parabolic(x_nozzle, y_nozzle, radius_throat, area_ratio, theta_i,
                     theta_exit, x_sc_endpoint, y_sc_endpoint, y_exit,
                     length_nozzle, x_fc)

    return length_nozzle


# Add plot function
def plot_parabolic(x_nozzle, y_nozzle, radius_throat, theta_i, theta_exit, 
                   x_sc_endpoint, y_sc_endpoint, y_exit, length_nozzle):
    r"""Exports the Rao thrust optimized parabolic nozzle as png image

    Args:
        x_nozzle (numpy.array): x-coordinates of nozzle contour 
            (along nozzle axis)
        y_nozzle (numpy.array):  y-Coordinates of nozzle contour 
            (radius of nozzle)
        radius_throat: throat radius :math:`r_t`
        theta_i: infliction / diverngence angle, where divergent curve and 
            parabolic curve intersect typically 20-50°, right downstream of 
            the nozzle throat (see Fig. 1) :math:`{\theta}_i`
        theta_exit: final parabola angle (see Fig. 1) :math:`{\theta}_e`
        x_sc_endpoint: x-Coordinate of second curve end point
        y_sc_endpoint: y-Coordinate of second curve end point
        y_exit: y-Coordinate of third curve end point, same as exit radius
            
    Returns:
        Exports a png nozzle of the rao parabolic nozzle geometry

    """
    negative_y_nozzle = -1 * y_nozzle
    fig = plt.figure()

    # Plot definition
    ax = fig.add_subplot(111)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.plot(x_nozzle, y_nozzle, color="dodgerblue")
    ax.plot(x_nozzle, negative_y_nozzle, color="dodgerblue")
    plt.xlabel('x-Coordinate in mm')
    plt.ylabel('y-Coordinate in mm')
    fig.tight_layout()
    plt.axis('scaled')

    # Annotations and Arrows
    plt.arrow(0, 0, length_nozzle, 0, length_includes_head=True,
          head_width=0.15, head_length=0.3)
    nozzle_length_annotation = r'$L_n$ = ' + str(round(length_nozzle, 1)) \
                               + ' mm'
    plt.annotate(nozzle_length_annotation, xy=(length_nozzle / 2, 0.15),
                   ha='center')
    plt.arrow(0, 0, 0, radius_throat, length_includes_head=True,
          head_width=0.15, head_length=0.3)
    throat_radius_annotation = r'$r_t$ = ' + str(radius_throat) + ' mm'
    plt.annotate(throat_radius_annotation, xy=(0.15, radius_throat / 2),
                   ha='left')
    plt.arrow(length_nozzle, 0, 0, y_exit, 
            length_includes_head=True, head_width=0.15, head_length=0.3)
    exit_radius_annotation = r'$r_e$ = ' + str(y_exit) + ' mm'
    plt.annotate(exit_radius_annotation, xy=(length_nozzle - 0.15, y_exit / 2),
                   ha='right')
    theta_e_annotation =  r'$\theta_e$ = ' + str(round(theta_exit * 180 
                          / math.pi, 1)) + '°'
    plt.annotate(theta_e_annotation, xy=(length_nozzle - 0.15, y_exit + 
                 0.15), ha='center')
    plt.plot(length_nozzle, y_exit, marker='o', markersize=3,
             color="red")
    theta_i_annotation =  r'$\theta_i$ = ' + str(round(theta_i * 180 
                          / math.pi, 1)) + '°'
    plt.annotate(theta_i_annotation, xy=(x_sc_endpoint + 0.5, 
                 y_sc_endpoint), ha='left')
    plt.plot(x_sc_endpoint, y_sc_endpoint, marker='o', markersize=3,
             color="red")

    plt.savefig('rao_thrust_optimized_parabola.png')


# Add export
def export_parabolic(x_nozzle, y_nozzle):
    r"""Exports the Rao thrust optimized parabolic nozzle in the current directory

    Args:
        x_nozzle (numpy.array): x-coordinates of nozzle contour 
            (along nozzle axis)
        y_nozzle (numpy.array):  y-Coordinates of nozzle contour (radius of 
            nozzle)
            
    Returns:
        CSV-Export of nozzle x and y coordinates

    """
    df = pd.DataFrame({"x_nozzle" : x_nozzle, "y_nozzle" : y_nozzle})
    print(df)
    df.to_csv("rao_thrust_optimized_parabola.csv", index=False)

    return df

# Verification: Sutton Table 3-4 "Data on Several Bell-Shaped nozzles"
# Case: 80% Bell contour, area ratio 10

radius_throat = 1
area_ratio = 25
theta_exit = 8.5 * math.pi / 180
theta_i = 30 * math.pi / 180
percent_length_conical = 0.8

print(calculate_parabolic(radius_throat, area_ratio, theta_i, 
                                     theta_exit, 
                                     percent_length_conical))


