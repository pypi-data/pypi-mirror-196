# -*- coding: utf-8 -*-
"""
Unittests
"""

import unittest
import ppf.constants as cn


class Test(unittest.TestCase):

    def test_molar_volume(self):
        V_mol = cn.R * -cn.T0 / (760 * cn.torr)
        self.assertTrue(abs(V_mol / 22.4e-3 - 1) < 0.01)


if __name__ == '__main__':
    # This enables running the unit tests by running this script which is
    # much more convenient than 'python setup.py test' while developing tests.
    # Note: package-under-test needs to be in python-path
    unittest.main()
