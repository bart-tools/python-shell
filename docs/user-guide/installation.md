# Installation

The python-shell library is developed as "pythonic" as possible, so
does not require any additional non-Python dependencies.

To install it, you need **pip** installed in the system.

Then simply run
```
pip install python-shell
```

## Supported Python versions

This library supports the next Python versions:

| Version | Supported |
|:-------:|:---------:|
| 2.5     |    No     |
| 2.6     |    No     |
| 2.7     | **Yes**   |
|         |           |
| 3.0     |    No     |
| 3.1     |    No     |
| 3.2     |    No     |
| 3.3     |    No     |
| 3.4     |    No     |
| 3.5     | **Yes**   |
| 3.6     | **Yes**   |
| 3.7     | **Yes**   |
| 3.8     | **Yes**   |

Support for coming new versions is obvious, but there will be no
additional compatibility with old versions listed in the table.
There're few simple points for that:
1. Some huge and old projects with tons of legacy code written in Python 2
   should be surely working on 2.7. If not, then it's a good chance
   to do so - I see no particular reason for keeping 2.6 or older.
1. Projects which use Python 3 should use at least 3.5. Still, I see
   no reason for keeping older versions, as they do not have lots of
   useful things and are dangerous in general.
