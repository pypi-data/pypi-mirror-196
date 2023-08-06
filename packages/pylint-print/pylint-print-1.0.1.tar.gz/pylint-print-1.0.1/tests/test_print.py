"""
Tests for print detection.
"""
import importlib.util

import pylint.testutils
import astroid

spec = importlib.util.spec_from_file_location("pylint_print", "pylint_print/pylint_print.py")
pylint_print = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pylint_print)

from astroid import parse
from pylint.lint import PyLinter
from unittest.mock import MagicMock

class TestPrintChecker(pylint.testutils.CheckerTestCase):
    """
    Test cases for print function detection.
    """
    CHECKER_CLASS = pylint_print.PrintChecker

    def test_print_call(self):
        module = parse('''
        print("output")
        ''')
        pp = pylint_print.PrintChecker(PyLinter())
        pp.add_message = MagicMock()
        pp.visit_call(module.body[-1].value)
        pp.add_message.assert_called_with('print-function', node=module.body[-1].value)

    def test_non_print_call(self):
        module = parse('''
        list()
        ''')
        pp = pylint_print.PrintChecker(PyLinter())
        pp.add_message = MagicMock()
        pp.visit_call(module.body[-1].value)
        pp.add_message.assert_not_called()
