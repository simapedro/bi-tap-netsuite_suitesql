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

# Maps the simple type names accepted in the `custom_schema` tap config to
# their JSON Schema representation.
_CUSTOM_SCHEMA_TYPE_MAP = {
    "string": {"type": ["string", "null"]},
    "integer": {"type": ["integer", "null"]},
    "number": {"type": ["number", "null"]},
    "boolean": {"type": ["boolean", "null"]},
    "date": {"type": ["string", "null"], "format": "date"},
    "date-time": {"type": ["string", "null"], "format": "date-time"},
}


_UNSET = object()


def _infer_json_schema_type(value: Any) -> dict:
    """Infer a JSON Schema type dict from a sample Python value."""
    if isinstance(value, bool):
        return {"type": ["boolean", "null"]}
    if isinstance(value, int):
        return {"type": ["integer", "null"]}
    if isinstance(value, float):
        return {"type": ["number", "null"]}
    return {"type": ["string", "null"]}


class NetsuiteSuiteQLStream(RESTStream):
    """NetsuiteSuiteQL stream class."""
    rest_method = "POST"

    records_jsonpath = "$.items[*]"
    next_page_token_jsonpath = "$.next_page"  # noqa: S105

    _query = None
    # When True, `schema` is inferred at runtime from a sample record instead
    # of relying on `_default_schema`. Used by streams whose query is only
    # known via the `custom_queries` tap config (e.g. CustomQueryStream).
    _dynamic_schema: bool = False
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
        return BaseOffsetPaginator(start_value=0, page_size=1000)

    def _get_start_date_for_query(self, context: Context | None) -> str | None:
        """Return the incremental start date formatted for SuiteQL's TO_DATE (YYYY-MM-DD HH24:MI:SS)."""
        start_value = self.get_starting_replication_key_value(context)
        if start_value is None:
            return None
        if isinstance(start_value, datetime):
            dt = start_value
        elif isinstance(start_value, str):
            try:
                dt = datetime.fromisoformat(start_value.replace("Z", "+00:00"))
            except ValueError:
                return None
        else:
            return None
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    @property
    def query(self) -> str:
        """Return the query for this stream, allowing override via the `custom_queries` tap config."""
        return self.config.get("custom_queries", {}).get(self.name, self._query)

    @query.setter
    def query(self, value: str) -> None:
        self._query = value

    _cached_sample_record: Any = _UNSET

    @property
    def _sample_record(self) -> dict | None:
        """Fetch a single record to infer a dynamic schema from (see `_dynamic_schema`).

        Skips (without caching) if called before RESTStream.__init__ has set up
        `_requests_session` — this happens because singer_sdk's Stream.__init__
        checks `self.schema` before RESTStream.__init__ finishes, and a dynamic
        schema stream needs a live HTTP session to answer that. Only a real
        attempt (success or genuine failure) gets memoized, so `schema` retries
        cleanly once the stream is fully initialized.
        """
        if getattr(self, "_requests_session", None) is None:
            return None
        if not self.query:
            return None
        if self._cached_sample_record is _UNSET:
            try:
                self._cached_sample_record = next(iter(self.request_records(context=None)), None)
            except Exception:
                logging.exception(
                    f"Stream '{self.name}' failed to fetch a sample record for schema inference."
                )
                self._cached_sample_record = None
        return self._cached_sample_record

    @property
    def schema(self) -> dict:
        """Return the JSON schema for this stream, extended with any `custom_schema` fields from tap config."""
        if self._dynamic_schema:
            sample = self._sample_record
            properties = (
                {field: _infer_json_schema_type(value) for field, value in sample.items()}
                if sample
                else {}
            )
            schema = {"type": "object", "properties": properties}
        else:
            schema = dict(self._default_schema)
        overrides = self.config.get("custom_schema", {}).get(self.name)
        if overrides:
            properties = {**schema.get("properties", {})}
            for field_name, json_type in overrides.items():
                properties[field_name] = _CUSTOM_SCHEMA_TYPE_MAP.get(
                    json_type, {"type": ["string", "null"]}
                )
            schema = {**schema, "properties": properties}
        return schema

    def _build_filtered_query(self, context: Context | None) -> str:
        """Build the SuiteQL query, appending an incremental date filter when applicable."""
        query = self.query
        if self.replication_key and self.replication_filter_field:
            start_date = self._get_start_date_for_query(context)
            if start_date:
                connector = "AND" if "WHERE" in query.upper() else "WHERE"
                query = (
                    f"{query} {connector} {self.replication_filter_field} "
                    f">= TO_DATE('{start_date}', 'YYYY-MM-DD HH24:MI:SS')"
                )
        return query

    def prepare_request_payload(
        self,
        context: Context | None,
        next_page_token: Any | None,  # noqa: ANN401
    ) -> dict | None:
        query = self._build_filtered_query(context)
        if next_page_token is not None:   # antes: "if next_page_token:" — 0 (primeira página) era ignorado
            offset = next_page_token
            query = f"SELECT * from (SELECT  *, rownum as r FROM ( {query} )) WHERE r BETWEEN {offset} and {offset + 999}"
        logging.info(f"SuiteQL request for stream '{self.name}': {query!r}")
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
            logging.exception(f"Stream '{self.name}' failed and will be skipped. Error: {e}")
            return

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        for record in extract_jsonpath(self.records_jsonpath, input=response.json()):
            # SuiteQL returns unquoted column/alias names normalized to lowercase,
            # regardless of the casing used in the query. Normalize here so record
            # keys reliably match the (lowercase) schema property names.
            yield {key.lower(): value for key, value in record.items()}
