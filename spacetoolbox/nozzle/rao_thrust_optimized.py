import math
import numpy as np

def rao_thrust_optimized_parabolic(radius_throat, area_ratio, theta_i, 
                                   theta_exit, percent_length_conical):
    r"""Calculates a bell nozzle according to Rao Thrust optimized parabolic approach
        Rao applied the Method of characteristics to determine bell nozzles. 
        He later found out that a parabola is a good approximation for the 
        bell-shaped contour curve.

        For more details: 
        - Sutton - Rocket Propulsion elements - Nozzle configurations
        - Rao - Exhaust Nozzle Contour for Optimum Thrust
        - Kulhanek -  Design Analysis And Simulation of Rocket Propulsion System

    .. math::
        C_F =  \sqrt{\frac{2\gamma^2}{\gamma-1}\left(\frac{2}{\gamma+1}\right)^{\frac{\gamma+1}{\gamma-1}}
                \left[1-\frac{p_e}{p_c}\right]^{\frac{\gamma-1}{\gamma}}} 
                + \left(\frac{p_e-p_a}{p_c}\right)\frac{A_e}{A_t}

    Insert picture p.80 Sutton Rocket propulsion elements

    Args:
        radius_throat (float): Heat capacity ratio
        area_ratio (float):  Ratio of exit area to throat area
        theta (float): 
        theta_exit (float): final parabola angle (see sketch)
        theta_i (float): infliction / diverngence angle, where divergent curve and parabolic curve intersect
            typically 20-50°, right downstream of the nozzle throat (see sketch)
        percent_length_conical (float): length percentage of equivilant conical nozzle. E.g. an 80%
            bell nozzle has a length that is 20% shorter than a comparable 15° cone half angle
            of the same area ratio (see skectch)
            
    Returns:
        Rao bell nozzle contour

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

    np.savetxt('firstCurve.csv', (x_fc, y_fc), delimiter=";")

    # Second curve (sc)
    angle_sc = -math.pi / 2
    N_STEPS_SC = 300
    step_sc = theta_i / N_STEPS_SC
    theta_sc = np.arange(angle_sc, theta_i - math.pi / 2 + step_sc, step_sc)

    x_sc = np.cos(theta_sc) * 0.382 * radius_throat
    y_sc = np.sin(theta_sc) * 0.382 * radius_throat + (0.382 * radius_throat
           + radius_throat)

    np.savetxt('secondCurve.csv', (x_sc, y_sc), delimiter=";")
                                
    return x_fc


# Verification: Sutton Table 3-4 "Data on Several Bell-Shaped nozzles"
# Case: 80% Bell contour, area ratio 10

radius_throat = 1
area_ratio = 10
theta_exit = 8.5 * math.pi / 180
theta_i = 50 * math.pi / 180
percent_length_conical = 0.8

print(rao_thrust_optimized_parabolic(radius_throat, area_ratio, theta_i, 
                                     theta_exit, 
                                     percent_length_conical))



