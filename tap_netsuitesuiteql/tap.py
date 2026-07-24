"""NetsuiteSuiteQL tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_netsuitesuiteql import streams


class TapNetsuiteSuiteQL(Tap):
    """NetsuiteSuiteQL tap class."""

    name = "tap-netsuitesuiteql"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "realm",
            th.IntegerType,
            required=True,
        ),
        th.Property(
            "client_key",
            th.StringType,
            required=True,
        ),
        th.Property(
            "client_secret",
            th.StringType,
            secret=True,
        ),
        th.Property(
            "resource_owner_key",
            th.StringType,
            description="The url for the API service",
        ),
        th.Property(
            "resource_owner_secret",
            th.StringType,
            secret=True,
        ),
        th.Property(
            "url",
            th.StringType,
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Earliest date to extract data from (ISO format, e.g. 2024-01-01). Used on first run; subsequent runs use the saved bookmark.",
        ),
        th.Property(
            "custom_queries",
            th.ObjectType(),
            description=(
                "Map of stream name to a SuiteQL query that overrides the stream's built-in query, "
                "e.g. {'generalledger_v2': 'SELECT ...'}. Also used to supply the query for the "
                "'custom_query' stream, which has no built-in query of its own and infers its schema "
                "dynamically from the query's results, e.g. {'custom_query': 'SELECT ...'}."
            ),
        ),
        th.Property(
            "custom_schema",
            th.ObjectType(),
            description=(
                "Map of stream name to {field_name: json_type} entries that extend/override that "
                "stream's schema, e.g. {'generalledger_v2': {'novo_campo': 'string'}}. Valid json_type "
                "values: string, integer, number, boolean, date, date-time."
            ),
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.NetsuiteSuiteQLStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.CurrencyRateStream(self),
            streams.TransactionLineStream(self),
            streams.AccountStream(self),
            streams.TransactionStream(self),
            streams.SubsidiaryStream(self),
            streams.ClassificationStream(self),
            streams.DepartmentStream(self),
            streams.EntityStream(self),
            streams.CurrencyStream(self),
            streams.AccountContextSearchStream(self),
            streams.AccountingContextStream(self),
            streams.TransactionAccountingLineStream(self),
            streams.AccountingBookStream(self),
            streams.AccountingPeriodStream(self),
            streams.AccountAccountingBookMapStream(self),
            streams.TransactionLineFullStream(self),
            streams.generalledgerStream(self),
            streams.CustomQueryStream(self),
        ]


if __name__ == "__main__":
    TapNetsuiteSuiteQL.cli()
