import os

#from flask import Flask, render_template
#from flask.logging import default_handler

import rhino3dm
import ghhops_server as hs

from ..constants import VOX_DOC_PATH, VOX_FILENAME, SQL_GET_COLS_RAW

import numpy as np
import pandas as pd
import sqlalchemy as sqla

from sqlalchemy import Table
from sqlalchemy.orm import load_only

#sqla.Table
#sqla.orm.load_only
#sqla.orm.Session

# Those are for SQL inserts...
#from sqlalchemy.orm import Session
#from sqlalchemy.dialects.sqlite import insert as sqlite_upsert
#from sqlalchemy import insert


#TODO: reading with WHERE statement...
#TODO: how to make is "user safe"?
#TODO: maybe having a list to choose from (reuse vox_list_data_layers)
#TODO: and make a list of logic operators
#TODO: component to turn the 2 above into SQL statement + execute it

vox_list_kwargs = {
    'rule':"/vox_list",
    'name':"VoxListName",
    'description':"VoxListDesc",
    #'icon':"examples/pointat.png",
    'inputs':[
        hs.HopsBoolean("Boolean", "Run", "Boolean toggle to read"),
    ],
    'outputs': [
        hs.HopsString("info", "info", "Status of the component"),
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
    ]
}

def vox_list(bool):

    #TODO: How do we check for the 'vox_meta' table (and whats inside)
    # wait...
    # here we check if there is a key in 'vox_meta' for each lvel in the list and return only those that have metadata


    status = '[vox_list] '

    #TODO: db_uri, engine and metadata_obj to ..database_helpers
    # from ..database_helpers import db_uri, engine and metadata_obj


    db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'

    engine = sqla.create_engine(db_uri)
    metadata_obj = sqla.MetaData()

    try:
        vox_meta_table = sqla.Table("vox_meta", metadata_obj, autoload_with=engine)
    except sqla.exc.NoSuchTableError as e:
        status += '[Error] vox_meta table does not exist, resolution and offsets unknown'
        return status, ['check the status output']

    #TODO: I don'know, see if it's better to work with Sessions instead of engine.connect()
    # e.g. with Session(engine) as session: session.execute() session.commit()

    print(vox_meta_table)

    _sel = vox_meta_table.select() #_sel -> stmt

    #with sqla.orm.Session(engine) as session:
    #     for row in session.execute(stmt):
    #         print(row)

    
    #with sqla.orm.Session(engine) as session:

        #statement = sqla.select(User).filter_by(name="ed")

        # list of ``User`` objects
        #user_obj = session.scalars(statement).all()

        # query for individual columns
        #statement = sqla.select(User.name, User.fullname)

        # list of Row objects
        #rows = session.execute(statement).all()


    conn = engine.connect()
    vox_meta_df = pd.DataFrame.from_records(conn.execute(_sel).fetchall(), columns = [c.name for c in vox_meta_table.columns])

    status += f'{len(vox_meta_df["name"])} voxel levels available'

    return status, vox_meta_df['name'].to_list()#, vox_lvl_dct['res'], vox_lvl_dct['x_off'], vox_lvl_dct['y_off']


vox_read_meta_kwargs = {
    'rule':"/vox_read_meta",
    'name':"VoxReadMeta",
    'description':"VoxReadMetaDesc",
    #icon="examples/pointat.png",
    'inputs':[
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Voxel level name from the /vox_list component"),
    ],
    'outputs':[
        hs.HopsString("info", "info", "Status of the component"),
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        hs.HopsNumber("Resolution", "res", "Voxel resolution"),
        hs.HopsVector("Local offset", "loc_off", "Local offset"),
        hs.HopsVector("Global offset", "glob_off", "Global offset"),
    ]
}

