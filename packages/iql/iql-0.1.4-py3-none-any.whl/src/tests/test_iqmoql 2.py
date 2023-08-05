# Copyright (C) 2023, IQMO Corporation [support@iqmo.com]
# All Rights Reserved
#

import iqmoql as ql
import logging

logger = logging.getLogger(__name__)


def test_v2_bql_star_fail():
    query = "select * from bql"

    # Error expected, can't select * from bql. 

def test_v2_bql():
    # Shows how we turn simple BQL into tables. 
    # Limit the bql subqueries to where clauses and from clauses. 
    query = """
        select sales_rev_turn from bql where index = 'RAY Index' and FPO='0D'"""
    
    bql = "get (sales_rev_turn) for (members('RAY Index')) with (FPO=0D)"
    
    dfs = ql.execute(query)

def test_v2_bql_chain_1():
    # Get the list of equities from the portfolio
    query = """
        select * from
        (select * from bql_portfolio where id='u123:2') q1
        join
        (select id, px_last from equities) q2 on q2.id=q1.id
        """
    dfs = ql.execute(query)

def test_v2_bql_s3api_chain():
    # get Q1 first, then pass id's to s3api:
    query = """
        select * from
        (select sales_rev_turn from bql where index = 'RAY Index' and FPO='0D' and sales_rev_turn>10000) q1
        join s3api on s3api.id = q1.id
        """
    
    # Consider lateral queries:
    #https://www.cybertec-postgresql.com/en/understanding-lateral-joins-in-postgresql/
    dfs = ql.execute(query)

def test_v2_eu():
    query = "select * from bql_equityuniv where index = 'IBM US Equity'"
    dfs = ql.execute(query)

def test_v2_is():
    query = "select * from bql_incomestatement where id = 'IBM US Equity'"
    dfs = ql.execute(query)


def test_v2_bs():
    query = "select * from bql_incomestatement where id = 'IBM US Equity'"
    dfs = ql.execute(query)
