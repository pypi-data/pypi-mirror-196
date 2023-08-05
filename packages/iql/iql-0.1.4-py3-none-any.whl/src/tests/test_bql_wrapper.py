# Copyright (C) 2023, IQMO Corporation [support@iqmo.com]
# All Rights Reserved
#


from bbg_bql.bql_datamodel import RawBqlQuery, BqlQuery, QueryPipeline

import logging
logger = logging.getLogger(__name__)

TEST_EQUITY = "IBM US Equity"

def test_raw_simple():
    q = RawBqlQuery(f"get (name) for (['{TEST_EQUITY}'])")
    success = q.execute()
    assert success


def test_raw_query_with_param():
    q = RawBqlQuery("get (name) for (['$SECURITY'])")
    q.params["$SECURITY"] = TEST_EQUITY
    success = q.execute()
    assert success


def test_query():
    q = BqlQuery(
        name="test",
        fields=["id"],
        security=["IBM US Equity", "HUBS US Equity"],
        let_str=None,
        with_params=None,
        for_str="$SECURITY",
    )
    success = q.execute()
    assert success
    assert q.dataframe is not None
    assert len(q.dataframe) == 2


def test_single_query_multiple_securities():
    q = BqlQuery(
        name="ids",
        fields=["id"],
        security=["IBM US Equity", "HUBS US Equity"],
        let_str=None,
        with_params=None,
        for_str="$SECURITY",
    )
    success = q.execute()
    assert success
    assert q.dataframe is not None
    assert len(q.dataframe) == 2


def test_pipeline_ids_single():

    pipeline = QueryPipeline()
    q1 = BqlQuery(
        name="ids",
        fields=["id"],
        security="IBM US Equity",
        let_str=None,
        with_params=None,
        for_str="$SECURITY",
    )

    pipeline.add_query(query=q1)

    q2 = BqlQuery(
        name="px",
        fields=["px_last"],
        security="$SECURITY",
        let_str=None,
        with_params=None,
        for_str="$SECURITY",
    )
    pipeline.add_query(query=q2, copy_from_previous=("id", "$SECURITY"))

    pipeline.execute()

    assert pipeline.successful()

    df = pipeline.dataframe()

    assert df is not None

    assert len(df) == 1

    # return df


def test_pipeline_ids_two():

    pipeline = QueryPipeline()
    q1 = BqlQuery(
        name="ids",
        fields=["id"],
        security=["IBM US Equity", "HUBS US Equity"],
        let_str=None,
        with_params=None,
        for_str="$SECURITY",
    )

    pipeline.add_query(query=q1)

    q2 = BqlQuery(
        name="px",
        fields=["px_last"],
        security="$SECURITY",
        let_str=None,
        with_params=None,
        for_str="$SECURITY",
    )
    pipeline.add_query(query=q2, copy_from_previous=("id", "$SECURITY"))

    pipeline.execute()

    assert pipeline.successful()

    df = pipeline.dataframe()

    assert df is not None

    assert len(df) == 2

    # return df


def test_pipeline_dates_four():

    pipeline = QueryPipeline()

    q1 = BqlQuery(
        name="px",
        fields=["px_last"],
        security="IBM US Equity",
        let_str=None,
        with_params="dates = '$DATE'",
        for_str="$SECURITY",
    )
    pipeline.add_query(
        query=q1, start_date="2022-01-01", end_date="2022-04-01", date_param="$DATE"
    )

    pipeline.execute()

    assert pipeline.successful()

    df = pipeline.dataframe()

    assert df is not None

    assert len(df) == 4

    # return df


def test_dates_2():
    pipeline = QueryPipeline()

    q1 = BqlQuery(
        name="px_last",
        fields=["px_last"],
        security=["IBM US Equity", "FDX US Equity"],
        let_str=None,
        with_params="dates = $DATE, fill=prev",
        for_str="$SECURITY",
    )

    pipeline.add_query(
        q1, date_param="$DATE", start_date="2012-01-01", end_date="2012-12-01"
    )

    pipeline.execute()

    assert pipeline.successful()

    df = pipeline.dataframe()

    assert df is not None
    assert len(df) == 24

    # return df


