"""Utilities to convert input strings into vectors usable in learning / prediction.

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

import numpy


class InputVectorizer:
    """Interface for vectorizing tokenized inputs."""

    def prepare(self, num_words, tokenization):
        """Vectorize a tokenized input.

        Args:
            num_words: The maximum number of unique tokens to be vectorized.
            tokenization: Iterable over integer tokens.
        Returns:
            numpy.array or similar that represents the vectorization.
        """
        raise NotImplementedError('Requires implementor of interface.')


class OccurenceInputVectorizer(InputVectorizer):
    """Vectorize logic for co-ocurrence feed forward network."""

    def prepare(self, num_words, tokenization):
        output_array = numpy.zeros(num_words-1)
        for token_id in tokenization:
            output_array[token_id - 1] = 1
        return output_array


class SequenceInputVectorizer(InputVectorizer):
    """Vectorize logic for sequences used by LSTM."""

    def prepare(self, num_words, tokenization):
        return tokenization # No-op the embedding is part of topology
