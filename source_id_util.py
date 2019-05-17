import numpy


class NumericalSourceIdSet:

    def __init__(self, mapping, num_sources):
        self.__mapping = mapping
        self.__num_sources = num_sources

    def get_num_sources(self):
        return self.__num_sources

    def get_id(self, source, default_value=-1):
        return self.__mapping.get(source, default_value)


class NumericalSourceVectorFactory:

    def __init__(self, source_col='source', id_col='source_id', vector_col='source_id_vector'):
        self.__source_col = source_col
        self.__id_col = id_col
        self.__vector_col = vector_col

    def build_vectors(self, data_frame):
        source_id_set = self.__build_numerical_source_set(data_frame)
        self.__add_source_id(data_frame, source_id_set)
        self.__add_source_id_vector(data_frame, source_id_set)
        return source_id_set

    def __build_numerical_source_set(self, data_frame):
        news_source_mapping = {}

        i = 0
        for source in data_frame[self.__source_col].unique():
            news_source_mapping[source] = i
            i += 1

        return NumericalSourceIdSet(news_source_mapping, i)

    def __add_source_id(self, data_frame, numerical_source_set):
        data_frame[self.__id_col] = data_frame[self.__source_col].apply(
            lambda x: numerical_source_set.get_id(x)
        )

    def __create_source_id_vector(self, source_id, num_sources):
        ret_vector = numpy.zeros(num_sources)
        ret_vector[source_id] = 1
        return ret_vector

    def __add_source_id_vector(self, data_frame, numerical_source_set):
        data_frame[self.__vector_col] = data_frame[self.__id_col].apply(
            lambda x: self.__create_source_id_vector(x, numerical_source_set.get_num_sources())
        )
