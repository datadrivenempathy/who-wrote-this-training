"""Copyright 2019 Data Driven Empathy LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sqlite3
import unittest

import pandas

import data_util
import test_util


class DataUtilTest(unittest.TestCase):

    def setUp(self):
        self.__conn = sqlite3.connect(':memory:')
        test_util.build_example_set(self.__conn)
        self.__conn.commit()

    def tearDown(self):
        cursor = self.__conn.cursor()
        cursor.execute('DROP TABLE articles_clean_assigned')
        self.__conn.commit()

    def test_load_data(self):
        loader = data_util.DataLoader(conn=self.__conn)
        loaded_data = loader.load_data()
        self.assertEquals(loaded_data.shape[0], 20)
