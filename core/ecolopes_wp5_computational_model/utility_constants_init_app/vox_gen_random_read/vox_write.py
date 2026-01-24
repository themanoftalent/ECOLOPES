#the code balow is untested, just dropped here during refactoring...
#need to redo it soon

import os #remove after moving db_uri etc. to database helpers
from itertools import islice

import rhino3dm
import ghhops_server as hs

from ..constants import VOX_DOC_PATH, VOX_FILENAME, SQL_GET_COLS_RAW, SQL_VARIABLE_LIMIT
from ..utility import get_cols_sorted


import numpy as np
import pandas as pd
import sqlalchemy as sqla

from sqlalchemy import select, column, delete


# Those are for SQL inserts...
#from sqlalchemy.orm import Session

#from sqlalchemy import insert
from sqlalchemy.dialects.sqlite import insert as sqlite_upsert

#sqla.orm.Session
#sqla.insert
#from sqla.dialects.sqlite import insert as sqlite_upsert


vox_write_datapoint_format_filter_kwargs = {
    'rule':"/vox_write_datapoint_format_filter",
    'name':"VoxWriteDatapointFormatFilter",
    'description':"VoxWriteDatapointFormatFilter Description",
    #'icon':"examples/pointat.png",
    'inputs':[
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        hs.HopsString("source_format", "source_format", "source_format - formated: aa_bb_cc:"),
        hs.HopsString("remove", "remove", "remove columns - formated: aa_bb_cc:"),
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
        hs.HopsString("datapoint_format", "datapoint_format", "Format of the datapoint"),
        #hs.HopsVector("C", "C", "Colors"),
    ]
    }

def vox_write_datapoint_format_filter(vox_lvl, source_format, remove):
    
    #we define this once in the engine...
    #db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'
    #engine = sqla.create_engine(db_uri)
    #metadata_obj = sqla.MetaData()

    status = '[vox_write_datapoint_format_filter] '

    _out = source_format.replace(remove, '')

    print(_out)

    #updating constr
    #_cols_ord_stmt = SQL_GET_COLS_RAW.replace('LVL', f"{vox_lvl}")
    #_cols_ord_que = sqla.text(_cols_ord_stmt)
    #vox_lvl_cols = [item['name'] for item in engine.execute(_cols_ord_que).mappings().all()]
    
    #vox_lvl_table = sqla.Table(vox_lvl, metadata_obj, autoload_with=engine)
    #data_layers = set([c.name for c in vox_lvl_table.columns])

    #lay_no_write = ['vox_idx', 'vox_x','vox_y','vox_z', 'vox_z_cont']
    #data_layers = list(set(vox_lvl_cols).difference(reserved_layers))

    #if skip_columns[-1] == ':':
    #    skip_columns= skip_columns[:-1]
    
    #reserved_layers = skip_columns.split('-')

    #writable_layers = [item for item in vox_lvl_cols if item not in lay_no_write]
    #writable_layers = ['coord_x','coord_y','coord_z'] + writable_layers

    #data_layers = list(set(vox_lvl_cols).difference(reserved_layers))

    #print('-'.join(data_layers))

    status += f'"{remove}" removed' 


    return status, \
           vox_lvl, \
           _out




vox_write_datapoint_format_kwargs = {
    'rule':"/vox_write_datapoint_format",
    'name':"VoxWriteDatapointFormat",
    'description':"VoxWriteDatapointFormat Description",
    #'icon':"examples/pointat.png",
    'inputs':[
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        #hs.HopsString("source_format", "source_format", "source_format - formated: aa_bb_cc:"),
        #hs.HopsString("remove", "remove", "remove columns - formated: aa_bb_cc:"),
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
        hs.HopsString("datapoint_format", "datapoint_format", "Format of the datapoint"),
        #hs.HopsVector("C", "C", "Colors"),
    ]
    }


