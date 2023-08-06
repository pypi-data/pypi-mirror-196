import iqmoql

import bbg_bql.bql_extension as be

def test_execute_1():
    be.register_extension_bql()

    df = be.execute_bql("get(sales_rev_turn, px_last) for ('IBM US Equity') iqmo(pivot=(id, name))")
    assert len(df)==1

def test_splitting_params():
        
    s1 = "pivot=(abc,123), splitids=true"
    results = be.split_options(s1)

    assert len(results) == 2

    s2 = "pivot=auto,splitids=true"
    results = be.split_options(s1)

    assert len(results) == 2