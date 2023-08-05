# Copyright (C) 2023, IQMO Corporation [support@iqmo.com]
# All Rights Reserved
#

import iqmoql as ql
import logging

logger = logging.getLogger(__name__)



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
