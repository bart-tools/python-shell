# Getting started

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
