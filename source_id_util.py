"""Utilities to convert news sources like NPR to integer ids.

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


class NumericalSourceIdSet:
    """Mapping of sources to unique integer IDs."""

    def __init__(self, mapping, num_sources):
        """Create a new source mapping.

        Args:
            mapping: The mapping's contents as a dictionary with sources as keys and integer IDs as
                values.
            num_sources: The number of sources included in the mapping. Should be the max of
                mapping's values.
        """
        self.__mapping = mapping
        self.__num_sources = num_sources

    def get_num_sources(self):
        """Get the number of sources included in the mapping.

        Returns:
            Integer number of sources included in this mapping.
        """
        return self.__num_sources

    def get_id(self, source, default_value=-1):
        """Get the integer ID for a given source.

        Args:
            source: The name of the news agency like NPR.
            default_value: The default value to return if the source is not found. Defaults to -1.
        Returns:
            Integer ID associated with the input source.
        """
        return self.__mapping.get(source, default_value)

    def get_mapping(self):
        """Get the raw dictionary mapping.

        Returns:
            Dictionary whose string keys are the source names and whose values are the unique IDs
            for those sources.
        """
        return self.__mapping


class NumericalSourceVectorFacade:
    """Facade to produce and apply encodings of news sources as a NumericalSourceIdSet."""

    def __init__(self, source_col='source', id_col='source_id', vector_col='source_id_vector'):
        """Create a new facade operating on the given columns.

        Args:
            source_col: The name of the column with the source like CNN.
            id_col: The column into which the numerical ID for the soruce should be written.
            vector_col: The column into which the one hot encoding for the sources should be
                written.
        """
        self.__source_col = source_col
        self.__id_col = id_col
        self.__vector_col = vector_col

    def build_vectors(self, data_frame, create_id=True):
        """Create the source vectors.

        Args:
            data_frame: The data frame from which sources should be read and into which the encoding
                of those sources should be written.
            create_id: Flag indicating if the source ID and source ID vector columns should be
                written. If False, only the NumericalSourceIdSet will be returned but the data
                frame will be left unchanged. If True, the encoding columns will be written.
                Defaults to True.
        Returns:
            Newly created NumericalSourceIdSet.
        """
        source_id_set = self.__build_numerical_source_set(data_frame)

        if create_id:
            self.__add_source_id(data_frame, source_id_set)
            self.__add_source_id_vector(data_frame, source_id_set)

        return source_id_set

    def __build_numerical_source_set(self, data_frame):
        """Build the NumericalSourceIdSet from the given data frame.

        Args:
            data_frame: The data frame from which the sources should be read.
        Returns:
            Newly created NumericalSourceIdSet.
        """
        news_source_mapping = {}

        i = 0
        for source in data_frame[self.__source_col].unique():
            news_source_mapping[source] = i
            i += 1

        return NumericalSourceIdSet(news_source_mapping, i)

    def __add_source_id(self, data_frame, numerical_source_set):
        """Add the source ID column to the given data frame.

        Args:
            data_frame: The data frame into which the ID column should be written. This frame will
                be modified in place.
            numerical_source_set: The source ID set through which the IDs should be generated.
        """
        data_frame[self.__id_col] = data_frame[self.__source_col].apply(
            lambda x: numerical_source_set.get_id(x)
        )

    def __create_source_id_vector(self, source_id, num_sources):
        """Create a one-hot encoding ID vector.

        Args:
            source_id: The numeric ID of the source being encoded.
            num_sources: The total number of news sources within the dataset.
        Returns:
            A numpy.array that represents the one-hot encoding of the input source id.
        """
        ret_vector = numpy.zeros(num_sources)
        ret_vector[source_id] = 1
        return ret_vector

    def __add_source_id_vector(self, data_frame, numerical_source_set):
        """Add the source ID vector into the given data frame.

        Args:
            data_frame: The data frame into which the one-hot encoding vector should be written.
                This frame will be modified in place.
            numerical_source_set: The NumericalSourceIdSet to use in generating the vector.
        """
        data_frame[self.__vector_col] = data_frame[self.__id_col].apply(
            lambda x: self.__create_source_id_vector(x, numerical_source_set.get_num_sources())
        )
