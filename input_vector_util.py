import numpy


class InputVectorizer:

    def prepare(self, num_words, tokenization):
        raise NotImplementedError('Requires implementor of interface.')


class OccurenceInputVectorizer(InputVectorizer):

    def prepare(self, num_words, tokenization):
        output_array = numpy.zeros(num_words-1)
        for token_id in tokenization:
            output_array[token_id - 1] = 1
        return output_array


class SequenceInputVectorizer(InputVectorizer):

    def prepare(self, num_words, tokenization):
        return tokenization # No-op the embedding is part of topology
