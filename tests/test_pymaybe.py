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

    def test_runDoctests(self):
        pass

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
