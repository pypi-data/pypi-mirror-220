# APC_Temp_fetch

This python package provides an unified interface to several UPS
network adapters with different firmware versions. It does not
support guessing which interface to use; that wasn't necessary yet.

It supports the following interfaces:
| `kind` | `description` |
|--------|---------------|
| `old`  | Simple interface using HTTP basic auth, information gets extracted from `upsstat.htm`, by finding the line mentioning `Internal Temperature` |
| `frmnc` | Requires 2 HTTP requests, main characteristics are that the login form is named `frmLogin` in HTML, and the data is presented in a `<div>`-table, but parsable line-by-line |
| `frmnc666` | Similar to `frmnc`; with 3 HTTP requests, but the status page is named `upstat.htm` (which makes the additional HTTP request necessary) |
| `gden-nt07` | Similar to `frmnc`; with 3 HTTP requests, but the login form is named `HashForm1` instead, and the data representation is more complex, so a more full-blown HTML-parser is used; data structured via `<span>` items |
| `cs121` | Unauthenticated HTTP API (simply pass `- -` as `<user> <password>`), information gets extracted from `main.shtml`, by parsing `_dw` and `&nbsp;` from an HTML table, line-by-line |
| `cs141` | Simple JSON API (and the imo best interface of these); with 3 HTTP requests, characteristic is the the data is located at `/api/devices/ups/report` |

The description provides some guidance which `kind` an interface is.
You may also just try out each `kind` and check if any returns useful results,
but (although unlikely) it may "brick" the network adapter until it is reset;
usually seen when (thru some bug) the script isn't able to properly logout
after a successful login, because many of these network adapters limit the
number of concurrent logins, often to even just 1 user at a time.

This package has 2 entry points:
* `APC_Tempf [--verbose] [--proxy <proxy_url>] <kind> <host> <user> <password> [--timeout <timeout>]`
  `kind` is the one of these mentioned above.
  `host`, `user` and `password` should be self-explanatory.
  `timeout` is an optional per-request timeout.
  This is the primary, "simple" interface.

* `APC_Tempstfe [--verbose] [--proxy <proxy_url>] <apclist>`
  allows querying multiple UPS devices sequentially, and is used to
  amortize the python script startup time.
  The file should contain lines of the format `<kind> <host> <user> <password>[ <timeout>]`
  (all without the `<>` brackets).
  After the timeout, a comment may be given, or a comment can be alternatively placed
  at the begging of a line, prefixed with a `# `; empty lines are ignored.

Results are formatted as `<host>\t<temperature>` (`<>` brackets aren't part of the output,
`\t` is replaced with an ASCII TAB character).

## proxy support

If required, `--proxy <proxy_url>` can be added to the entry point command line
to contact all API endpoints through the specified proxy.
Note that this might require `pip3 install 'requests[socks]'` or
on Gentoo `USE="socks5" emerge -v dev-python/requests` to work with SOCKS proxies.

When using the python API, proxies can be specified in the `ApcKind.__init__(_, rqa)`
`rqa` parameter (see Requests documentation, or the source code in `cli.py`)
