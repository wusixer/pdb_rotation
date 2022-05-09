'''Script to rotate and translate a pdb file, needed to evaluate equidock https://github.com/octavian-ganea/equidock_public'''

from biopandas.pdb import PandasPdb
import numpy as np
from math import sin, cos
import argparse

# define rotation and translation
translation = [60, 20, 44]


def rotate_translate_pdb(input_pdb:str, rotation_angle:int, out_file_pdb:str):
    """
    Rotate a pdb file with user defined angle in along x, y, z coords and move it
    along x, y, z coords. The rotated and tranformed file is then save to a new file

    Args:
        input_pdb (str): input pdb full path
        rotation_angle (int): rotation angel, can be of range -180 to 180
        out_file_pdb (str): output pdb full path

    Returns:
        str: execution status
    """

    rotation_matrix =np.array([[cos(rotation_angle), 0, sin(rotation_angle)],
                               [  0,     1,   0.   ],
                               [-sin(rotation_angle), 0, cos(rotation_angle)]])

    pdb_file = PandasPdb().read_pdb(input_pdb)

    # rotate each 
    pdb_file.df['ATOM'][['x_coord', 'y_coord', 'z_coord']] = (rotation_matrix @ pdb_file.df['ATOM'][['x_coord', 'y_coord', 'z_coord']].T).T+translation

    # save to file
    pdb_file.to_pdb(path=out_file_pdb, records=['ATOM'], gz=False)
    
    return 'Done'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("-pdb", help = 'the full path of a pdb file you want to rotate')
    parser.add_argument("-rotation", type = int, help = 'angle of the rotation')
    parser.add_argument("-out", help = 'the full path the rotated pdb to be saved')

    args = parser.parse_args()
    print(f'input pdb is {args.pdb}, out put will be saved in {args.out}')

    rotate_translate_pdb(args.pdb, args.rotation, args.out)
