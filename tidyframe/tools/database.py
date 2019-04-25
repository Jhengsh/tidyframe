from datetime import datetime
import pandas as pd
from sqlalchemy import (MetaData, Table, Column, BigInteger, Integer, Float,
                        NVARCHAR, CHAR, DATETIME, BOOLEAN)


def create_table(df,
                 con,
                 name,
                 primary_key=[],
                 nvarchar_columns=[],
                 non_nullable_columns=[],
                 dtype=None,
                 all_nvarchar=False,
                 default_char_type=CHAR,
                 default_int_type=Integer,
                 create=False):
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
    create : Bool(default: False), direct create table in database

    Returns
    -------
    sqlalchemy Table object
    """
    meta = MetaData(bind=con)
    column_list = []
    int_info = pd.np.iinfo(pd.np.int32)
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
        try:
            if dtype is not None and x in dtype:
                each_column = Column(x,
                                     dtype[x],
                                     primary_key=is_primary_key,
                                     nullable=nullable)
            elif df[x].dtype.char == 'O':
                length = df[x].fillna('').apply(lambda x: len(str(x))).max()
                if x in nvarchar_columns or all_nvarchar:
                    each_column = Column(x,
                                         NVARCHAR(length * 2),
                                         primary_key=is_primary_key,
                                         nullable=nullable)
                else:
                    each_column = Column(x,
                                         default_char_type(length),
                                         primary_key=is_primary_key,
                                         nullable=nullable)
            elif df[x].dtype.char == 'M':
                each_column = Column(x,
                                     DATETIME(),
                                     primary_key=is_primary_key,
                                     nullable=nullable)
            elif df[x].dtype.char == 'l':
                max_column_value = df[x].max()
                min_column_value = df[x].min()
                if pd.notna(max_column_value) and pd.notna(
                        min_column_value
                ) and min_column_value <= int_info.min and max_column_value >= int_info.max:
                    each_column = Column(x,
                                         BigInteger(),
                                         primary_key=is_primary_key,
                                         nullable=nullable)
                else:
                    each_column = Column(x,
                                         default_int_type(),
                                         primary_key=is_primary_key,
                                         nullable=nullable)
            elif df[x].dtype.char == 'd':
                if con.name == 'mysql':
                    from sqlalchemy.dialects.mysql import DOUBLE
                    each_column = Column(x,
                                         DOUBLE(asdecimal=False),
                                         nullable=nullable)
                elif con.name == 'postgresql':
                    from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
                    each_column = Column(x, DOUBLE_PRECISION())
                else:
                    each_column = Column(x,
                                         Float(asdecimal=False),
                                         nullable=nullable)
            elif df[x].dtype.str == '|b1':
                each_column = Column(x,
                                     BOOLEAN(),
                                     primary_key=is_primary_key,
                                     nullable=nullable)
            else:
                each_column = Column(x,
                                     NVARCHAR(255),
                                     primary_key=is_primary_key,
                                     nullable=nullable)
        except Exception as e:
            raise Exception('Column {}: {}'.format(x, str(e)))
        column_list.append(each_column)
    if create:
        table_object_target.create()
        return True
    else:
        return Table(name, meta, *column_list, extend_existing=True)


def copy_table_schema(source_table,
                      target_table,
                      source_con,
                      target_con,
                      omit_collation=False,
                      create=False,
                      add_columns=[]):
    """
    Copy table schema from database to another database

    Parameters
    ----------
    source_table : source table name in database
    target_table : target table name
    source_con : sqlalchemy.engine.Engine or sqlite3.Connection, source engine
    target_con : sqlalchemy.engine.Engine or sqlite3.Connection, target engine
    omit_collation : Bool(default: False), omit all char collation
    create : Bool(default: False), direct create table in database
    add_columns : list of column object

    Returns
    -------
    sqlalchemy Table object or True
    """
    meta_source = MetaData(bind=source_con)
    meta_target = MetaData(bind=target_con)
    table_object_source = Table(source_table, meta_source, autoload=True)
    columns = [{'name': x.name, 'type': x.type} for x in table_object_source.c]
    if omit_collation:
        for x in columns:
            try:
                x['type'].collation = None
            except:
                pass
    columns = [Column(x['name'], x['type']) for x in columns]
    if add_columns:
        columns.extend(add_columns)
    table_object_target = Table(target_table,
                                meta_target,
                                *columns,
                                extend_existing=True)
    if create:
        table_object_target.create()
        return True
    else:
        return table_object_target


def fit_dataframe_to_table_schema(df, table):
    """
    Fit DataFrame to table schema, let you can use DataFrame.to_sql directly if table is exist
    Limit: not tranform column dtype if python_type is str and column dtype is object 

    Parameters
    ----------
    df : Pandas DataFrame
    table : Table object 

    Returns
    -------
    None
    """
    for x in table.columns:
        if (x.type.python_type == str and df[x.name].dtype == 'object') or (
                x.type.python_type == float and df[x.name].dtype == 'float64'
        ) or (x.type.python_type == int and df[x.name].dtype == 'int64') or (
                x.type.python_type == int and df[x.name].dtype == 'int32') or (
                    x.type.python_type == bool and df[x.name].dtype == 'bool'
                ) or (x.type.python_type == datetime
                      and df[x.name].dtype == 'datetime64[ns]'):
            pass
        elif x.type.python_type == str and df[x.name].dtype != 'object':
            df[x.name] = [
                pd.np.nan if pd.np.isnan(x) else str(x) for x in df[x.name]
            ]
        elif x.type.python_type == float and df[
                x.name].dtype != 'float64' and df[x.name].dtype != 'float32':
            df[x.name] = df[x.name].astype(float)
        elif x.type.python_type == int and df[x.name].dtype != 'int64' and df[
                x.name].dtype != 'int32':
            df[x.name] = df[x.name].astype(int)
        elif x.type.python_type == bool and df[x.name].dtype != 'bool':
            df[x.name] = df[x.name].astype(bool)
        elif x.type.python_type == datetime and df[
                x.name].dtype != 'datetime64[ns]':
            df[x.name] = pd.to_datetime(df[x.name])
        else:
            raise Exception(
                'Column {} not deal with python_type {} and dtype {}'.format(
                    x.name, str(x.type.python_type), df[x.name].dtype))
    return None