def test_pipeline_dates_four_ids_two():

    pipeline = QueryPipeline()
    q1 = BqlQuery(
        name="ids",
        fields=["id"],
        security=["IBM US Equity", "HUBS US Equity"],
        let_str=None,
        with_params=None,
        for_str="$SECURITY",
    )

    pipeline.add_query(q1)
    q2 = BqlQuery(
        name="px",
        fields=["px_last"],
        security="$SECURITY",
        let_str=None,
        with_params="dates = '$DATE'",
        for_str="$SECURITY",
    )
    pipeline.add_query(
        query=q2,
        start_date="2022-01-01",
        end_date="2022-04-01",
        date_param="$DATE",
        copy_from_previous=("id", "$SECURITY"),
    )

    pipeline.execute()
    assert pipeline.successful()

    df = pipeline.dataframe()

    assert df is not None
    assert len(df) == 8

    # return df


def test_raw_query_pipeline():
    pipeline = QueryPipeline()

    q1 = RawBqlQuery("get (id) for (['BIVIX US Equity', 'HUBS US Equity'])")
    pipeline.add_query(q1)

    q2 = RawBqlQuery("get (CUR_MKT_CAP) for (['$SECURITY'])")

    pipeline.add_query(q2, copy_from_previous=("id", "$SECURITY"))
    pipeline.execute()

    assert pipeline.successful()

    df = pipeline.dataframe()

    assert df is not None
    assert len(df) == 2

    # return df


def test_pipeline_index():

    pipeline = QueryPipeline()
    q1 = BqlQuery(
        name="ids",
        fields=["id"],
        security="translatesymbols(members('SPX Index'),TARGETIDTYPE=FUNDAMENTALTICKER)",
        let_str=None,
        with_params=None,
        for_str="$SECURITY",
    )

    pipeline.add_query(query=q1)

    q2 = BqlQuery(
        name="px",
        fields=["px_last"],
        security="$SECURITY",
        let_str=None,
        with_params=None,
        for_str="$SECURITY",
    )
    pipeline.add_query(query=q2, copy_from_previous=("id", "$SECURITY"))

    pipeline.execute()

    assert pipeline.successful()

    df = pipeline.dataframe()

    assert df is not None

    # assert len(df) == 2

    # return df


def test_raw_2():
    q = RawBqlQuery(
        "get (px_last) for (translatesymbols(members('SPX Index'),TARGETIDTYPE=FUNDAMENTALTICKER))",
    )

    success = q.execute()
    assert success

def test_bql_segment_rawquery():
    q = RawBqlQuery("get (name) for (segments('$SECURITY'))")
    q.params["$SECURITY"] = "IBM US Equity"
    success = q.execute()
    assert success


def test_bql_segment_query():

    equity = "IBM US Equity"
    q2 = BqlQuery(
        name="segs",
        fields=["sales_rev_turn"],
        security=equity,
        let_str=None,
        with_params=None,
        for_str="segments('$SECURITY')",
    )

    success = q2.execute()

    assert success


# Test field detection
def test_get_fields_1():
    q = RawBqlQuery("get (name) for (segments('$SECURITY'))")
    q.params["$SECURITY"] = "IBM US Equity"
    assert len(q.get_fields()) == 1


# Test field detection
def test_get_fields_2():
    q = RawBqlQuery("get (name, px_last) for (segments('$SECURITY'))")
    q.params["$SECURITY"] = "IBM US Equity"
    assert len(q.get_fields()) == 2


# Test field detection
def test_get_fields_3():
    q = RawBqlQuery(
        "get (name, px_last(dates=range(1,2), fill=prev), sales_rev_turn(FPT=A, FPO=-10Y) for (segments('$SECURITY'))"
    )
    q.params["$SECURITY"] = "IBM US Equity"
    assert len(q.get_fields()) == 3
