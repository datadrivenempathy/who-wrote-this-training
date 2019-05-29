"""Logic to tokenize text and convert it to vector representations.

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
import bs4
import keras


class Tokenizer:
    """Utility to tokenize text and convert it to vector representations."""

    def __init__(self, corpus_col, tokens_col, vector_col, num_words, vectorizer):
        """Create a new tokenizer.

        Args:
            corpus_col: The name of the column with the text to be tokenized.
            tokens_col: The column into which token identifiers should be written.
            vector_col: The column into which vectors of the tokens should be written.
            num_words: The number of unique words to tokenize / vectorize.
            vectorizer: The InputVectorizer through which tokens should be converted to vectors.
        """
        self.__corpus_col = corpus_col
        self.__tokens_col = tokens_col
        self.__vector_col = vector_col
        self.__num_words = num_words
        self.__vectorizer = vectorizer
        self.__inner_tokenizer = None

    def tokenize(self, data_frame, overwrite_in_place=True):
        """Interpret and tokenize input text.

        Args:
            data_frame: The data frame from which input text should be interpreted and tokenized.
            overwrite_in_place: Flag indicating if the corpus text should be preprocessed in place.
                Often preprocessing in place will save memory so, by passing True, the corpus text
                will be written to the same column from which it was read after preprocessing. If
                False, the corpus text preprocessed will be saved to the a new column with the same
                name as the original but with '_preprocessed' appended to its name. Defaults to
                True.
        """
        tokenizer = keras.preprocessing.text.Tokenizer(lower=True, num_words=self.__num_words)

        if overwrite_in_place:
            output_col = self.__corpus_col
        else:
            output_col = self.__corpus_col + '_preprocessed'

        data_frame[output_col] = data_frame[self.__corpus_col].apply(
            lambda x: self.__parse_html(x)
        )

        tokenizer.fit_on_texts(data_frame[output_col])
        data_frame[self.__tokens_col] = tokenizer.texts_to_sequences(data_frame[output_col])

        self.__inner_tokenizer = tokenizer

    def convert_tokens_to_vector(self, data_frame):
        """Create a vectorization of tokens.

        Args:
            data_frame: The frame from which the tokens should be read and into which the
                vectorization should be written.
        """
        data_frame[self.__vector_col] = data_frame[self.__tokens_col].apply(
            lambda x: self.__vectorizer.prepare(self.__num_words, x)
        )

    def __parse_html(self, html):
        """Parse input HTML to return only the user visible text.

        Args:
            html: The string html source to process.
        Returns:
            String HTML text read from the source.
        """
        soup = bs4.BeautifulSoup(html, 'lxml')
        return soup.text

    def get_inner_tokenizer(self):
        """Get the third party tokenizer utility used to tokenzie the text.

        Returns:
            keras.preprocessing.text.Tokenizer used to fit the text.
        """
        return self.__inner_tokenizer
