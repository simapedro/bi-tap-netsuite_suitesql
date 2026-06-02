"""REST client handling, including NetsuiteSuiteQLStream base class."""

from __future__ import annotations

import sys
from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING, Any, Iterable

import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseAPIPaginator, BaseOffsetPaginator  # noqa: TCH002
from singer_sdk.streams import RESTStream
import logging

from tap_netsuitesuiteql.auth import NetsuiteSuiteQLAuthenticator

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

if TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class NetsuiteSuiteQLStream(RESTStream):
    """NetsuiteSuiteQL stream class."""
    rest_method = "POST"

    records_jsonpath = "$.items[*]"
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    query = None
    # Column expression used in the incremental WHERE filter (e.g. "t.trandate").
    # Must be set on streams that define a replication_key.
    replication_filter_field: str | None = None

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config["url"]

    @cached_property
    def authenticator(self) -> NetsuiteSuiteQLAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return NetsuiteSuiteQLAuthenticator(
            realm=self.config["realm"],
            client_key=self.config["client_key"],
            client_secret=self.config["client_secret"],
            resource_owner_key=self.config["resource_owner_key"],
            resource_owner_secret=self.config["resource_owner_secret"],
        )

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {'prefer': 'transient','Content-Type': 'application/json'}
        return headers

    def get_new_paginator(self) -> BaseOffsetPaginator:
        return BaseOffsetPaginator(start_value=0, page_size=5000)

    def _get_start_date_for_query(self, context: Context | None) -> str | None:
        """Return the incremental start date formatted for SuiteQL (MM/DD/YYYY)."""
        start_value = self.get_starting_replication_key_value(context)
        if start_value is None:
            return None
        if isinstance(start_value, datetime):
            return start_value.strftime("%m/%d/%Y")
        if isinstance(start_value, str):
            for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(start_value[:len(fmt)], fmt).strftime("%m/%d/%Y")
                except ValueError:
                    continue
        return str(start_value)

    def _build_filtered_query(self, context: Context | None) -> str:
        """Build the SuiteQL query, appending an incremental date filter when applicable."""
        query = self.query
        if self.replication_key and self.replication_filter_field:
            start_date = self._get_start_date_for_query(context)
            if start_date:
                connector = "AND" if "WHERE" in query.upper() else "WHERE"
                query = f"{query} {connector} {self.replication_filter_field} >= '{start_date}'"
        return query

    def prepare_request_payload(
        self,
        context: Context | None,
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict | None:
        query = self._build_filtered_query(context)
        if next_page_token:
            offset = next_page_token
            query = f"SELECT * from (SELECT  *, rownum as r FROM ( {query} )) WHERE r BETWEEN {offset} and {offset + 4999}"
        return {"q": query}
    
    def validate_response(self, response):
        if not response.ok:
            try:
                error_details = response.json()
            except Exception:
                error_details = response.text
            logging.error(f"API Error: {response.status_code} - {error_details}")
            response.raise_for_status()

    def request_records(self, context: "Context | None") -> Iterable[dict]:
        try:
            yield from super().request_records(context)
        except Exception as e:
            logging.error(f"Stream '{self.name}' failed and will be skipped. Error: {e}")
            return

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())
