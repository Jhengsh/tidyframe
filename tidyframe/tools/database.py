import pandas as pd
from sqlalchemy import MetaData, Table, Column, Integer, Float, NVARCHAR, CHAR, DATETIME, BOOLEAN


def create_table_object(df,
                        con,
                        name,
                        primary_key=[],
                        nvarchar_columns=[],
                        non_nullable_columns=[],
                        dtype=None,
                        all_nvarchar=False,
                        default_char_type=CHAR,
                        default_int_type=Integer):
    """
    Create sqlalchemy Table object for create table in database

    Parameters
    ----------
    df : Pandas DataFrame
    con : sqlalchemy.engine.Engine or sqlite3.Connection
    name : string, name of SQL table
    primary_key : list, primary key columns
    nvarchar_columns : list, nvarchar columns
    non_nullable_columns : list, non-nullable columns
    dtype: dict, optional, specifying the datatype for columns. The keys should be the column names and the values should be the SQLAlchemy types or strings for the sqlite3 legacy mode.
    all_nvarchar : Bool, all string column use NVARCHAR or not

    Returns
    -------
    sqlalchemy Table object
    """
    meta = MetaData(bind=con)
    column_list = []
    for x in df:
        if x in primary_key:
            is_primary_key = True
            nullable = False
        else:
            is_primary_key = False
            if x in non_nullable_columns:
                nullable = False
            else:
                nullable = True
        if dtype is not None and x in dtype:
            each_column = Column(
                x, dtype[x], primary_key=is_primary_key, nullable=nullable)
        elif df[x].dtype.char == 'O':
            length = df[x].fillna('').apply(lambda x: len(x)).max()
            if x in nvarchar_columns or all_nvarchar:
                each_column = Column(
                    x,
                    NVARCHAR(length * 2),
                    primary_key=is_primary_key,
                    nullable=nullable)
            else:
                each_column = Column(
                    x,
                    default_char_type(length),
                    primary_key=is_primary_key,
                    nullable=nullable)
        elif df[x].dtype.char == 'M':
            each_column = Column(
                x, DATETIME(), primary_key=is_primary_key, nullable=nullable)
        elif df[x].dtype.char == 'l':
            each_column = Column(
                x,
                default_int_type(),
                primary_key=is_primary_key,
                nullable=nullable)
        elif df[x].dtype.char == 'd':
            if con.name == 'mysql':
                from sqlalchemy.dialects.mysql import DOUBLE
                each_column = Column(
                    x, DOUBLE(asdecimal=False), nullable=nullable)
            elif con.name == 'postgresql':
                from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
                each_column = Column(x, DOUBLE_PRECISION())
            else:
                each_column = Column(
                    x, Float(asdecimal=False), nullable=nullable)
        elif df[x].dtype.str == '|b1':
            each_column = Column(
                x, BOOLEAN(), primary_key=is_primary_key, nullable=nullable)
        else:
            each_column = Column(
                x,
                NVARCHAR(255),
                primary_key=is_primary_key,
                nullable=nullable)
        column_list.append(each_column)
    return Table(name, meta, *column_list, extend_existing=True)
