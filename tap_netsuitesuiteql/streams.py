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

class CurrencyRateStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "currencyRate"
    path = ""
    query = "SELECT BUILTIN.DF(basecurrency) AS baseCurrency, effectivedate, exchangerate, BUILTIN.DF(transactioncurrency) AS transactioncurrency FROM currencyRate WHERE effectiveDate = '" + datetime.today().strftime('%m-%d-%Y') + "'"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("basecurrency", th.StringType),
        th.Property("effectivedate", th.DateType),
        th.Property("exchangerate", th.StringType),
        th.Property("transactioncurrency", th.StringType),

    ).to_dict()

class TransactionLineStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transactionline"
    path = ""
    query = "SELECT memo, custcol_pt_project, creditForeignAmount, custcol_sii_service_date FROM transactionLine"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("memo", th.StringType),
        th.Property("custcol_pt_project", th.StringType),
        th.Property("creditForeignAmount", th.StringType),
        th.Property("custcol_sii_service_date", th.DateType),

    ).to_dict()

class AccountStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "account"
    path = ""
    query = "SELECT fullname, accttype FROM account"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("fullname", th.StringType),
        th.Property("accttype", th.StringType),

    ).to_dict()

class TransactionStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transaction"
    path = ""
    query = "SELECT type, trandate, dueDate, memo, custbody_sii_ref_no, exchangeRate, transactionNumber, tranid, custbody_thl_vehicle_plate FROM transaction"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("type", th.StringType),
        th.Property("trandate", th.DateType),
        th.Property("dueDate", th.DateType),
        th.Property("memo", th.StringType),
        th.Property("custbody_sii_ref_no", th.StringType),
        th.Property("exchangeRate", th.StringType),
        th.Property("transactionNumber", th.StringType),
        th.Property("tranid", th.StringType),
        th.Property("custbody_thl_vehicle_plate", th.StringType)

    ).to_dict()


class SubsidiaryStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "subsidiary"
    path = ""
    query = "SELECT name FROM subsidiary"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("name", th.StringType)

    ).to_dict()

class ClassificationStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "classification"
    path = ""
    query = "SELECT name FROM classification"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("name", th.StringType)

    ).to_dict()

class DepartmentStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "department"
    path = ""
    query = "SELECT name FROM department"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("name", th.StringType)

    ).to_dict()

class EntityStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "entity"
    path = ""
    query = "SELECT entityid, altname FROM entity"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("entityid", th.StringType),
        th.Property("altname", th.StringType)

    ).to_dict()

class CurrencyStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "currency"
    path = ""
    query = "SELECT name FROM currency"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("name", th.StringType)

    ).to_dict()

class AccountContextSearchStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountContextSearch"
    path = ""
    query = "SELECT acctNumber FROM accountContextSearch"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("acctNumber", th.StringType)

    ).to_dict()

class AccountingContextStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingContext"
    path = ""
    query = "SELECT id FROM accountingContext"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType)

    ).to_dict()

class TransactionAccountingLineStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transactionAccountingLine"
    path = ""
    query = "SELECT transaction, transactionLine FROM transactionAccountingLine"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("transaction", th.StringType)
        th.Property("transactionLine", th.StringType)

    ).to_dict()