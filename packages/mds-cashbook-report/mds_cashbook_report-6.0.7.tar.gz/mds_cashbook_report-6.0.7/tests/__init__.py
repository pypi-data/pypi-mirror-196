# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.cashbook_report.tests.test_report import ReportTestCase


__all__ = ['suite']


class CashbookReportTestCase(\
    ReportTestCase,\
    ):
    'Test cashbook report module'
    module = 'cashbook_report'

# end CashbookReportTestCase

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(CashbookReportTestCase))
    return suite
