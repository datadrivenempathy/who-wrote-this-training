"""Create a mapping from 'clean title' to original title in a sqlite database.

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

import sqlite3
import sys

import pandas

import data_util

NUM_ARGS = 1
USAGE_STR = 'python create_clean_title_bridge.py [path to db]'


def perform_operations(db_loc):
    """The DB location at which the table should be created.

    Args:
        db_loc: String path to the sqlite database on which to operate.
    """
    data_loader = data_util.DataLoader(db_loc=db_loc)
    output_frame_not_clean = data_loader.load_data(
        output_col_title='newTitle',
        output_col_description='newDescription'
    )

    output_frame = pandas.DataFrame()
    output_frame['originalTitle'] = output_frame_not_clean['title']
    output_frame['originalDescription'] = output_frame_not_clean['description']
    output_frame['newTitle'] = output_frame_not_clean['newTitle']
    output_frame['newDescription'] = output_frame_not_clean['newDescription']
    output_frame['source'] = output_frame_not_clean['source']

    output_frame.to_sql('transformation_bridge', sqlite3.connect(db_loc))


def main():
    """Main entry point for the script."""
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        return

    perform_operations(sys.argv[1])

if __name__ == '__main__':
    main()
