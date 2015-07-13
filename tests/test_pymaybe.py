#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pymaybe
----------------------------------

Tests for `pymaybe` module.
"""

import unittest
import doctest

import pymaybe

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(pymaybe, globs=pymaybe.get_doctest_globs()))
    return tests


class TestPyMaybe(unittest.TestCase):

    def setUp(self):
        pass

    def test_something_forwardsMethodCalls(self):
        result = pymaybe.maybe('VALUE').lower()
        assert result.is_some()
        assert result == 'value'
        assert result == pymaybe.maybe('value')

    def test_something_forwardsMethodCalls_handlesNonExisting(self):
        result = pymaybe.maybe('VALUE').lowerr()
        assert result.is_none()

    def test_nothing_forwardsMethodCalls_handlesNonExisting(self):
        result = pymaybe.maybe(None).invalid().call()
        assert result.is_none()


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
