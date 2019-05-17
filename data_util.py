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

    def __init__(self, test_size=0, select_sql=DATA_SELECT_STATEMENT):
        self.__test_size = test_size
        self.__select_sql = select_sql

    def load_data(self, db_loc='articles.db', partition_test=False, remove_ad_here=True,
            remove_self_ref=True, remove_article_place_info=True):

        articles_db = sqlite3.connect(db_loc)
        data_frame = pandas.read_sql_query(self.__select_sql, articles_db)

        if partition_test:
            data_frame['set_assignment'] = data_frame['source'].apply(
                lambda x: self.__get_set_assignment()
            )

        if remove_ad_here:
            data_frame['description'] = data_frame['description'].apply(
                lambda x: x.replace('Advertise here', '').replace(']]>', '')
            )

        if remove_self_ref:
            data_frame['title'] = data_frame.apply(
                lambda x: x['title'].replace(x['source'], ''),
                axis=1
            )

            data_frame['description'] = data_frame.apply(
                lambda x: x['description'].replace(x['source'], ''),
                axis=1
            )

        if remove_article_place_info:
            data_frame['description'] = data_frame['description'].apply(
                lambda x: re.sub(
                    r'\(.* column, .* story, link\)',
                    '',
                    x
                )
            )

        return data_frame

    def __get_set_assignment(self):
        rand_num = random.random()
        if rand_num < (1 - self.__test_size):
            return 'train'
        else:
            return 'test'
