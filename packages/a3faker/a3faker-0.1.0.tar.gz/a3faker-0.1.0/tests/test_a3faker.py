# -*- coding: utf-8 -*-
import os
import unittest
from datetime import date

from a3faker import FakerProxy, TypePersonFaker, TypeDateTimeFaker


class T(unittest.TestCase):

    def test__faker_proxy(self):
        os.environ['FAKER_LOCALE'] = 'zh_CN'
        f: TypePersonFaker = FakerProxy.get_faker()
        chinese_name = f.name()
        self.assertTrue(0 < len(chinese_name) <= 4)

        f: TypeDateTimeFaker = FakerProxy.get_faker('en_US')
        self.assertTrue(f.future_date() > date.today())

        f: TypeDateTimeFaker = FakerProxy.get_faker()
        self.assertTrue(f.past_date() < date.today())
