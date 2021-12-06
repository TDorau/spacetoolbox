import os
import pandas as pd
import numpy as np
import random

def calculate_representative_cell_length(file_location):
    r"""Reads a csv with volume data entries for every cell in a CFD-mesh to 
        calculate the representative cell length according Celik et al. Cell
        volume for each cell generated from cell_volume.c UDF. Total cell
        volume can also be derived in FLUENT -> Perform Mesh Check

        Format: 0.001
                0.002
                0.0012

    | For more details: 
    [1] Celik - Procedure for Estimation and Reporting of Uncertainty Due to
                discretization in CFD applicaitons

    Args:
        file_directory (string): Directory to file (format: "C:/temp/xxx.csv")

    Returns:
        representative cell length h in m

    """

    df = pd.read_table(file_location, header=None,
                               names=["cellvolume"])

    # Equation (1) in [1]
    total_cellvolume = df["cellvolume"].sum()
    n_cells = len(df.index)
    representative_cell_length = (1 / n_cells * total_cellvolume)** (1./3.)

    return representative_cell_length


print(calculate_representative_cell_length("C:/temp/volumedata.csv"))

def calculate_discretization_error(phi_1, phi_2, phi_3, file_location1,
                                   file_location2, file_location3):
    r"""Calculates fine-grid convergence index, extrapolated relative error,
        approximate relative error of a CFD mesh with 3 discretization steps
        and a clearly defined solution variable (drag coeffiecent, thrust or
        similar)

    | For more details: 
    [1] Celik - Procedure for Estimation and Reporting of Uncertainty Due to
                discretization in CFD applicaitons

    Args:
        phi1 : Soluation variable for fine mesh
        phi2 : Soluation variable for mid mesh
        phi3 : Soluation variable for coarse mesh
        file_location1: file location of fine mesh cell volume data 
        file_location1: file location of mid mesh cell volume data 
        file_location1: file location of coarse mesh cell volume data 
        
    Returns:
        Prints the discretization error to console

    """

    # Calculate representative cell length
    h1 = calculate_representative_cell_length(file_location1)
    h2 = calculate_representative_cell_length(file_location2)
    h3 = calculate_representative_cell_length(file_location3)

    # Check if difference between meshes is large enough
    grad_refinement_factor = h3 / h1 
    if (grad_refinement_factor > 1.3):
        print("Grid finement is ")
    else:
        print("Grid refinement should be revised. Diffferenz between coarse \
               and fine mesh is not large enough")

    # Calculate grid refinement factors
    r21 = h2 / h1
    r32 = h3 / h2

    # Calculate absolute difference betweeen solution variable
    epsilon_32 = phi_3 - phi_2
    epsilon_21 = phi_2 - phi_1

    # Mode of convergence
    if (epsilon_32 / epsilon_21 > 0):
        print("Monotonic convergence")
    else: 
        print("Indication of oscillatory convergence")

    s = np.sign(epsilon_32 / epsilon_21)

    # Find order of convergence p, Combine (3a) and (3b) in [1]
    N_POINTS = 10000

    for i in range(1, N_POINTS):
        p_i = random.uniform(1, 2)
        residual = 1 / np.log(r21) * np.abs(np.log(np.abs(epsilon_32 
                   / epsilon_21)) + np.log((r_21**p_i - s) 
                   / (r_32 ** p_i - s)))  - p_i
        if (residual < residual_min):
            residual_min  = residual
            p = p_i

    # Calculate the extrapolated value
    phi_21_extrapolated = (r_21 ** p * phi_1 - phi_2) / (r_21 ** p - 1)

    # Calculate the approximate relative error
    e_a_21 = np.abs((phi_1 - phi_2) / phi_1)

    # Calculate the extrapolated relative error
    e_ext_21 = np.abs((phi_21_extrapolated - phi_1) / phi_21_extrapolated)

    #Calculate the fine grid convergence index
    gci_fine_21 = (1.25 * e_a_21) / (r_21 ** p - 1)





