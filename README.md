# tap-netsuite

[Singer](https://www.singer.io/) tap that extracts data from a [NetSuite](https://www.netsuite.com/) database and produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This version of [tap-netsuitesuiteql (v0.0.1)] that maintained by the Broadvoice BI team.

```bash
$ python3 -m venv env/tap-netsuite
$ source env/tap-netsuite/bin/activate
$ pip install .
$ tap-netsuite --config config.json --discover
$ tap-netsuite --config config.json --properties properties.json --state state.json
```

# Quickstart

## Install the tap

```
> pip install tap-netsuite
```

## Create a Config file
#### Token Based Authentication
```
{
  "ns_account":"netsuite_account_id",
  "ns_consumer_key":"netsuite_consumer_key",
  "ns_consumer_secret":"netsuite_consumer_secret",
  "ns_token_key":"netsuite_token_key",
  "ns_token_secret" :"netsuite_token_secret",
  "select_fields_by_default": true,
  "is_sandbox": true / false,
  "start_date": "2019-09-02T00:00:00Z"
}
```