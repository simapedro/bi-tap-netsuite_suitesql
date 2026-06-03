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
    query = "SELECT tl.memo, tl.custcol_pt_project, tl.creditForeignAmount, tl.custcol_sii_service_date, t.trandate FROM transactionline AS tl LEFT JOIN transaction t ON t.id = tl.transaction"
    replication_key = "trandate"
    replication_filter_field = "t.trandate"

    schema = th.PropertiesList(
        th.Property("memo", th.StringType),
        th.Property("custcol_pt_project", th.StringType),
        th.Property("creditForeignAmount", th.StringType),
        th.Property("custcol_sii_service_date", th.DateType),
        th.Property("trandate", th.DateType),

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
    query = "SELECT t.type, t.trandate, t.dueDate, t.memo, t.custbody_sii_ref_no, t.exchangeRate, t.transactionNumber, t.tranid, t.custbody_thl_vehicle_plate FROM transaction t"
    replication_key = "trandate"
    replication_filter_field = "t.trandate"

    schema = th.PropertiesList(
        th.Property("type", th.StringType),
        th.Property("trandate", th.DateType),
        th.Property("dueDate", th.DateType),
        th.Property("memo", th.StringType),
        th.Property("custbody_sii_ref_no", th.StringType),
        th.Property("exchangeRate", th.StringType),
        th.Property("transactionNumber", th.StringType),
        th.Property("tranid", th.StringType),
        th.Property("custbody_thl_vehicle_plate", th.StringType),

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
    query = "SELECT entityid, altname FROM entity"
    replication_key = None

    schema = th.PropertiesList(
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
    query = "SELECT account, acctnumber FROM accountContextSearch"
    replication_key = None

    schema = th.PropertiesList(
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

class GeneralLedgerStream(NetsuiteSuiteQLStream):
    """General ledger stream joining transaction lines with accounts, periods, subsidiaries and entities."""

    name = "generalLedger"
    path = ""
    replication_key = "date"
    replication_filter_field = "t.trandate"
    query = """SELECT DISTINCT
    search.acctNumber AS account_line_number,
    a.fullname AS name,
    t.type AS type,
    s.name AS subsidiary,
    a.accttype AS account_type,
    period.periodName AS accounting_period,
    c.name AS class,
    d.name AS department,
    BUILTIN.DF(l.custcol_gocontact_market) AS market,
    t.trandate AS date,
    t.dueDate AS due_date,
    t.memo AS memo,
    l.memo AS description,
    l.custcol_pt_project AS project_id,
    t.custbody_sii_ref_no AS reference_no,
    t.exchangeRate AS exchange_rate,
    t.transactionNumber AS transaction_number,
    t.tranid AS document_number,
    t.custbody_thl_vehicle_plate AS thl_vehicle_license_plate,
    e.entityid AS entity_id,
    e.altname AS entity_name,
    eline.entityid AS entity_line_id,
    eline.altname AS entity_line,
    cu.name AS currency,
    l.creditForeignAmount AS amount,
    l.custcol_sii_service_date AS service_date
FROM
    transactionline l
    LEFT JOIN account a ON a.id = l.expenseaccount
    LEFT JOIN transaction t ON t.id = l.transaction
    LEFT JOIN subsidiary s ON s.id = l.subsidiary
    LEFT JOIN classification c ON c.id = l.class
    LEFT JOIN department d ON d.id = l.department
    LEFT JOIN entity e ON e.id = t.entity
    LEFT JOIN entity eline ON eline.id = l.entity
    LEFT JOIN currency cu ON cu.id = t.currency
    LEFT JOIN AccountContextSearch search ON search.account = a.id
    LEFT JOIN AccountingContext context ON context.id = search.AccountingContext
    LEFT JOIN AccountingPeriod period ON period.id = t.postingPeriod
    LEFT JOIN AccountAccountingBookMap abm ON abm.account = a.id
    LEFT JOIN AccountingBook book ON book.id = abm.accountingbook
WHERE
    context.id = 1
    AND period.startdate BETWEEN '2026-01-01' AND '2026-03-01'
    AND s.id = 5
    AND (book.id IS NULL OR book.id = 4)
ORDER BY t.trandate"""

    schema = th.PropertiesList(
        th.Property("account_line_number", th.StringType),
        th.Property("name", th.StringType),
        th.Property("type", th.StringType),
        th.Property("subsidiary", th.StringType),
        th.Property("account_type", th.StringType),
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
        th.Property("exchange_rate", th.StringType),
        th.Property("transaction_number", th.StringType),
        th.Property("document_number", th.StringType),
        th.Property("thl_vehicle_license_plate", th.StringType),
        th.Property("entity_id", th.StringType),
        th.Property("entity_name", th.StringType),
        th.Property("entity_line_id", th.StringType),
        th.Property("entity_line", th.StringType),
        th.Property("currency", th.StringType),
        th.Property("amount", th.StringType),
        th.Property("service_date", th.DateType),
    ).to_dict()