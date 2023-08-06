import unittest
import math
import json

from pydantic import BaseModel, parse_obj_as

from . import *

import logging
logger = logging.getLogger(__name__)


# test_list = [
#     {
#         'dist': {
#             't': 'logistic',
#             'loc': 1
#         },
#         'cdf': {'x': 1, 'y': 0.5}
#     }
# ]
#parse_obj_as(Distribution, config)


class TestConstant(unittest.TestCase):
    def test_v(self):
        test_var = factory.get_instance({'t': 'constant'})
        self.assertEqual(test_var.get_random_value(), 0)

        test_var0 = factory.get_instance({'t': 'constant', 'loc': 0})
        self.assertEqual(test_var0.get_random_value(), 0)

        test_var1 = factory.get_instance({'t': 'constant', 'loc': 1})
        self.assertEqual(test_var1.get_random_value(), 1)

    def test_cdf(self):
        test_var = factory.get_instance({'t': 'constant', 'loc': 10})
        self.assertEqual(test_var.cdf(20), 200)
        self.assertEqual(test_var.pdf(0), 10)
        self.assertEqual(test_var.pdf(1), 10)


class TestUniform(unittest.TestCase):
    def test_uniform(self):
        test_var = factory.get_instance({'t': 'uniform', 'b': 2})
        cdf = test_var.cdf(0.5)
        self.assertAlmostEqual(cdf, 0.25)
        pdf = test_var.pdf(0.5)
        self.assertAlmostEqual(pdf, 0.5)


class TestLogistic(unittest.TestCase):
    def test_cdf(self):
        test_var = factory.get_instance({'t': 'logistic', 'loc': 1})
        #logger.debug(json.dumps(test_var.dict(), indent=2))

        cdf0 = test_var.cdf(1)
        self.assertEqual(cdf0, 0.5)


class TestNormal(unittest.TestCase):
    def test_cdf(self):
        test_var = factory.get_instance({'t': 'normal'})
        cdf = test_var.cdf(0.0)
        self.assertAlmostEqual(cdf, 0.5)

        cdf = test_var.cdf(1.0)
        self.assertAlmostEqual(cdf, 0.841344746)

    def test_pdf(self):
        test_var = factory.get_instance({'t': 'normal'})
        self.assertAlmostEqual(test_var.pdf(2.0), 0.05399096651)


class TestSkewNormal(unittest.TestCase):
    def test_cdf(self):
        test_var = factory.get_instance({'t': 'skew_normal', 'a': 1})
        cdf = test_var.cdf(0)
        self.assertAlmostEqual(cdf, 0.25)

        test_var = factory.get_instance({'t': 'skew_normal', 'a': -1})
        cdf = test_var.cdf(0)
        self.assertAlmostEqual(cdf, 0.75)


class TestLogNormal(unittest.TestCase):
    def test_cdf(self):
        test_var = factory.get_instance({'t': 'log_normal'})

        p50 = test_var.get_percentile(.5)
        self.assertAlmostEqual(p50, 1.0)

        p75 = test_var.get_percentile(0.75)
        cdf = test_var.cdf(p75)
        self.assertAlmostEqual(cdf, 0.75)

    def test_pdf(self):
        test_var = factory.get_instance({'t': 'log_normal', 'loc': 0, 'scale': 1})
        self.assertAlmostEqual(test_var.pdf(1.5), 0.24497365)


class TestGamma(unittest.TestCase):
    def test_gamma1(self):
        test_var = factory.get_instance({'t': 'gamma', 'loc': 1})
        pdf0 = test_var.pdf(1)
        self.assertAlmostEqual(pdf0, 1.0)

    def test_gamma_half(self):
        test_var = factory.get_instance({'t': 'gamma', 'rate': 0.5})
        pdf1 = test_var.pdf(1)
        self.assertAlmostEqual(pdf1, 0.30326532)


class TestBeta(unittest.TestCase):
    def test_pdf(self):
        test_var = factory.get_instance({'t': 'beta'})
        pdf = test_var.pdf(0.1)
        self.assertAlmostEqual(pdf, 1.0)


class TestWeibull(unittest.TestCase):
    def test_pdf(self):
        test_var = factory.get_instance({'t': 'weibull', 'shape': 2, 'scale': 4, 'threshold': 0})
        cdf = test_var.cdf(4)
        self.assertAlmostEqual(cdf, 0.63212055)
