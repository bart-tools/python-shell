# Testing

## Running tests

This library contains tests written using *unittest* module, so just run in the project directory

```
python -m unittest
```

Also it's possible to run tests using Tox:

```bash
tox -e <env>
```

Supported environments:

- py27
- py35
- py36
- py37
- py38
- py39
- pypy (based on Python 2.7)
- pypy3 (based on Python 3.6)

## Test coverage

Test coverage is one of the top priority for this library.
For the latest release:

- Coverage using Python 2.7: 96%
- Coverage using Python 3.x: 93%

Tox environments:

- coverage (using Python 3)
- coverage (using Python 2.7)

## Code style checking

There're a few more Tox environments for checking code style:

- pep8 (style checking)
- pylint (using Python 3)
- pylint27 (using Python 2.7)

For PEP8 check, the **pycodestyle** and **flake8** are used sequentially.
Passing this check is required for merging the pull request.

Pylint, in other hand, is added for additional check and is not used in release
process.
