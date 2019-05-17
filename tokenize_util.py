import bs4
import keras


class Tokenizer:

    def __init__(self, corpus_col, tokens_col, vector_col, num_words, vectorizer):
        self.__corpus_col = corpus_col
        self.__tokens_col = tokens_col
        self.__vector_col = vector_col
        self.__num_words = num_words
        self.__vectorizer = vectorizer

    def tokenize(self, data_frame):
        tokenizer = keras.preprocessing.text.Tokenizer(lower=True, num_words=self.__num_words)
        data_frame[self.__corpus_col] = data_frame[self.__corpus_col].apply(lambda x: self.__try_parse(x))
        tokenizer.fit_on_texts(data_frame[self.__corpus_col])
        data_frame[self.__tokens_col] = tokenizer.texts_to_sequences(data_frame[self.__corpus_col])

    def convert_tokens_to_vector(self, data_frame):
        data_frame[self.__vector_col] = data_frame[self.__tokens_col].apply(
            lambda x: self.__vectorizer.prepare(self.__num_words, x)
        )
    
    def __try_parse(self, html):
        soup = bs4.BeautifulSoup(html, 'lxml')
        return soup.text
