"""
Factory to construct keras neural networks structures and untrained keras models.

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
import keras


class TopologyFactory:
    """Interface for a factory that returns untrained keras models."""

    def build(self, kernel_regularizer=0, dropout=0):
        """Build a new keras model.

        Args:
            num_words: The number of unique words that will be used from the corpus.
            num_sources: The number of news sources that will be processed.
        Returns:
            The compiled keras.models.Model.
        """
        raise NotImplementedError('Must use implementor.')


class OccurrenceTopologyFactory(TopologyFactory):
    """Factory to build a keras feed forward network using word ocurrences / co-ocurrences."""

    def __init__(self, dense_size_1=8, dense_size_2=8, kernel_reg_penalty=0, dropout_rate=0):
        """Create a new factory to produce untrained feed forward networks.

        Args:
            dense_size_1: The number of nodes to include in the first dense layer.
            dense_size_2: The number of nodes to include in the second dense layer.
            kernel_reg_penalty: The L2 regularization penalty to apply.
            dropout_rate: The dropout rate to apply.
        """
        self.__dense_size_1 = dense_size_1
        self.__dense_size_2 = dense_size_2
        self.__kernel_reg_penalty = kernel_reg_penalty
        self.__dropout_rate = dropout_rate

    def build(self, num_words, num_sources):
        """Build a new feed forward keras model.

        Args:
            num_words: The number of unique words that will be used from the corpus.
            num_sources: The number of news sources that will be processed.
        Returns:
            The compiled keras.models.Model.
        """
        input_layer = keras.layers.Input(shape=(num_words,))

        dense_layer_1 = keras.layers.Dense(
            self.__dense_size_1,
            activation='relu',
            kernel_regularizer=keras.regularizers.l2(self.__kernel_reg_penalty)
        )(input_layer)

        dropout_layer = keras.layers.Dropout(self.__dropout_rate)(dense_layer_1)

        dense_layer_2 = keras.layers.Dense(
            self.__dense_size_2,
            activation='relu',
            kernel_regularizer=keras.regularizers.l2(self.__kernel_reg_penalty)
        )(dropout_layer)

        output_layer = keras.layers.Dense(
            num_sources,
            activation='softmax'
        )(dense_layer_2)

        ret_model = keras.models.Model(
            inputs=input_layer,
            outputs=output_layer
        )

        ret_model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

        return ret_model


class SequenceTopologyFactory(TopologyFactory):
    """Factory to build a keras LSTM recurrent network structure using word ids."""

    def __init__(self, max_seq_len=250, lstm_size=32, kernel_reg_penalty=0):
        """Create a new factory to produce untrained LSTM networks.

        Args:
            max_seq_len: The maximum length of the word sequence to feed through the network.
            lstm_size: The number of LSTM units to use within the returned networks.
            kernel_reg_penalty: The L2 regularization penalty to apply.
        """
        self.__max_seq_len = max_seq_len
        self.__lstm_size = lstm_size
        self.__kernel_reg_penalty = kernel_reg_penalty

    def build(self, num_words, num_sources):
        """Build a new LSTM keras model.

        Args:
            num_words: The number of unique words that will be used from the corpus.
            num_sources: The number of news sources that will be processed.
        Returns:
            The compiled keras.models.Model.
        """
        input_layer = keras.layers.Input(shape=(self.__max_seq_len,))

        embedding_layer = keras.layers.Embedding(num_words + 1, self.__lstm_size)(input_layer)

        lstm_layer = keras.layers.LSTM(
            self.__lstm_size,
            kernel_regularizer=keras.regularizers.l2(self.__kernel_reg_penalty)
        )(embedding_layer)

        output_layer = keras.layers.Dense(num_sources, activation='softmax')(lstm_layer)

        ret_model = keras.models.Model(inputs=input_layer, outputs=output_layer)

        ret_model.compile(
            loss='categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )

        return ret_model
