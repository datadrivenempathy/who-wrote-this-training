"""Utility to train keras models.

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
import sklearn.utils
import numpy
import wandb
import wandb.keras


class Trainer:
    """Interface for strategies to train different keras models."""

    def train(self, data_frame, model, epochs=None):
        """Train a new keras model.

        Args:
            data_frame: The data frame from which article data should be read.
            model: The keras.models.Model to be trained.
            epochs: The number of epochs over which the model should be trained.
        """
        raise NotImplementedError('Must use implementor.')


class OccurrenceTrainer(Trainer):
    """Strategy to train a feed forward network on word occurrences / co-ocurrences."""

    def __init__(self, train_vector_col, source_id_vector_col, source_col, fox_weight,
            epochs=30, set_assignment_col='set_assignment', use_wandb=True):
        """Create a new occurrence training strategy.

        Args:
            train_vector_col: The name of the column with the input vector.
            source_id_vector_col: The name of the column with the output.
            source_col: The column with the name of the news source.
            fox_weight: The amount of fox resampling from 0 (no resampling) to 1 (every article
                resampled once).
            epochs: The number of epochs for which the model should be trained. Defaults to 30.
            set_assignment_col: The column indicating in which set (train, test, validation) an
                instance is assigned. Defaults to set_assignment.
            use_wandb: Flag indicating if results should be reported to W&B. Defaults to True.
        """

        self.__set_assignment_col = set_assignment_col
        self.__train_vector_col = train_vector_col
        self.__source_id_vector_col = source_id_vector_col
        self.__source_col = source_col
        self.__fox_weight = fox_weight
        self.__epochs = epochs
        self.__use_wandb = use_wandb

    def train(self, data_frame, model):
        """Train a feed forward model.

        Args:
            data_frame: The data frame from which article data should be read.
            model: The keras.models.Model to be trained.
        """
        training_data = data_frame[data_frame[self.__set_assignment_col] == 'train']
        training_data_fox = data_frame[data_frame[self.__source_col] == 'Fox']

        x_train_reg = numpy.array(training_data[self.__train_vector_col].tolist())
        y_train_reg = numpy.array(training_data[self.__source_id_vector_col].tolist())

        x_train_fox = numpy.array(training_data_fox[self.__train_vector_col].tolist())
        x_train_fox = x_train_fox[:round(self.__fox_weight * training_data_fox.shape[0])]

        y_train_fox = numpy.array(training_data_fox[self.__source_id_vector_col].tolist())
        y_train_fox = y_train_fox[:round(self.__fox_weight * training_data_fox.shape[0])]

        if self.__fox_weight > 0:
            x_train = numpy.concatenate((x_train_reg, x_train_fox))
            y_train = numpy.concatenate((y_train_reg, y_train_fox))
        else:
            x_train = x_train_reg
            y_train = y_train_reg

        training_data_valid = data_frame[data_frame[self.__set_assignment_col] == 'validation']
        x_train_valid = numpy.array(training_data_valid[self.__train_vector_col].tolist())
        y_train_valid = numpy.array(training_data_valid[self.__source_id_vector_col].tolist())

        callbacks = []

        if self.__use_wandb:
            callbacks.append(wandb.keras.WandbCallback())

        model.fit(
            x_train,
            y_train,
            epochs=self.__epochs,
            validation_data=(x_train_valid, y_train_valid),
            callbacks=callbacks
        )


class SequenceTrainer(Trainer):
    """Strategy to train an LSTM network."""

    def __init__(self, train_vector_col, source_id_vector_col, source_col, max_seq_len,
            fox_weight, epochs=30, set_assignment_col='set_assignment', use_wandb=True):
        """Create a new LSTM training strategy.

        Args:
            train_vector_col: The name of the column with the input vector.
            source_id_vector_col: The name of the column with the output.
            source_col: The column with the name of the news source.
            fox_weight: The amount of fox resampling from 0 (no resampling) to 1 (every article
                resampled once).
            epochs: The number of epochs for which the model should be trained. Defaults to 30.
            set_assignment_col: The column indicating in which set (train, test, validation) an
                instance is assigned. Defaults to set_assignment.
            use_wandb: Flag indicating if results should be reported to W&B. Defaults to True.
        """

        self.__set_assignment_col = set_assignment_col
        self.__train_vector_col = train_vector_col
        self.__source_id_vector_col = source_id_vector_col
        self.__source_col = source_col
        self.__max_seq_len = max_seq_len
        self.__fox_weight = fox_weight
        self.__set_assignment_col = set_assignment_col
        self.__epochs = epochs
        self.__use_wandb = use_wandb

    def train(self, data_frame, model):
        """Train a sequence model.

        Args:
            data_frame: The data frame from which article data should be read.
            model: The keras.models.Model to be trained.
        """
        training_data = data_frame[data_frame[self.__set_assignment_col] == 'train']
        training_data_fox = data_frame[data_frame[self.__source_col] == 'Fox']

        x_train_reg = numpy.array(training_data[self.__train_vector_col].tolist())
        y_train_reg = numpy.array(training_data[self.__source_id_vector_col].tolist())

        x_train_fox = numpy.array(training_data_fox[self.__train_vector_col].tolist())
        x_train_fox = x_train_fox[:round(self.__fox_weight * training_data_fox.shape[0])]

        y_train_fox = numpy.array(training_data_fox[self.__source_id_vector_col].tolist())
        y_train_fox = y_train_fox[:round(self.__fox_weight * training_data_fox.shape[0])]

        if self.__fox_weight > 0:
            x_train = numpy.concatenate((x_train_reg, x_train_fox))
            y_train = numpy.concatenate((y_train_reg, y_train_fox))
        else:
            x_train = x_train_reg
            y_train = y_train_reg

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

        callbacks = []

        if self.__use_wandb:
            callbacks.append(wandb.keras.WandbCallback())

        model.fit(
            x_train_pad,
            y_train,
            epochs=self.__epochs,
            validation_data=(x_train_pad_valid, y_train_valid),
            callbacks=callbacks
        )
