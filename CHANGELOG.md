# Changes

### 2020-03-06

* Added support for Python 3.9 and PyPy
* Added proper documentation (based on mkdocs)
* Added property _is_undefined_ for processes
* Added `__version__` for the root package
* Refactoring in exception classes
* Added usage of **flake8** in Tox configurations

### 2020-03-20

* Added support for non-blocking commands
* Added option "wait" for running command
* stdout and stderr of a command become stream
* Improved test coverage

### 2020-02-29

* Enabled support for list shell commands by dir(Shell)
* Enabled command autocomplete in **BPython** and **IPython** for Shell
* Added ability to run shell commands with no-identifier-like name
* Added access to the last executed command even if exception was raised
* Added property "errors" for stderr output
* Added human-understandable behaviour for str() and repr() of Command instance
* Some internal refactoring and bugfixes
