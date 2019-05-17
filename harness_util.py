import wandb

import data_util
import input_vector_util
import source_id_util
import tokenize_util
import topology_util
import train_util


def get_num_articles(data_frame):
    return data_frame.count()[0]


def get_num_words(data_frame, tokens_col):
    return max(data_frame[tokens_col].apply(lambda x: max(x) if len(x) > 0 else 0))


def get_max_seq_len(data_frame, tokens_col):
    return max(data_frame['title_tokens'].apply(lambda x: len(x)))


class TemplateHarnessFactory:

    def __init__(self):
        self.__vectorizers = {
            'occurrence': lambda config: input_vector_util.OccurenceInputVectorizer(),
            'sequence': lambda config: input_vector_util.SequenceInputVectorizer()
        }

        self.__topology_factories = {
            'occurrence': lambda config: topology_util.OccurrenceTopologyFactory(
                dense_size_1=config['denseSize1'],
                dense_size_2=config['denseSize2'],
                kernel_reg_penalty=config['kernelRegPenalty'],
                dropout_rate=config['dropoutRate']
            ),
            'sequence': lambda config: topology_util.SequenceTopologyFactory(
                max_seq_len=config['maxSeqLen'],
                lstm_size=config['lstmSize'],
                kernel_reg_penalty=config['kernelRegPenalty']
            )
        }

        self.__trainers = {
            'occurrence': lambda config: train_util.OccurrenceTrainer(
                config['tokenVectorCol'],
                config['sourceIdVectorCol'],
                config['sourceCol'],
                config.get('foxWeight', 1)
            ),
            'sequence': lambda config: train_util.SequenceTrainer(
                config['tokenVectorCol'],
                config['sourceIdVectorCol'],
                config['sourceCol'],
                config['maxSeqLen'],
                config.get('foxWeight', 1)
            )
        }

    def build(self, config):
        data_loader = data_util.DataLoader()

        source_vector_factory = source_id_util.NumericalSourceVectorFactory(
            source_col=config['sourceCol'],
            id_col=config['sourceIdCol'],
            vector_col=config['sourceIdVectorCol']
        )

        method = config['method']

        tokenizer = tokenize_util.Tokenizer(
            config['corpusCol'],
            config['tokensCol'],
            config['tokenVectorCol'],
            config['numWords'],
            self.__vectorizers[method](config)
        )

        topology_factory = self.__topology_factories[method](config)

        trainer = self.__trainers[method](config)

        return TemplateHarness(
            data_loader,
            source_vector_factory,
            tokenizer,
            topology_factory,
            trainer
        )


class HarnessResults:

    def __init__(self, data_frame, source_ids, model, data_loader, source_vector_factory,
            tokenizer, topology_factory, trainer):

        self.__data_frame = data_frame
        self.__source_ids = source_ids
        self.__model = model
        self.__data_loader = data_loader
        self.__source_vector_factory = source_vector_factory
        self.__tokenizer = tokenizer
        self.__topology_factory = topology_factory
        self.__trainer = trainer

    def get_data_frame(self):
        return self.__data_frame

    def get_source_ids(self):
        return self.__source_ids

    def get_model(self):
        return self.__model

    def get_data_loader(self):
        return self.__data_loader

    def get_source_vector_factory(self):
        return self.__source_vector_factory

    def get_tokenizer(self):
        return self.__tokenizer

    def get_topology_factory(self):
        return self.__topology_factory

    def get_trainer(self):
        return self.__trainer


class TemplateHarness:

    def __init__(self, data_loader, source_vector_factory, tokenizer, topology_factory, trainer):
        self.__data_loader = data_loader
        self.__source_vector_factory = source_vector_factory
        self.__tokenizer = tokenizer
        self.__topology_factory = topology_factory
        self.__trainer = trainer

    def run(self, project, name, config):
        data_frame = self.__data_loader.load_data()

        # Convert source to a one hot vector
        source_ids = self.__source_vector_factory.build_vectors(data_frame)

        # Tokenize the target column and convert to one hot vector
        self.__tokenizer.tokenize(data_frame)
        self.__tokenizer.convert_tokens_to_vector(data_frame)

        # Build the keras topology
        num_words = get_num_words(data_frame, config['tokensCol'])
        num_sources = source_ids.get_num_sources()
        model = self.__topology_factory.build(num_words, num_sources)

        # Train
        wandb.init(
            project=project,
            name=name,
            config=config,
            reinit=True,
            tags=['fixed-set', 'html-to-text', 'fox-balanced-all', 'no-ads', 'no-self-ref', 'no-place']
        )

        self.__trainer.train(data_frame, model)

        return HarnessResults(
            data_frame,
            source_ids,
            model,
            self.__data_loader,
            self.__source_vector_factory,
            self.__tokenizer,
            self.__topology_factory,
            self.__trainer
        )
