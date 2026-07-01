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
        th.Property("exchangerate", th.NumberType),
        th.Property("transactioncurrency", th.StringType),

    ).to_dict()

class TransactionLineStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transactionline"
    path = ""
    query = "SELECT tl.expenseaccount, tl.custcol_gocontact_market, tl.transaction, tl.subsidiary, tl.class, tl.department, tl.entity, tl.memo, tl.custcol_pt_project, tl.creditForeignAmount, tl.custcol_sii_service_date, t.last_sync_timestamp FROM transactionline tl JOIN transaction t ON t.id = tl.transaction"
    replication_key = "last_sync_timestamp"
    replication_filter_field = "t.last_sync_timestamp"

    schema = th.PropertiesList(
        th.Property("expenseaccount", th.StringType),   
        th.Property("custcol_gocontact_market", th.StringType),
        th.Property("transaction", th.StringType),
        th.Property("subsidiary", th.StringType),
        th.Property("class", th.StringType),
        th.Property("department", th.StringType),
        th.Property("entity", th.StringType),
        th.Property("memo", th.StringType),
        th.Property("custcol_pt_project", th.StringType),
        th.Property("creditForeignAmount", th.NumberType),
        th.Property("custcol_sii_service_date", th.DateType),
        th.Property("last_sync_timestamp", th.DateTimeType),
    ).to_dict()

class AccountStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "account"
    path = ""
    query = "SELECT id, fullname, accttype FROM account"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("fullname", th.StringType),
        th.Property("accttype", th.StringType),

    ).to_dict()

class TransactionStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transaction"
    path = ""
    query = "SELECT t.id, t.entity, t.currency, t.type, t.trandate, t.dueDate, t.postingperiod, t.memo, t.custbody_sii_ref_no, t.exchangeRate, t.transactionNumber, t.tranid, t.custbody_thl_vehicle_plate, t.last_sync_timestamp FROM transaction t"
    replication_key = "last_sync_timestamp"
    replication_filter_field = "t.last_sync_timestamp"

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("entity", th.StringType),
        th.Property("currency", th.StringType),
        th.Property("type", th.StringType),
        th.Property("trandate", th.DateType),
        th.Property("postingperiod", th.StringType),
        th.Property("dueDate", th.DateType),
        th.Property("memo", th.StringType),
        th.Property("custbody_sii_ref_no", th.StringType),
        th.Property("exchangeRate", th.StringType),
        th.Property("transactionNumber", th.StringType),
        th.Property("tranid", th.StringType),
        th.Property("custbody_thl_vehicle_plate", th.StringType),
        th.Property("last_sync_timestamp", th.DateTimeType),

    ).to_dict()


class SubsidiaryStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "subsidiary"
    path = ""
    query = "SELECT id, name FROM subsidiary"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),

    ).to_dict()

class ClassificationStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "classification"
    path = ""
    query = "SELECT id, name FROM classification"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),

    ).to_dict()

class DepartmentStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "department"
    path = ""
    query = "SELECT id, name FROM department"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),

    ).to_dict()

class EntityStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "entity"
    path = ""
    query = "SELECT id, entityid, altname FROM entity"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("entityid", th.StringType),
        th.Property("altname", th.StringType),

    ).to_dict()

class CurrencyStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "currency"
    path = ""
    query = "SELECT id, name FROM currency"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),

    ).to_dict()

class AccountContextSearchStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountContextSearch"
    path = ""
    query = "SELECT accountingContext, account, acctnumber FROM accountContextSearch"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("AccountingContext", th.NumberType),
        th.Property("account", th.StringType),
        th.Property("acctnumber", th.StringType),

    ).to_dict()

class AccountingContextStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingContext"
    path = ""
    query = "SELECT id FROM accountingContext"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),

    ).to_dict()

class TransactionAccountingLineStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transactionAccountingLine"
    path = ""
    query = "SELECT transaction, transactionLine FROM transactionAccountingLine"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("transaction", th.StringType),
        th.Property("transactionLine", th.StringType),

    ).to_dict()

class AccountAccountingBookMapStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountAccountingBookMap"
    path = ""
    query = "SELECT account, accountingbook FROM AccountAccountingBookMap"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("account", th.StringType),
        th.Property("accountingbook", th.StringType),

    ).to_dict()

class AccountingPeriodStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingPeriod"
    path = ""
    query = "SELECT id, startdate, periodName FROM AccountingPeriod"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("startdate", th.StringType),
        th.Property("periodName", th.StringType),

    ).to_dict()


class AccountingBookStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingBook"
    path = ""
    query = "SELECT id, name FROM AccountingBook"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),

    ).to_dict()

