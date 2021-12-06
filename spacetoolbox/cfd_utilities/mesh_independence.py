import os
import pandas as pd

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
    total_cellvolume = df["cellvolume"].sum()
    n_cells = len(df.index)
    representative_cell_length = (1 / n_cells * total_cellvolume)** (1./3.)

    return representative_cell_length


print(calculate_representative_cell_length("C:/temp/volumedata.csv"))