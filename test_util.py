"""Common logic across unit tests.

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
import pandas


def build_example_frame():
    return pandas.DataFrame([
        create_example_record('CNN', 'Test title 1 a', 'Test description 1 a', 'train'),
        create_example_record('CNN', 'Test title 2 a', 'Test description 2 a', 'train'),
        create_example_record('Fox', 'Test title 1 b', 'Test description 1 b', 'train'),
        create_example_record('Fox', 'Test title 2 b', 'Test description 2 b', 'train'),
        create_example_record('Daily Mail', 'Test title 1 c', 'Test description 1 c', 'train'),
        create_example_record('Daily Mail', 'Test title 2 c', 'Test description 2 c', 'train'),
        create_example_record('Drudge Report', 'Test title 1 d', 'Test description 1 d', 'validation'),
        create_example_record('Drudge Report', 'Test title 2 d', 'Test description 2 d', 'validation'),
        create_example_record('New York Times', 'Test title 1 e', 'Test description 1 e', 'test'),
        create_example_record('New York Times', 'Test title 2 e', 'Test description 2 e', 'test'),
        create_example_record('BBC', 'Test title 1f', 'Test description 1 f', 'test'),
        create_example_record('BBC', 'Test title 2f', 'Test description 2 f', 'test'),
        create_example_record('Breitbart', 'Test title 1 g', 'Test description 1 g', 'test'),
        create_example_record('Breitbart', 'Test title 2 g', 'Test description 2 g', 'test'),
        create_example_record('Wall Street Journal', 'Test title 1 h', 'Test description 1 h', 'test'),
        create_example_record('Wall Street Journal', 'Test title 2 h', 'Test description 2 h', 'test'),
        create_example_record('Vox', 'Test title 1 i', 'Test description 1 i', 'test'),
        create_example_record('Vox', 'Test title 2 i', 'Test description 2 i', 'test'),
        create_example_record('NPR', 'Test title 1 j', 'Test description 1 j', 'test'),
        create_example_record('NPR', 'Test title 2 j', 'Test description 2 j', 'test')
    ])


def build_example_set(conn):
    test_data = build_example_frame()
    test_data.to_sql('articles_clean_assigned', conn)


def create_example_record(source, title, description, assignment):
    return {
        'source': source,
        'title': title,
        'description': description,
        'setAssignment': assignment
    }
