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

import pandas

import unittest

import source_id_util
import test_util


class NumericalSourceVectorFacadeTests(unittest.TestCase):

    def setUp(self):
        self.__frame = test_util.build_example_frame()
        self.__facade = source_id_util.NumericalSourceVectorFacade()

    def test_build_vectors_id_col(self):
        self.__facade.build_vectors(self.__frame)
        self.assertEquals(self.__frame['source_id'].min(), 0)
        self.assertEquals(self.__frame['source_id'].max(), 9)

    def test_build_vectors_vector_col(self):
        self.__facade.build_vectors(self.__frame)
        sample_vector = self.__frame.iloc[0]['source_id_vector']
        self.assertEquals(sample_vector.shape[0], 10)
