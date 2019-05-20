"""Utility script which runs LDA for topic modeling and textblob sentiment analysis.

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

import sys
import sqlite3

import gensim.corpora.dictionary
import gensim.models.callbacks
import gensim.models
import gensim.models.ldamodel
import gensim.parsing.preprocessing
import pandas
import textblob

NUM_ARGS = 1
USAGE_STR = 'python sentiment_and_topics.py [path to db]'


def fix_and_tokenize_text(text):
    """Clean up text including removal of stop words before tokenizing.

    Args:
        text: The text to preprocess.
    Returns:
        Iterable over string tokens.
    """
    return gensim.parsing.preprocessing.preprocess_string(text)


def create_topics(data_frame, num_topics=20):
    """Create topic assignments using LDA over titles.

    Args:
        data_frame: The data frame with the article information. Expects a title column. This frame
            will be modified in place such that titleBow and titleProbs columns are added.
        num_topics: Optional argument specifying how many topics should be created. Defaults to 20.
    """
    titles = data_frame['title'].apply(fix_and_tokenize_text).tolist()
    title_dictionary = gensim.corpora.dictionary.Dictionary(titles)
    title_corpus = [title_dictionary.doc2bow(text) for text in titles]

    lda_model_title = gensim.models.ldamodel.LdaModel(
        title_corpus,
        num_topics=num_topics
    )

    data_frame['titleBow'] = title_corpus
    data_frame['topicProbs'] = data_frame['titleBow'].apply(lambda x: lda_model_title[x])

    max_topics = data_frame['topicProbs'].apply(
        lambda probs: max(probs, key=lambda prob: prob[1]) if len(probs) > 0 else (-1, 0)
    )

    data_frame['maxTopic'] = max_topics.apply(lambda x: x[0])
    data_frame['maxTopicProb'] = max_topics.apply(lambda x: x[1])


def get_avg_sentiment(text):
    """Get the average sentiment across sentences found within given text.

    Args:
        text: The text for which average sentiment polarity should be returned.
    Returns:
        Float representing average polarity across all setences found within text.
    """
    blob = textblob.TextBlob(text)
    sentences = blob.sentences
    if len(sentences) == 0:
        return 0
    return sum(map(lambda x: x.sentiment.polarity, sentences)) / len(sentences)


def create_sentiment(data_frame):
    """Create a sentiment score column in a provided data frame.

    Args:
        data_frame: The frame (which is expected to have a title column) into which a new
            titleSentiment column will be added. This data frame will be modified in place.
    """
    data_frame['titleSentiment'] = data_frame['title'].apply(get_avg_sentiment)


def output_results(data_frame, conn):
    """Save the results of this script back out to the input database.

    Args:
        data_frame: The frame with columns title, description, actualSource, maxTopic, maxTopicProb,
            and titleSentiment.
        conn: The database connection through which the given frame will be persisted.
    """
    data_frame_out = pandas.DataFrame()
    data_frame_out['title'] = data_frame['title']
    data_frame_out['description'] = data_frame['description']
    data_frame_out['actualSource'] = data_frame['actualSource']
    data_frame_out['maxTopic'] = data_frame['maxTopic']
    data_frame_out['maxTopicProb'] = data_frame['maxTopicProb']
    data_frame_out['titleSentiment'] = data_frame['titleSentiment']

    data_frame_out.to_sql('topics_and_sentiment', conn)
    conn.commit()


def run_operations(path_to_db=None, conn=None, num_topics=20):
    """Find average sentence sentiment and topic assignments.

    Args:
        path_to_db: String path to a sqlite database on which to operate.
        conn: DB API v2 compliant database conne tion on which to perform operations. If not given,
            use path_to_db.
        num_topics: The number of topics to generate.
    """
    num_passed = len(list(filter(lambda x: x != None, [conn, path_to_db])))
    if num_passed != 1:
        raise RuntimeError('run_operations requires conn or path_to_db but not both.')

    if conn == None:
        conn = sqlite3.connect(path_to_db)

    data_frame = pandas.read_sql(
        '''
            SELECT
                *
            FROM
                predictions
        ''',
        conn
    )

    create_topics(data_frame, num_topics=num_topics)
    create_sentiment(data_frame)
    output_results(data_frame, conn)


def main():
    """Run the sentiment and topics script."""
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        return

    path_to_db = sys.argv[1]

    run_operations(path_to_db)


if __name__ == '__main__':
    main()