def vox_read_meta(vox_lvl_name):

    #TODO: Exceptions: table does not exist, table empty etc.
    #TODO: return the level 2D extent -> [new component] to load data in parallel eg. in 4 threads

    #global VOX_DOC_PATH
    #global VOX_FILENAME

    status = '[vox_read_meta] '

    db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'
    engine = sqla.create_engine(db_uri)
    metadata_obj = sqla.MetaData()
    try:
        vox_meta_table = sqla.Table("vox_meta", metadata_obj, autoload_with=engine)
    except sqla.exc.NoSuchTableError as e:
        status += '[Error] vox_meta table does not exist, resolution and offsets unknown'
        return status, ['check the status output']

    conn = engine.connect()
    _sel = vox_meta_table.select().where(vox_meta_table.c.name==vox_lvl_name)
    vox_meta_df = pd.DataFrame.from_records(conn.execute(_sel).fetchall(),
                                            columns = [c.name for c in vox_meta_table.columns])

    status += f'Metadata for {vox_lvl_name} read'

    #Dirty trick because Hops vectors need to have the Z dimmension...
    vox_meta_df['zeros'] = 0

    loc_offs_data = vox_meta_df[['x_off','y_off', 'zeros']].to_numpy()
    loc_off_obj = [rhino3dm.Vector3f(*item) for item in tuple(map(tuple, loc_offs_data))]

    geo_offs_data = vox_meta_df[['geo_x_off','geo_y_off', 'zeros']].to_numpy()
    geo_off_obj = [rhino3dm.Vector3f(*item) for item in tuple(map(tuple, geo_offs_data))]

    return status, vox_meta_df['name'].to_list(), \
                vox_meta_df['res'].to_list(), \
                loc_off_obj, \
                geo_off_obj



vox_read_rgb_kwargs = {
    'rule':"/vox_read_rgb",
    'name':"VoxReadRGB",
    'description':"VoxReadRGB",
    #'icon':"examples/pointat.png",
    'inputs':[
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        hs.HopsBoolean("Boolean", "Run", "Boolean toggle to read"),
    ],
    'outputs':[
        hs.HopsString("info", "info", "Status of the component"),
        hs.HopsString("vox_idx", "vox_idx", "vox_idx"),
        hs.HopsPoint("P", "P", "Vox points"),
        #hs.HopsNumber("vox_z_cont", "z_cont", "vox_z_cont"),
        #First is the name of output in GH
        #hs.HopsPoint("C", "C", "Colors"),
        #hs.HopsString("C", "C", "Colors"),
        hs.HopsVector("C", "C", "Colors"),
    ]
    }

def vox_read_rgb(vox_lvl, bool):
    #here implement all functionality run every time the component is executed
    #for writing data maybe we need to turn single thread in GH or somehow accumulate data here...

    #for coordinates use smallint from -32k to +32k (2 bytes)
    #for other parameters use tinyint from 0 to 255 (1 byte) 

    if not bool == True: return []

    #TODO: all the engine binding and metadata outside of the query function...
    #TODO: maybe a separate function to relad the metadata with boolean switch, but not required on canvas...
 
    #global VOX_DOC_PATH
    #global VOX_FILENAME

    #we define this once in the engine...
    db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'
    engine = sqla.create_engine(db_uri)
    metadata_obj = sqla.MetaData()

    status = '[vox_read_rgb] '

    #vox_lvl_ch = 'vox_lvl30'

    vox_lvl_table = Table(vox_lvl, metadata_obj, autoload_with=engine)
    #[c.name for c in vox_meta_table.columns]


    conn = engine.connect()

    _names = ['vox_idx', 'vox_x', 'vox_y','vox_z','red', 'green', 'blue']
    _cols = [_col for _col in vox_lvl_table.c if _col.name in _names]
    _sel = vox_lvl_table.select().with_only_columns(_cols)

    result = conn.execute(_sel)
    rows = result.fetchall()

    #why all that mess? because rhino3dm is not written to support numpy arrays...
    vox_df = pd.DataFrame.from_records(rows, columns = [c.name for c in _cols]) #[c.name for c in vox_lvl_table.columns]
    pts_data = vox_df[['vox_x','vox_y','vox_z']].to_numpy()
    col_data = vox_df[['red','green','blue']].to_numpy()
    pts_obj = [rhino3dm.Point3d(*item) for item in tuple(map(tuple, pts_data))]
    col_obj = [rhino3dm.Vector3f(*item) for item in tuple(map(tuple, col_data))]


    if len(rows) == 0:
        status += r'Voxel Engine Running, but no SQL data loaded, showing single point...'
        rows = ((0, 0, 0, 128, 128, 128),)


    else:
        status += f'Component successfully read data from: {VOX_FILENAME}'
    

    #TODO: don't return z_cont

    return status, \
           vox_df['vox_idx'].to_list(), \
           pts_obj, \
           col_obj
        #vox_df['vox_z_cont'].to_list(), \'