def vox_write_datapoint_format(vox_lvl):
    
    #we define this once in the engine...
    db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'
    engine = sqla.create_engine(db_uri)
    metadata_obj = sqla.MetaData()

    status = '[vox_write_datapoint_format] '
    
    _cols_ord_stmt = SQL_GET_COLS_RAW.replace('LVL', f"{vox_lvl}")
    _cols_ord_que = sqla.text(_cols_ord_stmt)
    vox_lvl_cols = [item['name'] for item in engine.execute(_cols_ord_que).mappings().all()]
    


    #vox_lvl_table = sqla.Table(vox_lvl, metadata_obj, autoload_with=engine)
    #data_layers = set([c.name for c in vox_lvl_table.columns])

    lay_no_write = ['vox_idx', 'vox_x','vox_y','vox_z', 'vox_z_cont']
    #data_layers = list(set(vox_lvl_cols).difference(reserved_layers))

    #if skip_columns[-1] == ':':
    #    skip_columns= skip_columns[:-1]
    
    #reserved_layers = skip_columns.split('-')

    writable_layers = [item for item in vox_lvl_cols if item not in lay_no_write]
    writable_layers = ['coord_x','coord_y','coord_z'] + writable_layers

    #data_layers = list(set(vox_lvl_cols).difference(reserved_layers))

    #print('-'.join(data_layers))

    status += f'{len(vox_lvl_cols)} data layers listed' 


    return status, \
           vox_lvl, \
           '-'.join(writable_layers)






#TODO: turn it into docstring
#TODO: maybe turn it into classes to hold data (kwargs) with logics?

desc_data_point = ""
desc_data_point += "Voxel data points. " + \
"A data point contains both the x, y, z " + \
"coordinates and the numeric values related " + \
"to the parameter it contains. Number of parameters" + \
"should match with the columns defined in [...] " + \
"Because of the current Hops limitation data points " + \
"need to be formatted in Grasshopper as a single string" + \
"like this: x_y_z_your-param:x_y_z_your-param: (...) " + \
"e.g. 1.30_1.45_1.20_255:2.35_3.55_4.60_255"

## copy over the kwargs definition
vox_write_geom_kwargs = {
    'rule':"/vox_write_geom",
    'name':"VoxWriteGeom",
    'description':"VoxWriteGeom",
    #'icon':"examples/pointat.png",
    'inputs':[
        #hs.HopsXxx('name_in_desc', 'name_on_canvas', 'desc')
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        hs.HopsString("datapoint_format", "datapoint_format", "Format of the datapoint"),
        hs.HopsString("Voxel data points", "Data points", desc_data_point),
        hs.HopsBoolean("Boolean", "Run", "Boolean toggle to write"),
        #hs.HopsVector("C", "C", "Colors"), #Lets hardcode red for now...
    ],
    'outputs':[
        hs.HopsString("info", "info", "Status of the component"),
        hs.HopsString("vox_idx", "vox_idx", "vox_idx"),
        #hs.HopsPoint("P", "P", "Vox points"),
        #hs.HopsNumber("vox_z_cont", "z_cont", "vox_z_cont"),
        #First is the name of output in GH
        #hs.HopsPoint("C", "C", "Colors"),
        #hs.HopsString("C", "C", "Colors"),
        #hs.HopsVector("C", "C", "Colors"),
    ]
    }

def voxidx_in_vox_not(row):
    return f"{row['vox_x']}_{row['vox_y']}_{row['vox_z']}"


