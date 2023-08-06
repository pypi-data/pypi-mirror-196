# Pylint Print Checker

A Pylint plugin for checking for use of the `print()` function in Python.

## Installation

The best way to install Pylint Print is to use pip as follows:

```bash
pip install pylint-print
```

## Example Usage

This simple program is saved as `hello_world.py`:
```python
"""
a module to demonstrate the pylint-print checker
"""

if __name__ == "__main__":
    print("Hello, World!")

```

In order to use pylint-print, this must be included as a plug in there are two main ways to do
this. The first method is to use the command line options:
```bash
pylint hello_world.py --load-plugins=pylint_print
```

This will provide a response that should look like this:
```
************* Module hello_world
hello_world.py:6:4: W8201: Logging should be used instead of the print() function. (print-function)

-----------------------------------
Your code has been rated at 5.00/10
```

The other main way to use pylint is with a configuration file. Refer to the 
[Pylint Documentation](https://pylint.pycqa.org/en/latest/) for more details about the 
configuration files and how to set one up. 

The configuration file should have a `load-plugin` key which will need the `pylint_print` added
as follows:

```ini
# List of plugins (as comma separated values of python module names) to load,
# usually to register additional checkers.
load-plugins=pylint_print
```

Once the plugin has been added to the configuration file it is no long necessary to add it to the
`pylint` execution, for example:
```bash
pylint hello_world.py
```

# Why warn about `print` usage 

`print` statements  are often the first thing a developer learns, they are useful to add to your 
code when developing to understand how it works and debug problems. 

However, as a project grows they can become problematic, it is much better to use a logger that
allows:
* Log messages to be filtered by type or module
* Log messages can be redirected to other places rather than the console e.g. a file

For these reasons some projects may want to restrict the usage of `print` in their coding rules 
and make a check as part of the linting checks to avoid needing manual reviews

# Further Information

View on [PyPi](https://pypi.org/project/pylint-print/)