vox_list_data_layers_kwargs = {
    'rule':"/vox_list_data_layers",
    'name':"VoxListDataLayers",
    'description':"VoxListDataLayers Description",
    #'icon':"examples/pointat.png",
    'inputs':[
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        #hs.HopsBoolean("Boolean", "Run", "Boolean toggle to read"),
    ],
    'outputs':[
        hs.HopsString("info", "info", "Status of the component"),
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        #hs.HopsString("vox_idx", "vox_idx", "vox_idx"),
        #hs.HopsPoint("P", "P", "Vox points"),
        #hs.HopsNumber("vox_z_cont", "z_cont", "vox_z_cont"),
        #First is the name of output in GH
        #hs.HopsPoint("C", "C", "Colors"),
        hs.HopsString("data_layer", "data_layer", "Available data layers"),
        #hs.HopsVector("C", "C", "Colors"),
    ]
    }

def vox_list_data_layers(vox_lvl):
    #here implement all functionality run every time the component is executed
    #for writing data maybe we need to turn single thread in GH or somehow accumulate data here...

    #for coordinates use smallint from -32k to +32k (2 bytes)
    #for other parameters use tinyint from 0 to 255 (1 byte) 

    #if not bool == True: return []

    #TODO: all the engine binding and metadata outside of the query function...
    #TODO: maybe a separate function to relad the metadata with boolean switch, but not required on canvas...
 
    #global VOX_DOC_PATH
    #global VOX_FILENAME

    #we define this once in the engine...
    db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'
    engine = sqla.create_engine(db_uri)
    metadata_obj = sqla.MetaData()

    status = '[vox_list_data_layers] '


    #TODO: turn this into utility function...
    _cols_ord_stmt = SQL_GET_COLS_RAW.replace('LVL', f"{vox_lvl}")
    _cols_ord_que = sqla.text(_cols_ord_stmt)
    vox_lvl_cols = [item['name'] for item in engine.execute(_cols_ord_que).mappings().all()]

    reserved_layers = ['vox_idx', 'vox_x', 'vox_y', 'vox_z', 'red', 'green', 'blue']
    data_layers = [item for item in vox_lvl_cols if item not in reserved_layers]

    status += f'{len(data_layers)} data layers found' 

    return status, \
           vox_lvl, \
           data_layers \


vox_read_data_layer_kwargs = {
    'rule':"/vox_read_data_layer",
    'name':"VoxReadDataLayer",
    'description':"oxReadDataLayer Description",
    #'icon':"examples/pointat.png",
    'inputs':[
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        hs.HopsString("data_layer", "data_layer", "Select voxel data layer, e.g. slo"),
        hs.HopsBoolean("Boolean", "Run", "Boolean toggle to read"),
    ],
    'outputs':[
        hs.HopsString("info", "info", "Status of the component"),
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        hs.HopsString("vox_idx", "vox_idx", "vox_idx"),
        #hs.HopsPoint("P", "P", "Vox points"),
        hs.HopsNumber("dl_min", "dl_min", "Minimum value"),
        hs.HopsNumber("dl_max", "dl_max", "Amximum value"),
        hs.HopsNumber("data_layer", "data_layer", "Data from the data layer"),
        #First is the name of output in GH
        #hs.HopsPoint("C", "C", "Colors"),
        #hs.HopsString("C", "C", "Colors"),
        #hs.HopsVector("C", "C", "Colors"),
    ]
    }

def vox_read_data_layer(vox_lvl, data_layer, bool):

    if not bool == True: return []

    #we define this once in the engine...
    db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'
    engine = sqla.create_engine(db_uri)
    metadata_obj = sqla.MetaData()

    status = '[vox_read_data_layer] '

    vox_lvl_table = Table(vox_lvl, metadata_obj, autoload_with=engine)

    conn = engine.connect()
    _names = ['vox_idx', f'{data_layer}']
    _cols = [_col for _col in vox_lvl_table.c if _col.name in _names]
    _sel = vox_lvl_table.select().with_only_columns(_cols)
    result = conn.execute(_sel)
    rows = result.fetchall()

    #why all that mess? because rhino3dm is not written to support numpy arrays...
    vox_df = pd.DataFrame.from_records(rows, columns = [c.name for c in _cols])
    #pts_data = vox_df[['vox_x','vox_y','vox_z']].to_numpy()
 
    if len(rows) == 0:
        status += r'Voxel Engine Running, but no SQL data loaded, showing single point...'
        rows = ((0, 0))

    else:
        status += f'Component successfully read data from: {VOX_FILENAME}'
    

    #TODO: don't return z_cont

    return status, \
           vox_df['vox_idx'].to_list(), \
           vox_lvl, \
           float(vox_df[f'{data_layer}'].min()), \
           float(vox_df[f'{data_layer}'].max()), \
           vox_df[f'{data_layer}'].to_list()
