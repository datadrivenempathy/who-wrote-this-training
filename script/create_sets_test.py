"""Tests for creating train, test, and validation sets.

Copyright 2019 Data Driven Empathy LLC

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
import sqlite3
import unittest

import create_sets


class CreateSetTests(unittest.TestCase):

    def test_assign_to_sets_no_param(self):
        self.assertRaises(RuntimeError, lambda: create_sets.assign_to_sets())

    def test_assign_to_sets_connection(self):
        conn = sqlite3.connect(':memory:')

        in_frame = pandas.DataFrame([
            {'source': 'test source', 'title': 'test title', 'description': 'test description'}
        ] * 100)

        in_frame.to_sql('articles_clean', conn)

        create_sets.assign_to_sets(conn=conn)

        out_frame = pandas.read_sql(
            '''
            SELECT
                setAssignment,
                count(1) AS cnt
            FROM
                articles_clean_assigned
            GROUP BY
                setAssignment
            ''',
            conn
        )

        count = out_frame[out_frame['setAssignment'] == 'train']['cnt'].sum()
        self.assertTrue(count > 70)
        self.assertTrue(count < 90)

        cursor = conn.cursor()
        cursor.execute('DROP TABLE articles_clean_assigned')
        cursor.execute('DROP TABLE articles_clean')
        conn.commit()
