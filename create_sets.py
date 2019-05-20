"""Utility that assigns instances to train, test, and validation sets.

Simple python script that assigns instances to train, test, and validation sets, reading from
article_clean and outputing assignments into articles_clean_assigned.

----

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

import random
import sqlite3

import pandas

NUM_ARGS = 1
USAGE_STR = 'USAGE: python create_sets.py [path to db]'


def assign_to_sets(conn=None, path_to_db=None):
    """Assign instances in the target database into test, training, and validation sets.

    Args:
        conn: DB API v2 compliant database connection. If not given, provide path_to_db.
        path_to_db: The string path to the sqlite database on which to operate. If not given,
            provide conn.
    """
    num_passed = len(list(filter(lambda x: x != None, [conn, path_to_db])))
    if num_passed != 1:
        raise RuntimeError('assign_to_sets requires conn or path_to_db but not both.')

    if conn == None:
        conn = sqlite3.connect(path_to_db)

    frame = pandas.read_sql(
        '''
        SELECT
            source,
            title,
            description
        FROM
            articles_clean
        WHERE
            title != ''
            AND description != ''
            AND source != ''
        ''',
        conn
    )

    frame['setAssignment'] = frame['source'].apply(lambda x: random.choice([
        'train',
        'train',
        'train',
        'train',
        'train',
        'train',
        'train',
        'train',
        'validation',
        'test'
    ]))

    frame.to_sql('articles_clean_assigned', conn)

    conn.commit()


def main(db=None):
    """Assign to training, test, and validation sets using CLI arguments."""
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        return

    path_to_db = sys.argv[1]

    assign_to_sets(path_to_db=path_to_db)


if __name__ == '__main__':
    main()