def vox_write_geom(vox_lvl, datapoint_format, points, bool):

    #oh boy, oh boy, Hops does not work on lists...

    if not bool == True: return []
    status = '[vox_write_geom] '

    # in GH -> join column values (point coords)
    # with _ and join rows with :

    datapoint_format = datapoint_format.split('-')#[:-1]
    #print(datapoint_format)

    vox_rows = points.split(':') 
    points = np.array([_i.split('-') for _i in vox_rows])

    #print(points)

    #len(vox_write_geom_kwargs['inputs'])

    if len(datapoint_format) != points.shape[1]:
        status += "[ERROR]: Wrong point format - data length don't match column count"

        #TODO: as you add outputs, make sure you return here one 0 for each output
        #TODO: maybe something like [status, 0 * n]
        #len(vox_write_geom_kwargs['output'])
        return status, [0]

    #TODO: dtype checking, especially for the the 3 first columns 
    
    vox_df = pd.DataFrame(points, columns =[*datapoint_format])
    #print(vox_df)


    #vox_df = pd.DataFrame.from_records(points[:,:3], columns = ['coord_x','coord_y','coord_z'])
    vox_df['vox_z_cont'] = vox_df['coord_z']

    vox_df['vox_x'] = vox_df['coord_x'].astype(float).round(0).astype(int)
    vox_df['vox_y'] = vox_df['coord_y'].astype(float).round(0).astype(int)
    vox_df['vox_z'] = vox_df['coord_z'].astype(float).round(0).astype(int)
    vox_df.drop(columns=['coord_x', 'coord_y', 'coord_z'], inplace=True)


    #vox_df['vox_idx'] = vox_df[['vox_x','vox_y','vox_z']].apply(voxidx_in_vox_not, axis=1)
    
    vox_df['vox_idx'] = vox_df['vox_x'].map(str) + "_" + \
                        vox_df['vox_y'].map(str) + "_" + \
                        vox_df['vox_z'].map(str)

    #TODO: think of how we will handle duplicate cell records...

    #continue here tomorrow
    #print(vox_df)


    #we define this once in the engine...
    db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'
    engine = sqla.create_engine(db_uri)
    metadata_obj = sqla.MetaData()


    _cols_ord_stmt = SQL_GET_COLS_RAW.replace('LVL', f"{vox_lvl}")
    _cols_ord_que = sqla.text(_cols_ord_stmt)
    vox_lvl_cols = [item['name'] for item in engine.execute(_cols_ord_que).mappings().all()]

    #TODO: what we do with NaNs to not fall out of 8bit int bounds?
    _nan_value = 0

    #NaN all values in the columns for which we don't have data...
    for item in vox_lvl_cols:
        if not item in vox_df.columns:
            vox_df[item] = _nan_value

    conn = engine.connect()
    vox_lvl_table = sqla.Table(vox_lvl, metadata_obj, autoload_with=engine)

    #print(vox_df.to_dict('records'))
    #stmt = sqlite_upsert(vox_lvl_table).values(vox_df.to_dict('records'))


    #from sqlalchemy import exc

    #db.add(user)

    #try:
    #    db.commit()
    #except exc.SQLAlchemyError:
    #    pass # do something intelligent here

    

    if SQL_VARIABLE_LIMIT != 0:

        _chunked = []
        _rec_list = vox_df.to_dict('records')

        for i in range(0, len(_rec_list), SQL_VARIABLE_LIMIT):
            _chunked.append(_rec_list[i:i+SQL_VARIABLE_LIMIT])

        for _rec_part in _chunked:
            stmt = sqlite_upsert(vox_lvl_table).values(_rec_part)
            #stmt = stmt.on_conflict_do_nothing(index_elements=['vox_idx'])
            with engine.connect() as conn:
                result = conn.execute(stmt)
                #conn.commit() #neeed only on 2.0
    
    #this is for other backends
    else:
        pass


    '''
    
        for vox_chunk in chunks(vox_df.to_dict('records'), SQL_VARIABLE_LIMIT):
            stmt = sqlite_upsert(vox_lvl_table).values(vox_chunk) 
            with engine.connect() as conn:
                result = conn.execute(stmt)
                conn.commit()
    

    #this is for other backends
    else:
        stmt = sqlite_upsert(vox_lvl_table).values(vox_df.to_dict('records'))
        with engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()
'''

    # create session and add objects
    #with sqla.orm.Session(engine) as session:
    #    session.execute(stmt)
    #    session.commit()


    status += f'Done inserting into {len(_rec_list)} records into {vox_lvl}'


    #stmt = stmt.on_conflict_do_update(
    #    index_elements=[vox_lvl_table.vox_idx], set_=dict(vox_idx=stmt.excluded.vox_idx)
    #)

   
    #with Session(engine) as session:
    #    session.execute(stmt)
    #    session.commit()        
    
    ##print(vox_df.to_dict('records')[:5])

    #with Session(engine) as session:
    #    session.execute( insert(vox_lvl_table), vox_df.to_dict('records') )
    #    session.commit()


    #session.execute(stmt)


    #_cols = [_col.name for _col in vox_lvl_table.c]
    #print(_cols)

    #print([_col for _col in vox_lvl_table.c.name])

    #stmt = sqlite_upsert(vox_lvl_table).values(
    #[
    #    {"name": "spongebob", "fullname": "Spongebob Squarepants"},
    #    {"name": "sandy", "fullname": "Sandy Cheeks"},
    #    {"name": "patrick", "fullname": "Patrick Star"},
    #    {"name": "squidward", "fullname": "Squidward Tentacles"},
    #    {"name": "ehkrabs", "fullname": "Eugene H. Krabs"},
    #]
    #)

    #stmt = stmt.on_conflict_do_update(
    #    index_elements=[vox_lvl_table.name], set_=dict(fullname=stmt.excluded.fullname)
    #)
    
    #session.execute(stmt)

    #_names = ['vox_idx', f'{data_layer}']
    #_cols = [_col for _col in vox_lvl_table.c if _col.name in _names]
    #_sel = vox_lvl_table.select().with_only_columns(_cols)
    #result = conn.execute(_sel)
    #rows = result.fetchall()

    #why all that mess? because rhino3dm is not written to support numpy arrays...
   # vox_df = pd.DataFrame.from_records(rows, columns = [c.name for c in _cols])
    #pts_data = vox_df[['vox_x','vox_y','vox_z']].to_numpy()
 
    #if len(rows) == 0:
    #    status += r'Voxel Engine Running, but no SQL data loaded, showing single point...'
    #    rows = ((0, 0))


    #else:
    #    status += f'Component successfully read data from: {VOX_FILENAME}'
    

    #TODO: don't return z_cont


    # aggregation function on duplicates



    return status, \
           vox_df['vox_idx'].to_list()
           #vox_df['vox_idx'].to_list(), \
           #float(vox_df[f'{data_layer}'].min()), \
           #float(vox_df[f'{data_layer}'].max()), \
           #vox_df[f'{data_layer}'].to_list()





