import sqlalchemy as sqla

from .constants import SQL_GET_COLS_RAW

def get_cols_sorted(vox_lvl, engine):
    #TODO: with session
    _cols_ord_stmt = SQL_GET_COLS_RAW.replace('LVL', f"{vox_lvl}")
    _cols_ord_que = sqla.text(_cols_ord_stmt)
    vox_lvl_cols = [item['name'] for item in engine.execute(_cols_ord_que).mappings().all()]