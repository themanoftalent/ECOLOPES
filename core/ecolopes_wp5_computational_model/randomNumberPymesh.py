#pip install ghhops_server==1.5.4 numpy==1.23.5 pandas==1.5.2 rhino3dm==7.15.0 SQLAlchemy==1.4.44


import logging
import random

from .constants import LOG_LVL, FLASK_HOSTNAME, VOX_DOC_PATH, HEVC_PATH

from .components.vox_read import *
from .components.vox_write import *

def main():
    # Generate random values for each list
    V1 = [random.randint(1, 200) for _ in range(3)]
    V2 = [random.randint(1, 200) for _ in range(3)]
    V3 = [random.randint(1, 200) for _ in range(3)]

    # Create a logger for logging messages
    logger = logging.getLogger(__name__)
    logger.setLevel(LOG_LVL)

    # Loop through each list of values and generate different pymesh shapes
    for values in [V1, V2, V3]:
        # Read the voxel data from the VOX_DOC_PATH
        voxel_data = read_vox_file(VOX_DOC_PATH)
        if voxel_data is None:
            logger.error("Voxel data not found at %s", VOX_DOC_PATH)
            continue

        # Write the voxel data to a HEVC file
        write_hevc_file(voxel_data, HEVC_PATH)

        # Loop through the values in the current list and generate pymesh shapes
        for value in values:
            # Generate the pymesh shape with the current value
            generate_pymesh_shape(value, voxel_data)

if __name__ == '__main__':
    main()
