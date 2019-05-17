import sqlite3
import unittest

import pandas

import sentiment_and_topics


class SentimentAndTopicsTests(unittest.TestCase):

    def setUp(self):
        self.__test_frame = pandas.DataFrame([
            self.__create_test_record('Excellent article biology'),
            self.__create_test_record('Excellent article biology 2'),
            self.__create_test_record('Excellent article science'),
            self.__create_test_record('Excellent article art')
        ])

        self.__conn = sqlite3.connect(':memory:')
        self.__test_frame.to_sql('predictions', self.__conn)
        self.__conn.commit()

    def test_fix_and_tokenize_text(self):
        tokens = sentiment_and_topics.fix_and_tokenize_text('Testing test. Test text.')
        self.assertEquals(len(tokens), 4)

    def test_create_topics(self):
        sentiment_and_topics.create_topics(self.__test_frame, num_topics=3)
        min_topic = self.__test_frame['maxTopic'].min()
        max_topic = self.__test_frame['maxTopic'].max()
        self.assertTrue(min_topic >= 0 and min_topic <= 3)
        self.assertTrue(max_topic >= 0 and max_topic <= 3)

    def test_get_avg_sentiment(self):
        sentiment_1 = sentiment_and_topics.get_avg_sentiment('It is vile. It is awful.')
        sentiment_2 = sentiment_and_topics.get_avg_sentiment('It is excellent. It is great.')
        self.assertTrue(sentiment_1 < 0)
        self.assertTrue(sentiment_2 > 0)

    def test_create_sentiment(self):
        sentiment_and_topics.create_sentiment(self.__test_frame)
        self.assertTrue(self.__test_frame['titleSentiment'].mean() > 0)

    def test_run_operations(self):
        sentiment_and_topics.run_operations(conn=self.__conn, num_topics=3)
        results = pandas.read_sql('SELECT count(1) AS cnt FROM topics_and_sentiment', self.__conn)
        self.assertEquals(results['cnt'].sum(), 4)

    def __create_test_record(self, title):
        return {
            'title': title,
            'description': 'description',
            'actualSource': 'source'
        }
