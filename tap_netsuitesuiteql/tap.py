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
        ]


if __name__ == "__main__":
    TapNetsuiteSuiteQL.cli()
