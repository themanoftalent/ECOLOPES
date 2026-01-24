import os

import rhino3dm
import ghhops_server as hs

from ..constants import VOX_DOC_PATH, VOX_FILENAME, SQL_GET_COLS_RAW

import numpy as np
import pandas as pd

gen_random_cubes_kwargs = {
    'rule':"/gen_random_cubes",
    'name':"GenRanCubes",
    'description':"GenRanCubes",
    #'icon':"examples/pointat.png",
    'inputs':[
        hs.HopsBoolean("Boolean", "Run", "Boolean toggle to read"),
        hs.HopsString("nr_vol", "nr_vol", "Number of volumes"),
        hs.HopsString("vol_dim", "vol_dim", "Volume dimensions -> [w,d,h]"),
        hs.HopsString("boundary_dimms", "boundary_dimms", "Boundary dimmensions -> 3D domain [formatting?]"),
        hs.HopsString("map", "map", "Exemplary map -> map name or map_name.np"),
    ],
    'outputs': [
        hs.HopsString("info", "info", "Status of the component"),
        hs.HopsString("box_prev", "box_prev", "box_prev"),
        hs.HopsPoint("vox_idx", "vox_idx", "vox_idx"),
    ]
}

def gen_random_cubes(bool, nr_vol, vol_dim, boundary_dimms, map):
  
    status = '[gen_random_cubes] '

    if bool == True:

        ##START: here comes Akif the master

        import random

        volumes = {}

        for idx, volume in enumerate(range(nr_vol)):

            #TODO: Akif implements this function that
            # places a volume in the (site) boundary
            # defined with boundary_dimms variable
            ## def place_volume_in_boundary(vol_dim):
            status += 'Volumes placed...'
            volumes[idx] = place_volume_in_boundary(vol_dim)

            #TODO: next step (1) - check against map
            # Akif implements this function that
            # checks volume position based on values inside a map
            # based on some constraint, like map_value > 2 (more than 2 sunlight hours)
            ## def check_against_map(volumes[idx], map: np.ndarray, constraint) -> bool:
        
            map_constraint = False

            while map_constraint == False:
                #TODO: Akif - if the volume does not fulfill the constraint
                # place it again and check
                is_valid_against_map = check_against_map(volumes[idx], map, constraint)
                if not is_valid_against_map == True:
                    volumes[idx] = place_volume_in_boundary(vol_dim)
                #TODO: Akif - exit this loop after xxxx iterations
                # to prevent infinite loop if constraints turns out
                # to be imposible to be met 
                else:
                    map_constraint = True

            #TODO: next step (n+1) - check against netwoerk
            # Akif implements this function that
            # checks volume position based on a network node position

            network_constraint = False
            # and so on...      

        #write that it suceeded
        status += ' Something happened...'
  
        #TODO create Rhino objects from Akif's volumes
        rh_cubes = [rhino3dm.Box(box) for box in volumes]

        #TODO create Rhino points from Akiif's volumes
        rh_points = [rhino3dm.Point(points_in_box) for points_in_box in volumes]

        ##END: here comes Akif's code used to distribute the volumes   

    #this code returns things that will be visible in Rhino
    return status, rh_cubes, rh_points