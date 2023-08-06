import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

import unittest

from uncertainty.utypes import *
from funcs_testing import *

class uboolTest(unittest.TestCase):

    def test_abs(self):
        t(abs(uint(-3, 0.7)),        e = uint(3, 0.7))
        t(abs(ufloat(-0.2, 0.7)),    e = ufloat(0.2, 0.7))

    def test_sqrt(self):
        t(sqrt(uint(3, 0.7)),        e = ufloat(1.732, 0.202))
        t(sqrt(ufloat(2.0, 0.7)),    e = ufloat(1.414, 0.247))

    def test_inverse(self):
        t(inverse(uint(7, 0.7)),     e = ufloat(0.143, 0.014))
        t(inverse(ufloat(7, 0.7)),   e = ufloat(0.143, 0.014))

if __name__ == '__main__':
    unittest.main()