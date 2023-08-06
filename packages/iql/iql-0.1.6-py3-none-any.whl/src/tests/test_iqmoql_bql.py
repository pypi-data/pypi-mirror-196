# Copyright (C) 2023, IQMO Corporation [support@iqmo.com]
# All Rights Reserved
#

import iqmoql as ql
import logging

logger = logging.getLogger(__name__)


def test_bql_simple():
    query = "get (name, px_last) for (['IBM US Equity', 'META US Equity'])"
    df = ql.execute(query)

    assert df is not None
    assert len(df) == 4


def test_bql_pivot():
    query = "get (name, px_last) for (['IBM US Equity', 'META US Equity']) iqmo(pivot=(ID, name))"
    df = ql.execute(query)
    assert df is not None
    # logging.info(df)
    assert len(df) == 2

    # return df


def test_bql_pivot2():
    query = "get (px_last) for (['IBM US Equity', 'META US Equity']) with (dates = range(-7D, 0D)) iqmo(pivot=auto)"
    df = ql.execute(query)
    assert df is not None
    # logging.info(df)
    assert len(df) == 16

    # return df


def test_bql_split():
    query = "get (name, px_last) for (['IBM US Equity', 'META US Equity']) with (fill=prev) iqmo(splitids=True)"
    df = ql.execute(query)

    assert df is not None
    assert len(df) == 4

    # return df


def test_bql_split_and_pivot():
    query = "get (name, px_last) for (['IBM US Equity', 'META US Equity']) with (fill=prev) iqmo(pivot=(ID, name);splitids=True)"
    df = ql.execute(query)

    assert df is not None
    assert len(df) == 2

    # return df


def test_bql_pivot_twoindices():
    query = "get (name, px_last) for (['IBM US Equity', 'META US Equity']) with (fill=prev) iqmo(pivot=([ID:DATE], name);splitids=True)"
    df = ql.execute(query)

    assert df is not None
    assert len(df) == 4

    return df


def test_bql_strip_cols():
    query = """
        get(
            id().positions as #positions, market_sector_des, px_last, avg(px_volume(dates=range(-12m, 0d))) as #avgvol
        )
        for(
            members('U31260312-3', type=PORT)
        )
        with(fill=prev)
        iqmo(pivot=(ID, name))"""

    df = ql.execute(query)
    assert len(df.columns) == 5

def test_bql_unknown_option():
    query = "get (name, px_last) for (['IBM US Equity', 'META US Equity']) with (fill=prev) iqmo(unknownoption=True)"
    try:
        df = ql.execute(query)
        failed = False
    except Exception:
        failed = True

    assert failed


def test_bql_renaming_columns():
    query = """get(
        AVG(TURNOVER(dates=range(-6m,0d))) * 2/ 1200M as #MP,
        (1200M * 0.001 / PX_LAST()) / avg(dropna(PX_VOLUME(dates=range(-3M,-1D)))) as #10BPS,
        (0.0499 * IS_SH_FOR_DILUTED_EPS(fa_period_type=A) * PX_LAST)/1200M as #fournine,
        AVG(TURNOVER(dates=range(-6m,0d))) as #avgturnover)
        for (
        ['BAC US Equity'])
        preferences (
        addcols=all)
        iqmo(pivot=(ID, name))"""

    df = ql.execute(query)

    assert len(df.columns) == 5


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


def test_s3api():
    query = "select * from (s3api('IBM US Equity')) q1"
    df = ql.execute(query)

    assert len(df) > 0


def test_s3api_join():
    query = """select * from 
            (
            get(
                SHORT_INT_RATIO, 
                SHORT_INT/EQY_FLOAT as #SI_PERCENT_EQUITY_FLOAT, 
                max(dropna(PX_HIGH(dates=range(-52w,0d)))) as #52WEEK_HIGH, 
                min(dropna(PX_LOW(dates=range(-52w,0d)))) as #52WEEK_LOW, 
                EQY_FUND_CRNCY, 
                PX_VOLUME, 
                avg(dropna(PX_VOLUME(dates=range(-3M, -1D)))) as #VOLUME_AVG_3M
                ) 
            for (['BAC US Equity'])
            with (currency=USD, fill=prev)
            preferences (addcols=all)
            iqmo(pivot=(ID, name))
            ) q1
            left outer join 
            (s3api('BAC US Equity')) q2
            on true"""

    df = ql.execute(query)

    assert len(df) > 0
