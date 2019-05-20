"""Template method ("harness") which uses given set of implementors to run the ML pipeline.

The other utilities provide implementations of strategies that are referenced polymorphically from
this template method which runs training on articles to produce a new authorship classifier.

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

import wandb

import data_util
import input_vector_util
import source_id_util
import tokenize_util
import topology_util
import train_util


def get_num_words(data_frame, tokens_col):
    """Get the maximum token found within a column.

    Args:
        data_frame: The frame from which the max value should be found.
        tokens_col: The string column name to be returned.
    Returns:
        Maximum token found within the given column.
    """
    return max(data_frame[tokens_col].apply(lambda x: max(x) if len(x) > 0 else 0))


class TemplateHarnessFactory:
    """Factory which builds a template harness."""

    def __init__(self):
        """Create a new template harness with cached large objects."""
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
                config.get('foxWeight', 1),
                use_wandb=config.get('useWandb', True),
                epochs=config.get('epochs', 30)
            ),
            'sequence': lambda config: train_util.SequenceTrainer(
                config['tokenVectorCol'],
                config['sourceIdVectorCol'],
                config['sourceCol'],
                config['maxSeqLen'],
                config.get('foxWeight', 1),
                use_wandb=config.get('useWandb', True),
                epochs=config.get('epochs', 30)
            )
        }

    def build(self, config, conn=None, db_loc='articles.db'):
        """Build a new test harness.

        Args:
            config: Dictionary describing how the harness should be run.
            conn: DB API v2 connection from which the harness should get its data. If None, will
                use the sqlite path provided in db_loc. Defaults to None.
            db_loc: String path to the sqlite database from which the harness should get its data.
                Ignored if conn is not None.
        Returns:
            Create a new TemplateHarness loaded with strategies.
        """
        data_loader = data_util.DataLoader(conn=conn, db_loc=db_loc)

        source_vector_facade = source_id_util.NumericalSourceVectorFacade(
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
            source_vector_facade,
            tokenizer,
            topology_factory,
            trainer
        )


class HarnessResults:
    """Structure containing results from running a TemplateHarness."""

    def __init__(self, data_frame, source_ids, model, data_loader, source_vector_facade,
            tokenizer, topology_factory, trainer):
        """Create a new structure holding results from running a TemplateHarness.

        Args:
            data_frame: The data frame from which data was read to train the model and into which
                some intermediate data structures like the tokens were written.
            source_ids: The NumericalSourceIdSet through which sources were converted to integers.
            model: The keras.models.Model trained.
            data_loader: The DataLoader used to get article data.
            source_vector_facade: The InputVectorizer used to generate vectors for article data.
            tokenizer: The Tokenizer used to convert the input strings to tokens.
            topology_factory: The TopologyFactory used to build the model prior to training.
            trainer: The Trainer used to train the returned model.
        """

        self.__data_frame = data_frame
        self.__source_ids = source_ids
        self.__model = model
        self.__data_loader = data_loader
        self.__source_vector_facade = source_vector_facade
        self.__tokenizer = tokenizer
        self.__topology_factory = topology_factory
        self.__trainer = trainer

    def get_data_frame(self):
        """Get the data frame from which data were written and into which intermediate were written.

        Return:
            The data frame from which data was read to train the model and into which some
            intermediate data structures like the tokens were written.
        """
        return self.__data_frame

    def get_source_ids(self):
        """Get the mapping to source IDs.

        Returns:
            The NumericalSourceIdSet through which sources were converted to integers.
        """
        return self.__source_ids

    def get_model(self):
        """Get the trained keras model.

        Returns:
            The keras.models.Model trained.
        """
        return self.__model

    def get_data_loader(self):
        """Get the utility used to load article data.

        Returns:
            The DataLoader used to get article data.
        """
        return self.__data_loader

    def get_source_vector_facade(self):
        """Get the utility that vectorized source tokens.

        Returns:
            The InputVectorizer used to generate vectors for article data.
        """
        return self.__source_vector_facade

    def get_tokenizer(self):
        """Get the utility that converted strings to tokens.

        Returns:
            The Tokenizer used to convert the input strings to tokens.
        """
        return self.__tokenizer

    def get_topology_factory(self):
        """Get the factory that built the keras neural network.

        Returns:
            The TopologyFactory used to build the model prior to training.
        """
        return self.__topology_factory

    def get_trainer(self):
        """Get the utility that trained the returned model.

        Returns:
            The Trainer used to train the returned model.
        """
        return self.__trainer


class TemplateHarness:
    """Template method that trains a model."""

    def __init__(self, data_loader, source_vector_facade, tokenizer, topology_factory, trainer):
        """Generate a template method using the given strategies.

        Args:
            data_loader: The utility to use to load article data.
            source_vector_facade: The InputVectorizer to generate vectors for article data.
            tokenizer: The Tokenizer used to convert the input strings to tokens.
            topology_factory: The TopologyFactory to build the model prior to training.
            trainer:The Trainer to train the returned model.
        """
        self.__data_loader = data_loader
        self.__source_vector_facade = source_vector_facade
        self.__tokenizer = tokenizer
        self.__topology_factory = topology_factory
        self.__trainer = trainer

    def run(self, project, name, config):
        """Build and train a new classifier.

        Args:
            project: The string name of the project with which this run should be associated. Will
                be reported to W&B if enabled.
            name: The string name of the run. Will be reported to W&B if enabled.
            config: Dictionary with configuration information with which the harness should be run.
        """
        data_frame = self.__data_loader.load_data()

        # Convert source to a one hot vector
        source_ids = self.__source_vector_facade.build_vectors(data_frame)

        # Tokenize the target column and convert to one hot vector
        self.__tokenizer.tokenize(data_frame)
        self.__tokenizer.convert_tokens_to_vector(data_frame)

        # Build the keras topology
        num_words = get_num_words(data_frame, config['tokensCol'])
        num_sources = source_ids.get_num_sources()
        model = self.__topology_factory.build(num_words, num_sources)

        # Train
        if config.get('useWandb', True):
            wandb.init(
                project=project,
                name=name,
                config=config,
                reinit=True,
                tags=[
                    'fixed-set',
                    'html-to-text',
                    'fox-balanced-all',
                    'no-ads',
                    'no-self-ref',
                    'no-place'
                ]
            )

        self.__trainer.train(data_frame, model)

        return HarnessResults(
            data_frame,
            source_ids,
            model,
            self.__data_loader,
            self.__source_vector_facade,
            self.__tokenizer,
            self.__topology_factory,
            self.__trainer
        )
