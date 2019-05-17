import keras


class TopologyFactory:

    def build(self, kernel_regularizer=0, dropout=0):
        raise NotImplementedError('Must use implementor.')


class OccurrenceTopologyFactory(TopologyFactory):

    def __init__(self, dense_size_1=8, dense_size_2=8, kernel_reg_penalty=0, dropout_rate=0):
        self.__dense_size_1 = dense_size_1
        self.__dense_size_2 = dense_size_2
        self.__kernel_reg_penalty = kernel_reg_penalty
        self.__dropout_rate = dropout_rate

    def build(self, num_words, num_sources):
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

    def __init__(self, max_seq_len=250, lstm_size=32, kernel_reg_penalty=0):
        self.__max_seq_len = max_seq_len
        self.__lstm_size = lstm_size
        self.__kernel_reg_penalty = kernel_reg_penalty

    def build(self, num_words, num_sources):
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
