# Ocient Database Python API

This python database API conforms to the Python Database API
Specification 2.0 and can be used to access the Ocient database.

This module can also be called as a main function, in which case
it acts as a CLI for the database.

When called as main, it a connection string in DSN (data source name)
format, followed by zero or more query strings that will be executed.
Output is returned in JSON format.

The Ocient DSN is of the format:
   `ocient://user:password@[host][:port][/database][?param1=value1&...]`

`user` and `password` must be supplied.  `host` defaults to localhost,
port defaults to 4050, database defaults to `system` and `tls` defaults
to `unverified`.

Currently supported parameters are:

- tls: Which can have the values "off", "unverified", or "on"
- force: Which can have the values "true"
- handshake: Which can have the value "cbc", "gcm", or "sso"

For the handshake protocols, "cbc" (Cipher Block Chaining) denotes a previous password encryption protocol which
should be avoided. "gcm" (Galois/Counter Mode), which pyocient will default to, is recommended. If single sign
on is desired, then "sso" should be used.

Release notes are available at https://github.com/ocient/pyocient_release/
