"""Stream type classes for tap-netsuitesuiteql."""

from __future__ import annotations

import sys
import typing as t

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_netsuitesuiteql.client import NetsuiteSuiteQLStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

# class CurrencyRateStream(NetsuiteSuiteQLStream):
#     """Define custom stream."""

#     name = "currencyRate"
#     path = ""
#     primary_keys = ["id"]
#     query = "SELECT id, BUILTIN.DF(basecurrency) AS baseCurrency, effectivedate, exchangerate FROM currencyRate WHERE effectiveDate >= '1/1/2025' ORDER BY id"
#     replication_key = None

#     schema = th.PropertiesList(
#         th.Property("id", th.NumberType),
#         th.Property("basecurrency", th.StringType),
#         th.Property("effectivedate", th.DateType),
#         th.Property("exchangerate", th.StringType),

#     ).to_dict()

class ArrRestatementsStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "arr_restatements"
    path = ""
    primary_keys = ["id"]
    query = "SELECT R.id id, R.custrecord_prq_arr_amount arr, R.custrecord_prq_arr_start_date start_date, R.custrecord_prq_end_date end_date, R.custrecord_prq_arr_so_est so_est_id, R.created created, R.custrecord_lum_arr_amendment amendment FROM customrecord_prq_arr_restatement R WHERE isInactive='F' ORDER BY id"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("arr", th.NumberType),
        th.Property("start_date", th.DateType),
        th.Property("end_date", th.DateType),
        th.Property("created", th.DateType),
        th.Property("amendment", th.StringType),
        th.Property("so_est_id", th.NumberType),

    ).to_dict()