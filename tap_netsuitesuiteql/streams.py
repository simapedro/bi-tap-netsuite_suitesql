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

class CurrencyRateStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "currencyRate"
    primary_keys = ["id"]
    query = "SELECT id, BUILTIN.DF(basecurrency) AS baseCurrency, effectivedate, exchangerate FROM currencyRate WHERE effectiveDate >= '1/1/2025' ORDER BY id"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.NumberType),
        th.Property("basecurrency", th.StringType),
        th.Property("effectivedate", th.DateType),
        th.Property("exchangerate", th.StringType),

    ).to_dict()