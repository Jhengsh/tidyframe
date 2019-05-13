from copy import deepcopy
from datetime import datetime
import pandas as pd
from sqlalchemy import (MetaData, Table, Column, BigInteger, Integer, Float,
                        NVARCHAR, CHAR, DATETIME, BOOLEAN)
from sqlalchemy.schema import CreateTable
from funcy import chunks


def create_table(
        df,
        name,
        con,
        primary_key=[],
        nvarchar_columns=[],
        non_nullable_columns=[],
        dtype=None,
        create=True,
        all_nvarchar=False,
        base_char_type=CHAR(),
        base_nchar_type=NVARCHAR(),
        base_int_type=Integer(),
        base_bigint_type=BigInteger(),
        base_float_type=Float(),
        base_boolean_type=BOOLEAN(),
):
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
                    nchar_type = deepcopy(base_nchar_type)
                    nchar_type.length = length * 2
                    each_column = Column(x,
                                         nchar_type,
                                         primary_key=is_primary_key,
                                         nullable=nullable)
                else:
                    char_type = deepcopy(base_char_type)
                    char_type.length = length
                    each_column = Column(x,
                                         char_type,
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
                                         base_bigint_type,
                                         primary_key=is_primary_key,
                                         nullable=nullable)
                else:
                    each_column = Column(x,
                                         base_int_type,
                                         primary_key=is_primary_key,
                                         nullable=nullable)
            elif df[x].dtype.char == 'd':
                each_column = Column(x, base_float_type, nullable=nullable)
            elif df[x].dtype.str == '|b1':
                each_column = Column(x,
                                     base_boolean_type,
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
        Table(name, meta, *column_list, extend_existing=True).create()
        return True
    else:
        return Table(name, meta, *column_list, extend_existing=True)


def copy_table_schema(source_table,
                      target_table,
                      source_con,
                      target_con,
                      omit_collation=False,
                      create=True,
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
    create : Bool(default: True), direct create table in database
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


def fit_table_schema_type(df, table):
    """
    Fit DataFrame to table schema type, let you can use DataFrame.to_sql directly if table is exist
    Limit: not tranform column dtype if python_type is str and column dtype is object 

    Parameters
    ----------
    df : Pandas DataFrame
    table : Table object 

    Returns
    -------
    None
    """
    try:
        for x in table.columns:
            if (x.type.python_type == float and df[x.name].dtype == 'float64'
                ) or (x.type.python_type == int and df[x.name].dtype == 'int64'
                      ) or (x.type.python_type == int
                            and df[x.name].dtype == 'int32') or (
                                x.type.python_type == bool
                                and df[x.name].dtype == 'bool') or (
                                    x.type.python_type == datetime
                                    and df[x.name].dtype == 'datetime64[ns]'):
                pass
            elif x.type.python_type == str:
                df[x.name] = [
                    pd.np.nan
                    if not isinstance(x, list) and pd.isna(x) else str(x)
                    for x in df[x.name]
                ]
            elif x.type.python_type == float and df[
                    x.name].dtype != 'float64' and df[
                        x.name].dtype != 'float32':
                df[x.name] = df[x.name].astype(float)
            elif x.type.python_type == int and df[
                    x.name].dtype != 'int64' and df[x.name].dtype != 'int32':
                df[x.name] = df[x.name].astype(int)
            elif x.type.python_type == bool and df[x.name].dtype != 'bool':
                df[x.name] = df[x.name].astype(bool)
            elif x.type.python_type == datetime and df[
                    x.name].dtype != 'datetime64[ns]':
                df[x.name] = pd.DatetimeIndex(df[x.name]).tz_localize(None)
            else:
                raise Exception(
                    'Column {} not deal with python_type {} and dtype {}'.
                    format(x.name, str(x.type.python_type), df[x.name].dtype))
        return None
    except Exception as e:
        raise Exception('fit Column {} error: {}'.format(x.name, str(e)))


def load_table_schema(name, con):
    """
    load table schema from database

    Parameters
    ----------
    name : string, name of SQL table
    con : sqlalchemy.engine.Engine or sqlite3.Connection

    Returns
    -------
    sqlalchemy Table object
    """

    meta = MetaData(bind=con)
    return Table(name, meta, autoload=True)


def drop_table(name, con):
    """
    drop table from database

    Parameters
    ----------
    name : string, name of SQL table
    con : sqlalchemy.engine.Engine or sqlite3.Connection

    Returns
    -------
    True
    """

    table = load_table_schema(name, con)
    table.drop()
    return True


def get_create_table_script(table):
    """
    get create table script

    Parameters
    ----------
    table : sqlalchemy Table object

    Returns
    -------
    string which sqlalchemy create for create table
    """
    return CreateTable(table).compile().string


def _insert_chunk_records(records, table, con):
    with con.connect() as connection:
        with connection.begin() as transaction:
            try:
                connection.execute(table.insert(), records)
            except:
                transaction.rollback()
                return False
            else:
                transaction.commit()
                return True


def bulk_insert(records, table, con, batch_size=10000, only_insert_fail=False):
    """
    bulk insert records(list dict)

    Parameters
    ----------
    records : list of dict
    table : sqlalchemy Table object(you can get from function load_table_schema)
    con : sqlalchemy.engine.Engine or sqlite3.Connection
    batch_size : batch size for bluk insert
    only_insert_fail : Bool(default: False), only return record wihich insert fail

    Returns
    -------
    list of record which insert fail in batch records or list of record which fail to insert database
    """
    list_error_batch = []
    for each_batch_record in chunks(batch_size, records):
        if not _insert_chunk_records(each_batch_record, table, con):
            list_error_batch.append(each_batch_record)
    return_batch_error_record = []
    for x in list_error_batch:
        return_batch_error_record.extend(x)
    if not only_insert_fail:
        return return_batch_error_record
    else:
        while (batch_size > 10):
            batch_size = int(batch_size / 2)
            list_error = bulk_insert(return_batch_error_record,
                                     table,
                                     con,
                                     batch_size=batch_size)
        return_list_insert_fail_record = []
        for record in list_error:
            insert_status = _insert_chunk_records(record, table, con)
            if not insert_status:
                return_list_insert_fail_record.append(record)
        return return_list_insert_fail_record
