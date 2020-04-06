# Integrations

Being a result of Python magic around "duck typing", **python-shell**
tries to integrate with different tools for easier usage.
One of the most popular features is autocompletion, which is somehow
 implemented for Shell commands to work with **Shell** class.
However, not all the popular software "agreed" with that.

## Integrations with custom Python interpreters

For now, autocompletion of **Shell** class is confirmed in a few
popular custom Python interfaces (interpreters):

* [BPython](https://github.com/bpython/bpython)

* [IPython](https://ipython.org/)


## Integrations with IDEs

Modern IDEs are complicated, as they provide a lot of functionality.
Some of them, like PyCharm, use static analysis for it ([proof](https://youtrack.jetbrains.com/issue/PY-40943)).
That's the reason why **Shell** autocompletion does not work in this IDE.
