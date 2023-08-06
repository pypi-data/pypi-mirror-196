"""
Test the plugin registration method.
"""

import importlib.util
spec = importlib.util.spec_from_file_location("pylint_print", "pylint_print/pylint_print.py")
pylint_print = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pylint_print)

from pylint.lint import PyLinter

def test_register():
    linter = PyLinter()
    assert 'print-function' not in linter._checkers
    pylint_print.register(linter)
    assert 'print-function' in linter._checkers
