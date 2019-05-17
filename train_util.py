import keras
import sklearn.utils
import numpy
import wandb
import wandb.keras


class Trainer:

    def train(self, data_frame, model, epochs=None, validation_split=None):
        raise NotImplementedError('Must use implementor.')


class OccurrenceTrainer(Trainer):

    def __init__(self, train_vector_col, source_id_vector_col, source_col, fox_weight,
            set_assignment_col='set_assignment'):

        self.__set_assignment_col = set_assignment_col
        self.__train_vector_col = train_vector_col
        self.__source_id_vector_col = source_id_vector_col
        self.__source_col = source_col
        self.__fox_weight = fox_weight

    def train(self, data_frame, model, epochs=30):
        training_data = data_frame[data_frame[self.__set_assignment_col] == 'train']
        training_data_fox = data_frame[data_frame[self.__source_col] == 'Fox']

        x_train_reg = numpy.array(training_data[self.__train_vector_col].tolist())
        y_train_reg = numpy.array(training_data[self.__source_id_vector_col].tolist())

        x_train_fox = numpy.array(training_data_fox[self.__train_vector_col].tolist())
        x_train_fox = x_train_fox[:round(self.__fox_weight * training_data_fox.shape[0])]

        y_train_fox = numpy.array(training_data_fox[self.__source_id_vector_col].tolist())
        y_train_fox = y_train_fox[:round(self.__fox_weight * training_data_fox.shape[0])]

        x_train = numpy.concatenate((x_train_reg, x_train_fox))
        y_train = numpy.concatenate((y_train_reg, y_train_fox))

        training_data_valid = data_frame[data_frame[self.__set_assignment_col] == 'validation']
        x_train_valid = numpy.array(training_data_valid[self.__train_vector_col].tolist())
        y_train_valid = numpy.array(training_data_valid[self.__source_id_vector_col].tolist())

        model.fit(
            x_train,
            y_train,
            epochs=epochs,
            validation_data=(x_train_valid, y_train_valid),
            callbacks=[wandb.keras.WandbCallback()]
        )


class SequenceTrainer(Trainer):

    def __init__(self, train_vector_col, source_id_vector_col, source_col, max_seq_len,
            fox_weight, set_assignment_col='set_assignment'):

        self.__set_assignment_col = set_assignment_col
        self.__train_vector_col = train_vector_col
        self.__source_id_vector_col = source_id_vector_col
        self.__source_col = source_col
        self.__max_seq_len = max_seq_len
        self.__fox_weight = fox_weight
        self.__set_assignment_col = set_assignment_col

    def train(self, data_frame, model, epochs=30):
        training_data = data_frame[data_frame[self.__set_assignment_col] == 'train']
        training_data_fox = data_frame[data_frame[self.__source_col] == 'Fox']

        x_train_reg = numpy.array(training_data[self.__train_vector_col].tolist())
        y_train_reg = numpy.array(training_data[self.__source_id_vector_col].tolist())

        x_train_fox = numpy.array(training_data_fox[self.__train_vector_col].tolist())
        x_train_fox = x_train_fox[:round(self.__fox_weight * training_data_fox.shape[0])]

        y_train_fox = numpy.array(training_data_fox[self.__source_id_vector_col].tolist())
        y_train_fox = y_train_fox[:round(self.__fox_weight * training_data_fox.shape[0])]

        x_train = numpy.concatenate((x_train_reg, x_train_fox))
        y_train = numpy.concatenate((y_train_reg, y_train_fox))

        x_train_pad = keras.preprocessing.sequence.pad_sequences(
            x_train,
            maxlen=self.__max_seq_len
        )

        training_data_valid = data_frame[data_frame[self.__set_assignment_col] == 'validation']
        x_train_valid = numpy.array(training_data_valid[self.__train_vector_col].tolist())
        y_train_valid = numpy.array(training_data_valid[self.__source_id_vector_col].tolist())
        x_train_pad_valid = keras.preprocessing.sequence.pad_sequences(
            x_train_valid,
            maxlen=self.__max_seq_len
        )

        model.fit(
            x_train_pad,
            y_train,
            epochs=epochs,
            validation_data=(x_train_pad_valid, y_train_valid),
            callbacks=[wandb.keras.WandbCallback()]
        )
