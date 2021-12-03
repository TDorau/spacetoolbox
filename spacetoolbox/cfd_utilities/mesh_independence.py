import os

def calculate_representative_cell_length(file_directory):
    r"""Reads a csv with volume data entries for every cell in a CFD-mesh to 
        calculate the representative cell length according Celik et al.
        Format: 0.001
                0.002
                0.0012

    | For more details: 
    [1] Celik - Procedure for Estimation and Reporting of Uncertainty Due to
                discretization in CFD applicaitons

    Args:
        file_directory (string): Directory to file (format: "C:/temp/xxx.csv")

    Returns:
        representative cell length h

    """

    representative_cell_length = 1

    return representative_cell_length

print(calculate_representative_cell_length("C:/temp/volumedata.csv"))