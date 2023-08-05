# Copyright (C) 2023, IQMO Corporation [support@iqmo.com]
# All Rights Reserved
#

import iqmoql as ql
import logging

logger = logging.getLogger(__name__)

def test_single_select():
    bql = "get (name, px_last) for (['IBM US Equity', 'META US Equity']) with (fill=prev) iqmo(pivot=(ID, name);splitids=True)"
    sql = f"select avg(px_last) avg_px from query_bql({bql}) q1"

    df = ql.execute(sql)
    assert len(df) == 1


def test_two_bql_select():
    bql = "get (name, px_last) for (['IBM US Equity', 'META US Equity']) with (fill=prev) iqmo(pivot=(ID, name);splitids=True)"
    sql = f"select * from query_bql({bql}) q1 join query_bql({bql}) q2 on q1.id = q2.id"

    df = ql.execute(sql)

    assert len(df) == 2

def test_autopivot():
    bql1 = "get (name, GICS_SECTOR_NAME) for (['IBM US Equity', 'META US Equity']) with (fill=prev) iqmo(pivot=auto)"
    bql2 = "get (px_last) for (['IBM US Equity', 'META US Equity']) with (fill=prev, dates=range(-2D, 0D)) iqmo(pivot=auto)"

    sql = f"select q1.id, gics_sector_name, px_last from query_bql({bql1}) q1 join query_bql({bql2}) q2 on q1.id = q2.id"

    df = ql.execute(sql)

    assert len(df) == 6
    assert len(df.columns) == 3


def test_cte():
    query = "with q1 as query_bql(get (name, px_last) for (['IBM US Equity', 'META US Equity']) with (fill=prev) iqmo(pivot=(id, name))) select * from q1"
    df = ql.execute(query)

    assert df is not None
    assert len(df) == 2

    return df


def test_failure():
    query = """select ID,bob,mary from query_bql(get () iqmo(pivot=(ID, name); allow_failure=ID,bob,mary)) as blah"""

    df = ql.execute(query)

    assert len(df) == 0 and "bob" in df.columns

