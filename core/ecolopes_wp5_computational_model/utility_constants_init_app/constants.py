#SoftAiyazilim.com
import logging
import os
import tempfile
import configparser

LOG_LVL = logging.INFO
FLASK_HOSTNAME = '127.0.0.1'

VOX_DOC_PATH = os.path.expanduser('~\Documents\HopsVoxels')
#VOX_FILENAME = 'vox_VIE_2022W_data.sqlite'
HEVC_PATH = os.path.join(tempfile.gettempdir(), 'HopsEngineVoxelCore')

for _path in [HEVC_PATH, VOX_DOC_PATH]:
    if not os.path.isdir(_path):
        os.makedirs(_path)

_config_path = os.path.join(VOX_DOC_PATH,'HopsVoxels.ini')

if not os.path.exists(_config_path):
    print(_config_path)
    with open(_config_path, 'w') as _f:
        _defaults = ['[data]', 'filename = vox_VIE_2022W_data.sqlite'] 
        _f.writelines(s + '\n' for s in _defaults)

config = configparser.ConfigParser()
config.read(_config_path)

VOX_FILENAME = config['data']['filename']

SQL_ENGINE = 'SQLite' 

if SQL_ENGINE == 'SQLite':

    SQL_GET_COLS_RAW = f"PRAGMA table_info('LVL')"
    #SQLITE_LIMIT_VARIABLE_NUMBER = 999
    #set it to 0 for other engines
    SQL_VARIABLE_LIMIT = 999
