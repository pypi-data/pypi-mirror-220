###############################################################################
#
# Copyright 2006 by refline (Schweiz) AG, CH-5630 Muri
#
###############################################################################
"""Refline Recruiter Tests
"""
import doctest
import unittest

from zope.schema.interfaces import RequiredMissing

from z3c.schema.hostname import HostName
from z3c.schema.hostname import InvalidHostName


class HostNameTest(unittest.TestCase):

    _Field_Factory = HostName
    _convert = str

    def testValidate(self):
        field = self._Field_Factory(title='HostName field', description='',
                                    readonly=False, required=False)
        field.validate(None)
        field.validate(self._convert('host'))
        field.validate(self._convert('123.123.123.123'))
        field.validate(self._convert('host:123'))
        field.validate(self._convert('www.host.com:123'))
        field.validate(self._convert('123.123.123.123:123'))

    def testValidateRequired(self):
        field = self._Field_Factory(title='HostName field', description='',
                                    readonly=False, required=True)
        field.validate(self._convert('host'))
        self.assertRaises(RequiredMissing, field.validate, None)

    def testBadStringType(self):
        field = self._Field_Factory(title='HostName field')
        self.assertRaises(InvalidHostName, field.validate, '123.123')

    def test_newlines(self):
        field = self._Field_Factory(title='HostName field')
        self.assertRaises(InvalidHostName, field.validate,
                          self._convert('host\nfoo'))


def test_suite():
    return unittest.TestSuite((
        doctest.DocFileSuite(
            'README.txt',
            optionflags=(doctest.NORMALIZE_WHITESPACE
                         | doctest.ELLIPSIS
                         | doctest.IGNORE_EXCEPTION_DETAIL)),
        unittest.defaultTestLoader.loadTestsFromTestCase(HostNameTest),
    ))
