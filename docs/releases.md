# Releases

## Release 1.0.3

Date: 2020-03-20

Changes:

* Added support for non-blocking commands
* Added option "wait" for running command
* stdout and stderr of a command become stream
* Improved test coverage


## Release 1.0.2
Date: no date

Changes:
* By technical accident, release 1.0.2 was skipped.

## Release 1.0.1

Date: 2020-02-29

Changes:

* Enabled support for list shell commands by dir(Shell)
* Enabled command autocomplete in **BPython** and **IPython** for Shell
* Added ability to run shell commands with no-identifier-like name
* Added access to the last executed command even if exception was raised
* Added property "errors" for stderr output
* Added human-understandable behaviour for str() and repr() of Command instance
* Some internal refactoring and bugfixes
