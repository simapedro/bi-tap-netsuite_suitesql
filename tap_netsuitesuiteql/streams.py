"""Stream type classes for tap-netsuitesuiteql."""

from __future__ import annotations

import sys
import typing as t

from datetime import datetime

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
#     query = "SELECT id, BUILTIN.DF(basecurrency) AS baseCurrency, effectivedate, exchangerate FROM currencyRate WHERE effectiveDate = '2/20/2025' ORDER BY id"
#     # query = "SELECT id, BUILTIN.DF(basecurrency) AS baseCurrency, effectivedate, exchangerate FROM currencyRate WHERE effectiveDate = '" + datetime.today().strftime('%m-%d-%Y') + "' ORDER BY id"
#     replication_key = None

#     schema = th.PropertiesList(
#         th.Property("id", th.NumberType),
#         th.Property("basecurrency", th.StringType),
#         th.Property("effectivedate", th.DateType),
#         th.Property("exchangerate", th.StringType),

#     ).to_dict()

class RenewalItemsStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "renewal_items"
    path = ""
    primary_keys = ["id"]
    query = "select id, itemid, displayname from item ORDER BY id"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.NumberType),
        th.Property("itemid", th.StringType),
        th.Property("displayname", th.StringType),

    ).to_dict()
