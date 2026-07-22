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
    query = "SELECT tl.debitForeignAmount, tl.expenseaccount, tl.custcol_gocontact_market, tl.transaction, tl.subsidiary, tl.class, tl.department, tl.entity, tl.memo, tl.custcol_pt_project, tl.creditForeignAmount, tl.custcol_sii_service_date, tl.id, t.lastmodifieddate FROM transactionline tl JOIN transaction t ON t.id = tl.transaction"
    replication_key = "lastmodifieddate"
    replication_filter_field = "t.lastmodifieddate"

    schema = th.PropertiesList(
        th.Property("debitForeignAmount", th.NumberType),
        th.Property("expenseaccount", th.IntegerType),   
        th.Property("custcol_gocontact_market", th.IntegerType),
        th.Property("transaction", th.IntegerType),
        th.Property("subsidiary", th.IntegerType),
        th.Property("class", th.IntegerType),
        th.Property("department", th.IntegerType),
        th.Property("entity", th.IntegerType),
        th.Property("memo", th.StringType),
        th.Property("custcol_pt_project", th.StringType),
        th.Property("creditforeignamount", th.NumberType),
        th.Property("custcol_sii_service_date", th.DateType),
        th.Property("id", th.IntegerType),
        th.Property("lastmodifieddate", th.DateTimeType),
    ).to_dict()

class TransactionLineFullStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transactionline"
    path = ""
    query = "SELECT tl.debitForeignAmount, tl.expenseaccount, tl.custcol_gocontact_market, tl.transaction, tl.subsidiary, tl.class, tl.department, tl.entity, tl.memo, tl.custcol_pt_project, tl.creditForeignAmount, tl.custcol_sii_service_date, tl.id FROM transactionline tl"
    replication_key = "lastmodifieddate"
    replication_filter_field = "t.lastmodifieddate"

    schema = th.PropertiesList(
        th.Property("debitForeignAmount", th.NumberType),
        th.Property("expenseaccount", th.IntegerType),   
        th.Property("custcol_gocontact_market", th.IntegerType),
        th.Property("transaction", th.IntegerType),
        th.Property("subsidiary", th.IntegerType),
        th.Property("class", th.IntegerType),
        th.Property("department", th.IntegerType),
        th.Property("entity", th.IntegerType),
        th.Property("memo", th.StringType),
        th.Property("custcol_pt_project", th.StringType),
        th.Property("creditforeignamount", th.NumberType),
        th.Property("custcol_sii_service_date", th.DateType),
        th.Property("id", th.IntegerType),
    ).to_dict()

class AccountStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "account"
    path = ""
    query = "SELECT id, fullname, accttype, acctnumber FROM account"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("fullname", th.StringType),
        th.Property("accttype", th.StringType),
        th.Property("acctnumber", th.StringType)

    ).to_dict()

class TransactionStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transaction"
    path = ""
    query = "SELECT t.id, t.entity, t.currency, t.type, t.trandate, t.dueDate, t.postingperiod, t.memo, t.custbody_sii_ref_no, t.exchangeRate, t.transactionNumber, t.tranid, t.custbody_thl_vehicle_plate, t.lastmodifieddate FROM transaction t ORDER BY t.id"
    replication_key = "lastmodifieddate"
    replication_filter_field = "t.lastmodifieddate"

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("entity", th.IntegerType),
        th.Property("currency", th.IntegerType),
        th.Property("type", th.StringType),
        th.Property("trandate", th.DateType),
        th.Property("postingperiod", th.IntegerType),
        th.Property("duedate", th.DateType),
        th.Property("memo", th.StringType),
        th.Property("custbody_sii_ref_no", th.StringType),
        th.Property("exchangerate", th.NumberType),
        th.Property("transactionnumber", th.StringType),
        th.Property("tranid", th.StringType),
        th.Property("custbody_thl_vehicle_plate", th.StringType),
        th.Property("lastmodifieddate", th.DateTimeType),

    ).to_dict()


class SubsidiaryStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "subsidiary"
    path = ""
    query = "SELECT id, name FROM subsidiary"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),

    ).to_dict()

class ClassificationStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "classification"
    path = ""
    query = "SELECT id, name FROM classification"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),

    ).to_dict()

class DepartmentStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "department"
    path = ""
    query = "SELECT id, name FROM department"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),

    ).to_dict()

class EntityStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "entity"
    path = ""
    query = "SELECT id, entityid, altname FROM entity"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
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
        th.Property("accountingcontext", th.IntegerType),
        th.Property("account", th.IntegerType),
        th.Property("acctnumber", th.StringType),

    ).to_dict()

class AccountingContextStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingContext"
    path = ""
    query = "SELECT id, name FROM accountingContext"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
    ).to_dict()

class TransactionAccountingLineStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transactionAccountingLine"
    path = ""
    query = "SELECT transaction, transactionline, account, posting, accountingbook FROM transactionAccountingLine"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("transaction", th.IntegerType),
        th.Property("transactionline", th.IntegerType),
        th.Property("account", th.IntegerType),
        th.Property("posting", th.BooleanType),
        th.Property("accountingbook", th.IntegerType),

    ).to_dict()

class AccountAccountingBookMapStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountAccountingBookMap"
    path = ""
    query = "SELECT account, accountingbook FROM AccountAccountingBookMap"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("account", th.StringType),
        th.Property("accountingbook", th.IntegerType),

    ).to_dict()

class AccountingPeriodStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingPeriod"
    path = ""
    query = "SELECT id, startdate, periodName FROM AccountingPeriod"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("startdate", th.DateType),
        th.Property("periodname", th.StringType),

    ).to_dict()


class AccountingBookStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingBook"
    path = ""
    query = "SELECT id, name FROM AccountingBook"
    replication_key = None

    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),

    ).to_dict()

