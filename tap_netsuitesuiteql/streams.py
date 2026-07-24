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

class CustomQueryStream(NetsuiteSuiteQLStream):
    """Ad-hoc stream driven entirely by `custom_queries.custom_query` in the tap config.

    Its schema is inferred at runtime from a sample record (see `_dynamic_schema`
    on the base class) instead of a hardcoded `_default_schema`, so it adapts to
    whatever columns the configured query returns.
    """

    name = "custom_query"
    path = ""
    _query = None
    replication_key = None
    _dynamic_schema = True

    _default_schema = th.PropertiesList().to_dict()

class CurrencyRateStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "currencyRate"
    path = ""
    _query = "SELECT BUILTIN.DF(basecurrency) AS baseCurrency, effectivedate, exchangerate, BUILTIN.DF(transactioncurrency) AS transactioncurrency FROM currencyRate WHERE effectiveDate = '" + datetime.today().strftime('%m-%d-%Y') + "'"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("basecurrency", th.StringType),
        th.Property("effectivedate", th.DateType),
        th.Property("exchangerate", th.NumberType),
        th.Property("transactioncurrency", th.StringType),

    ).to_dict()

class generalledgerStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "generalledger_v2"
    path = ""
    _query = "SELECT a.acctnumber, a.fullname, t.type AS type, s.name AS subsidiary, a.accttype AS account_type, period.startdate, period.periodName AS accounting_period, c.name AS class, d.name AS department, BUILTIN.DF(l.custcol_gocontact_market) AS market, t.trandate AS date, t.dueDate AS due_date, t.memo AS memo, l.memo AS description, l.custcol_pt_project AS project_id, t.custbody_sii_ref_no AS reference_no, t.exchangeRate AS exchange_rate, t.transactionNumber AS transaction_number, t.tranid AS document_number, t.custbody_thl_vehicle_plate AS thl_vehicle_license_plate, e.entityid AS entity_id, e.altname AS entity_name, eline.entityid AS entity_line_id, eline.altname AS entity_line, cu.symbol AS currency, COALESCE(l.creditForeignAmount,0) - COALESCE(l.debitForeignAmount,0) AS amount, l.custcol_sii_service_date AS service_date FROM transactionline l JOIN transactionAccountingLine tal ON tal.transaction = l.transaction AND tal.transactionline = l.id LEFT JOIN account a ON a.id = tal.account LEFT JOIN transaction t ON t.id = l.transaction LEFT JOIN subsidiary s ON s.id = l.subsidiary LEFT JOIN classification c ON c.id = l.class LEFT JOIN department d ON d.id = l.department LEFT JOIN entity e ON e.id = t.entity LEFT JOIN entity eline ON eline.id = l.entity LEFT JOIN currency cu ON cu.id = t.currency LEFT JOIN AccountingPeriod period ON period.id = t.postingPeriod WHERE period.startdate >= '2026-01-01' ORDER BY s.name, t.trandate, l.id"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("acctnumber", th.StringType),
        th.Property("fullname", th.StringType),
        th.Property("type", th.StringType),
        th.Property("subsidiary", th.StringType),
        th.Property("account_type", th.StringType),
        th.Property("startdate", th.DateType),
        th.Property("accounting_period", th.StringType),
        th.Property("class", th.StringType),
        th.Property("department", th.StringType),
        th.Property("market", th.StringType),
        th.Property("date", th.DateType),
        th.Property("due_date", th.DateType),
        th.Property("memo", th.StringType),
        th.Property("description", th.StringType),
        th.Property("project_id", th.StringType),
        th.Property("reference_no", th.StringType),
        th.Property("exchange_rate", th.NumberType),
        th.Property("transaction_number", th.StringType),
        th.Property("document_number", th.StringType),
        th.Property("thl_vehicle_license_plate", th.StringType),
        th.Property("entity_id", th.StringType),
        th.Property("entity_name", th.StringType),
        th.Property("entity_line_id", th.StringType),
        th.Property("entity_line", th.StringType),
        th.Property("currency", th.StringType),
        th.Property("amount", th.NumberType),
        th.Property("service_date", th.DateType),

    ).to_dict()

class TransactionLineStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transactionline"
    path = ""
    _query = "SELECT tl.debitForeignAmount, tl.expenseaccount, tl.custcol_gocontact_market, tl.transaction, tl.subsidiary, tl.class, tl.department, tl.entity, tl.memo, tl.custcol_pt_project, tl.creditForeignAmount, tl.custcol_sii_service_date, tl.id, t.lastmodifieddate FROM transactionline tl JOIN transaction t ON t.id = tl.transaction"
    replication_key = "lastmodifieddate"
    replication_filter_field = "t.lastmodifieddate"

    _default_schema = th.PropertiesList(
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

    name = "transactionlinefull"
    path = ""
    _query = "SELECT tl.debitForeignAmount, tl.expenseaccount, tl.custcol_gocontact_market, tl.transaction, tl.subsidiary, tl.class, tl.department, tl.entity, tl.memo, tl.custcol_pt_project, tl.creditForeignAmount, tl.custcol_sii_service_date, tl.id FROM transactionline tl"
    replication_key = "lastmodifieddate"
    replication_filter_field = "t.lastmodifieddate"

    _default_schema = th.PropertiesList(
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
    _query = "SELECT id, fullname, accttype, acctnumber FROM account"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("fullname", th.StringType),
        th.Property("accttype", th.StringType),
        th.Property("acctnumber", th.StringType)

    ).to_dict()

class TransactionStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transaction"
    path = ""
    _query = "SELECT t.id, t.entity, t.currency, t.type, t.trandate, t.dueDate, t.postingperiod, t.memo, t.custbody_sii_ref_no, t.exchangeRate, t.transactionNumber, t.tranid, t.custbody_thl_vehicle_plate, t.lastmodifieddate FROM transaction t ORDER BY t.id"
    replication_key = "lastmodifieddate"
    replication_filter_field = "t.lastmodifieddate"

    _default_schema = th.PropertiesList(
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
    _query = "SELECT id, name FROM subsidiary"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),

    ).to_dict()

class ClassificationStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "classification"
    path = ""
    _query = "SELECT id, name FROM classification"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),

    ).to_dict()

class DepartmentStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "department"
    path = ""
    _query = "SELECT id, name FROM department"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),

    ).to_dict()

class EntityStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "entity"
    path = ""
    _query = "SELECT id, entityid, altname FROM entity"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("entityid", th.StringType),
        th.Property("altname", th.StringType),

    ).to_dict()

class CurrencyStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "currency"
    path = ""
    _query = "SELECT id, name FROM currency"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),

    ).to_dict()

class AccountContextSearchStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountContextSearch"
    path = ""
    _query = "SELECT accountingContext, account, acctnumber FROM accountContextSearch"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("accountingcontext", th.IntegerType),
        th.Property("account", th.IntegerType),
        th.Property("acctnumber", th.StringType),

    ).to_dict()

class AccountingContextStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingContext"
    path = ""
    _query = "SELECT id, name FROM accountingContext"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
    ).to_dict()

class TransactionAccountingLineStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "transactionAccountingLine"
    path = ""
    _query = "SELECT transaction, transactionline, account, posting, accountingbook FROM transactionAccountingLine"
    replication_key = None

    _default_schema = th.PropertiesList(
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
    _query = "SELECT account, accountingbook FROM AccountAccountingBookMap"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("account", th.StringType),
        th.Property("accountingbook", th.IntegerType),

    ).to_dict()

class AccountingPeriodStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingPeriod"
    path = ""
    _query = "SELECT id, startdate, periodName FROM AccountingPeriod"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("startdate", th.DateType),
        th.Property("periodname", th.StringType),

    ).to_dict()


class AccountingBookStream(NetsuiteSuiteQLStream):
    """Define custom stream."""

    name = "accountingBook"
    path = ""
    _query = "SELECT id, name FROM AccountingBook"
    replication_key = None

    _default_schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),

    ).to_dict()

