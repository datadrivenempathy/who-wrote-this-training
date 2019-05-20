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

import run_single
import test_util


class RunSingleTest(unittest.TestCase):

    def setUp(self):
        self.__config_occ = {
            "corpusCol": "description",
            "denseSize1": 32,
            "denseSize2": 16,
            "dropoutRate": 0,
            "kernelRegPenalty": 0.01,
            "method": "occurrence",
            "numWords": 15,
            "sourceCol": "source",
            "sourceIdCol": "sourceId",
            "sourceIdVectorCol": "sourceIdVector",
            "tokenVectorCol": "tokenVector",
            "tokensCol": "tokens",
            "foxWeight": 0,
            "useWandb": False,
            "epochs": 1
        }

        self.__config_lstm = {
            "corpusCol": "description",
            "lstmSize": 32,
            "dropoutRate": 0,
            "kernelRegPenalty": 0.01,
            "method": "sequence",
            "numWords": 15,
            "sourceCol": "source",
            "sourceIdCol": "sourceId",
            "sourceIdVectorCol": "sourceIdVector",
            "tokenVectorCol": "tokenVector",
            "tokensCol": "tokens",
            "maxSeqLen": 10,
            "useWandb": False,
            "epochs": 1,
            "foxWeight": 0
        }

        self.__project_name = 'test'

        self.__run_name = 'run_name'

        self.__conn = sqlite3.connect(':memory:')

        test_util.build_example_set(self.__conn)

        self.__conn.commit()

    def test_run_config_occ(self):
        run_single.run_config(
            self.__config_occ,
            self.__project_name,
            self.__run_name,
            self.__conn
        )

        results = pandas.read_sql('SELECT count(1) AS cnt FROM predictions', self.__conn)

        self.assertEquals(results['cnt'].sum(), 20)

    def test_run_config_lstm(self):
        run_single.run_config(
            self.__config_lstm,
            self.__project_name,
            self.__run_name,
            self.__conn
        )

        results = pandas.read_sql('SELECT count(1) AS cnt FROM predictions', self.__conn)

        self.assertEquals(results['cnt'].sum(), 20)
