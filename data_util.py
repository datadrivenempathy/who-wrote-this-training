"""Logic to load article data from an input database.

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

import re
import random
import sqlite3

import pandas


DATA_SELECT_STATEMENT = '''
    SELECT
        source,
        title,
        description,
        setAssignment AS set_assignment
    FROM
        articles_clean_assigned
    ORDER BY
        random()
'''


class DataLoader:
    """Facade for loading article data required for training or prediction."""

    def __init__(self, test_size=0, select_sql=DATA_SELECT_STATEMENT, conn=None,
            db_loc='article.db'):
        """Create a new data loading facade.

        Args:
            test_size: The amount of data to put into a hidden test set. Set to zero if the data
                is already partitioned in the dataset. Defaults to zero.
            select_sql: The SQL to execute to read the data. Defaults to DATA_SELECT_STATEMENT.
            conn: The DB API v2 connection to use when reading article data. Set to None if
                providing a path via db_loc. Defaults to None.
            db_loc: Path to the sqlite database from which data will be read. Ignored if conn is
                provided and not null. Defaults to "article.db" within working directory.
        """

        self.__test_size = test_size
        self.__select_sql = select_sql
        self.__conn = conn
        self.__db_loc = db_loc

    def clean_input_text(self, target_text, source, remove_ad_here=True,
        remove_related_stories=True, remove_self_ref=True, remove_article_place_info=True,
        remove_the_latest=True):
        """Clean input a piece of input text:

        Args:
            source: The name of the news source that produced the given target text.
            target_text: The text to clean.
            remove_ad_here: Flag indicating if advertising string should be removed that could
                give away the publisher identity. Defaults to True.
            remove_self_ref: Flag controlling removal of references to the publisher from the title
                and description. Defaults to True.
            remove_article_place_info: Remove article placement metadata text that could give
                away the publisher identity. Deafults to True.
            remove_the_latest: Flag indicating if the string "the lastest" which may be identifying
                of some sources should be removed.
        Returns:
            The cleaned text as a string.
        """
        target_text = target_text.lower()
        source = source.lower()

        if remove_ad_here:
            target_text = target_text.replace('advertise here', '').replace(']]>', '')

        if remove_self_ref:
            target_text = target_text.replace(source, '')

        if remove_related_stories:
            target_text = target_text.replace('related stories', '')

        if remove_article_place_info:
            target_text = re.sub(
                r'\(.* column, .* story, link\)',
                '',
                target_text
            )

        if remove_the_latest:
            target_text = target_text.replace('the latest', '')

        return target_text

    def load_data(self, partition_test=False, remove_ad_here=True, remove_related_stories=True,
            remove_self_ref=True, remove_article_place_info=True, remove_the_latest=True,
            output_col_title='title', output_col_description='description'):
        """Load a data frame with article data.

        Args:
            partition_test: Flag indicating if a hidden test set should be set aside. Set to False
                to use a partitioning already found within the data. Deafults to False.
            remove_ad_here: Flag indicating if advertising string should be removed that could
                give away the publisher identity. Defaults to True.
            remove_self_ref: Flag controlling removal of references to the publisher from the title
                and description. Defaults to True.
            remove_article_place_info: Remove article placement metadata text that could give
                away the publisher identity. Deafults to True.
            remove_the_latest: Flag indicating if the string "the lastest" which may be identifying
                of some sources should be removed.
            output_col_title: The name of the column where the cleaned title should be written.
                Defaults to title (overwrite existing title col).
            output_col_description: The name of the column where the cleaned description should be
                written. Defaults to description (overwrite existing title description).
        Returns:
            Data frame with title, description, and source (with other optional fields depending
            on arguments) describing articles.
        """

        if self.__conn == None:
            articles_db = sqlite3.connect(self.__db_loc)
        else:
            articles_db = self.__conn

        data_frame = pandas.read_sql_query(self.__select_sql, articles_db)

        if partition_test:
            data_frame['set_assignment'] = data_frame['source'].apply(
                lambda x: self.__get_set_assignment()
            )

        cleanup_lambda = lambda text, source: self.clean_input_text(
            text,
            source,
            remove_ad_here=remove_ad_here,
            remove_related_stories=remove_related_stories,
            remove_self_ref=remove_self_ref,
            remove_article_place_info=remove_article_place_info,
            remove_the_latest=remove_the_latest
        )

        data_frame[output_col_title] = data_frame.apply(
            lambda x: cleanup_lambda(x['title'], x['source']),
            axis=1
        )

        data_frame[output_col_description] = data_frame.apply(
            lambda x: cleanup_lambda(x['description'], x['source']),
            axis=1
        )

        return data_frame

    def __get_set_assignment(self):
        """Generate a test or training set label.

        Returns:
            Random string either "train" or "test".
        """
        rand_num = random.random()
        if rand_num < (1 - self.__test_size):
            return 'train'
        else:
            return 'test'
