# Python Shell Wrapper Library

A flexible, easy-to-use library to integrate your Python script with Unix ecosystems.

## Why yet another one?

This library comes with a few major points to use it:

* It is easy and intuitive (see examples)
* It's compatible with Python 2 (can be useful in old large systems)
* Continuous support of the library

## Getting started

This library is pretty easy to use:

```python
from python_shell import Shell
from python_shell.util.streaming import decode_stream

Shell.ls('-l', '$HOME')  # Equals "ls -l $HOME"

command = Shell.whoami()  # Equals "whoami"
print(command)  # Prints representation of command in shell

print(command.command)  # prints "whoami"
print(repr(command))  # Does the same as above

print(command.return_code)  # prints "0"
print(command.arguments)  # prints ""

print(decode_stream(command.output)) # Prints out command's stdout
print(decode_stream(command.errors)) # Prints out command's stderr
```

To run any Bash command, you need to do it like this:
```
Shell.<bash_command_name>(<bash command parameters>)
```

For example, you want to create a new folder:
```python
Shell.mkdir('-p', '/tmp/new_folder')
```

It's also possible to run a command which name is not a valid Python identifier.
To do this, use Shell class as a callable instance:
```python
command = Shell('2to3')
```

When the command fails (returncode is non-zero), Shell throws a ShellException error.
However, even if you didn't save a reference to your command, you still can access it.
To do this, try
```python
last_cmd = Shell.last_command
```
### Installing

Simply run

```
pip install python-shell
```

## Integration with development tools

**Shell** class now allows to list all available commands simply by
```python
dir(Shell)
```

This feature enables autocomplete of commands in a few popular interfaces:
- BPython
- IPython
 
## Extending the basic functionality

It's possible to extend the existing functionality without forking the project.
The library provides an interface to add a custom Command class.

## Running the tests

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
- coverage (using Python 3)
- coverage (using Python 2.7)
- pep8 (style checking)

Other old versions of Python (e.g. 2.6, 3.4, etc) will never be supported. However, you always can implement such support in your forks.

Test coverage is one of the top priority for this library:
- Coverage using Python 2.7: 96%
- Coverage using Python 3.x: 93%

## Authors

* **Alex Sokolov** - *Author* - [Albartash](https://github.com/AlBartash)

## Contacts

* Telegram channel with updates: [@bart_tools](http://t.me/bart_tools)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
