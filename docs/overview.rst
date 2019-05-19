.. Overview

Overview
========

TidyFrame help clean data to tidy DadaFrame quickly. TidyFrame provide some function to help you extract, transform, load data easily.
This page help you know how to use tidyframe function.

+ Make tranform nest dictionary easily

    >>> from tidyframe import flatten_dict
    >>> nest_dict = {
    ...     'a': 1,
    ...     'b': [1, 2],
    ...     'c': {
    ...         'cc1': 3,
    ...         'cc2': 4
    ...     },
    ...     'd': {
    ...         'd1': 5,
    ...         'd2': {
    ...             'dd1': 6,
    ...             'dd2': 7
    ...         }
    ...     }
    ... }
    >>> flatten_dict(nest_dict)
    {'a': 1, 'b': [1, 2], 'c_cc1': 3, 'c_cc2': 4, 'd_d1': 5, 'd_d2_dd1': 6, 'd_d2_dd2': 7}
    >>> flatten_dict(nest_dict, inner_name=True)
    {'a': 1, 'b': [1, 2], 'cc1': 3, 'cc2': 4, 'd1': 5, 'dd1': 6, 'dd2': 7}


+ Make select columns, reorder columns easily

    >>> import numpy as np
    >>> import pandas as pd
    >>> from tidyframe import select, reorder_columns
    >>> df = pd.DataFrame(np.array(range(10)).reshape(2, 5),
    ...                   columns=list('abcde'),
    ...                   index=['row_1', 'row_2'])
    >>> select(df, columns=['b', 'd'])
        b  d
    row_1  1  3
    row_2  6  8
    >>> select(df, columns_minus=['b', 'd'])
        a  c  e
    row_1  0  2  4
    row_2  5  7  9
    >>> select(df, pattern='[a|b]')
        a  b
    row_1  0  1
    row_2  5  6
    >>> df = pd.DataFrame([{'a': 1, 'b': 1, 'c': 1, 'd': 1, 'e': 2}])
    >>> df_reorder = reorder_columns(df, ['b', 'c'], last_columns=['a', 'd'])
    >>> df_reorder
    b  c  e  a  d
    0  1  1  2  1  1

+ Wapper SQLAlchemy function to help you create table, insert table, drop table easily

  + Help find suitable data type and string length for database table(you can change length by sqlalchemy Table object if you want)  
  + Help you bulk insert records and find insert fail records quickly

    >>> import pandas as pd
    >>> from sqlalchemy import create_engine
    >>> from datetime import datetime
    >>> from tidyframe import (create_table, load_table_schema, bulk_insert)
    >>>
    >>> engine = create_engine('sqlite:///test_for_create_table.db')
    >>> df = pd.DataFrame()
    >>> df['a'] = list('abc')
    >>> df['b'] = 1
    >>> df['c'] = 1.3
    >>> df['d'] = [pd.np.nan, 10, 1.4]
    >>> df['e'] = ['adev', pd.NaT, '今天天氣']
    >>> df['f'] = [datetime.now(), None, datetime.now()]
    >>> df['g'] = [True, False, True]
    >>> df['h'] = 2147483647 * 2
    >>> create_table(df,
    ...              'test_table',
    ...              engine,
    ...              primary_key=['a'],
    ...              nvarchar_columns=['e'],
    ...              non_nullable_columns=['d'],
    ...              create=False)
    Table('test_table', MetaData(bind=Engine(sqlite:///test_for_create_table.db)), Column('a', CHAR(length=1), table=<test_table>, primary_key=True, nullable=False), Column('b', Integer(), table=<test_table>), Column('c', Float(), table=<test_table>), Column('d', Float(), table=<test_table>, nullable=False), Column('e', NVARCHAR(length=8), table=<test_table>), Column('f', DATETIME(), table=<test_table>), Column('g', BOOLEAN(), table=<test_table>), Column('h', Integer(), table=<test_table>), schema=None)
    >>>
    >>> create_table(df,
    ...              'test_table_create',
    ...              engine,
    ...              primary_key=['a'],
    ...              nvarchar_columns=['e'],
    ...              non_nullable_columns=['d'],
    ...              create=True)
    True
    >>>
    >>> engine = create_engine("mysql://root:sdysuD4UXaynu84u@127.0.0.1/test_db")
    >>> df = pd.DataFrame()
    >>> df["a"] = ["a"] * 10000
    >>> df["b"] = [1] * 10000
    >>> df["c"] = [1.3] * 10000
    >>>
    >>> create_table(df, "want_insert_table", engine, create=True)
    True
    >>> table = load_table_schema("want_insert_table", engine)
    >>>
    >>> df.iloc[0,0]= "abc"
    >>> df.iloc[-1,0]= "abc"
    >>>
    >>> insert_fail_records = bulk_insert(df.to_dict("record"),
    ...                                   table,
    ...                                   engine,
    ...                                   batch_size=100)
    >>> len(insert_fail_records)
    200
    >>>
    >>> insert_fail_records = bulk_insert(df.to_dict("record"),
    ...                                   table,
    ...                                   engine,
    ...                                   batch_size=100,
    ...                                   only_insert_fail=True)
    >>> len(insert_fail_records)
    2