## copy over the kwargs definition
vox_clean_new_kwargs = {
    'rule':"/vox_clean_new",
    'name':"VoxCleanNew",
    'description':"VoxCleanNew",
    #'icon':"examples/pointat.png",
    'inputs':[
        #hs.HopsXxx('name_in_desc', 'name_on_canvas', 'desc')
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        #hs.HopsString("datapoint_format", "datapoint_format", "Format of the datapoint"),
        #hs.HopsString("Voxel data points", "Data points", desc_data_point),
        hs.HopsBoolean("Boolean", "Run", "Boolean toggle to write"),
        #hs.HopsVector("C", "C", "Colors"), #Lets hardcode red for now...
    ],
    'outputs':[
        hs.HopsString("info", "info", "Status of the component"),
        hs.HopsString("vox_lvl_name", "vox_lvl_name", "Select voxel resolution level, e.g. vox_lvl30"),
        hs.HopsString("vox_idx", "vox_idx", "vox_idx"),
        #hs.HopsPoint("P", "P", "Vox points"),
        #hs.HopsNumber("vox_z_cont", "z_cont", "vox_z_cont"),
        #First is the name of output in GH
        #hs.HopsPoint("C", "C", "Colors"),
        #hs.HopsString("C", "C", "Colors"),
        #hs.HopsVector("C", "C", "Colors"),
    ]
    }

def vox_clean_new(vox_lvl, bool):


    #we define this once in the engine...
    #in the baseClass?

    db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'
    engine = sqla.create_engine(db_uri)
    metadata_obj = sqla.MetaData()

    status = '[vox_clean_new] '

    if not bool == True: return status, 0, 0

    conn = engine.connect()
    vox_lvl_table = sqla.Table(vox_lvl, metadata_obj, autoload_with=engine)

    stmt = (
    select(vox_lvl_table).
    where(vox_lvl_table.c.is_new == 1).with_only_columns(column('vox_idx'))
    )

    #parse the vox_idx for returning
    rows = conn.execute(stmt).fetchall()

    status += f'Found {len(rows)} new data points from {vox_lvl}'
    
    db_uri = f'sqlite:///{os.path.join(VOX_DOC_PATH, VOX_FILENAME)}'
    engine = sqla.create_engine(db_uri)
    metadata_obj = sqla.MetaData()

    conn = engine.connect()
    vox_lvl_table = sqla.Table(vox_lvl, metadata_obj, autoload_with=engine)


    '''
    if SQL_VARIABLE_LIMIT != 0:

            _chunked = []
            _rec_list = rows

            for i in range(0, len(_rec_list), SQL_VARIABLE_LIMIT):
                _chunked.append(_rec_list[i:i+SQL_VARIABLE_LIMIT])

            for _rec_part in _chunked:
                stmt = sqlite_upsert(vox_lvl_table).values(_rec_part)
                #stmt = stmt.on_conflict_do_nothing(index_elements=['vox_idx'])
                with engine.connect() as conn:
                    result = conn.execute(stmt)
                    #conn.commit() #neeed only on 2.0
    
    '''
    
    stmt = (
    delete(vox_lvl_table).
    where(vox_lvl_table.c.is_new == 1)
    )



    #print(stmt)
    conn.execute(stmt)
    
    status += f'   Removed {len(rows)} data points marked as is_new == 1 from {vox_lvl}'

    return status, \
           vox_lvl, \
           'NotImplemented'
           #vox_df['vox_idx'].to_list()