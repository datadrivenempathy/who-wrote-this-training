Who Wrote This Training
====================================================================================================
Code and reference configurations used in research for https://whowrotethis.com and "Machine Learning Techniques for Detecting Identifying Linguistic Patterns in the News Media" by [A. Samuel Pottinger](https://gleap.org). Released under the MIT license. For data, please see https://whowrotethis.com.

<br>
<br>

Purpose
----------------------------------------------------------------------------------------------------
This repository provides a harness based on the [Template Method](https://sourcemaking.com/design_patterns/template_method) pattern to train a neural network to predict from which news agency an article was published given only a short snippet of text. When used from the command line, it takes in a JSON file describing how to run the harness and typically a [SQLite](https://www.sqlite.org/index.html) database with article information. These scripts can also optionally report results out to [Weights and Biases](https://www.wandb.com/) (referred to as W&B).

<br>
<br>

Environment Setup
----------------------------------------------------------------------------------------------------
These scripts will require Python 3, pip, and a number of supporting libraries. [Setup instructions for the language are platform specific](https://realpython.com/installing-python/). Note that users may choose to use a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/) though the specifics of that setup are not discussed here. Finally, users will require a database of articles which is available from https://whowrotethis.com.

After having Python, pip, optionally a virtual environment set up, and a copy of the articles database, one can install the supporting libraries by executing `$ pip install -r requirements.txt`.

<br>
<br>

Usage
----------------------------------------------------------------------------------------------------
While these scripts can be imported to other Python code, typical usage will come from command line operation. This can be done either by running many scripts or a single configuration. Those configurations are described below.

<br>

**Running a single configuration**

Running a single configuration will cause a new model to be trained and predictions using that model to be persisted into the input sqlite database. The required script can be run from the command line with `$ python run_single.py [path to json config] [project name] [run name] [path to sqlite] [write predictions] [optional output path for accuracy] [optional output path for source performance] [optional path for predictions output]`. The arguments are as follows:

 - The path to the JSON configuration (as described below) with which to execute the pipeline.
 - The name of the project. This will be used with W&B if enabled.
 - The name to give to this specific execution. This will be used with W&B if enabled.
 - Path to the sqlite database from which article information will be read and into which predictions will be written.
 - If 't' (case-insensitive), will write predictions to SQLite database. Otherwise, predictions will not be persisted.
 - Optional path to where accuracy statistics (test, train, and validation) should be written.
 - Optional path to where source by source performance statistics (precision, recall) should be written.
 - Optional path to where predictions should be written.

An example of a single configuration file is at `config/selected_network.json`.

<br>

**Running multiple configurations**

Running multiple configurations will train multiple models, optionally writing the results to W&B. This will _not_ cause predictions to be persisted into the sqlite database. The required script can be run from the command line with `$ python run_set.py [json_file] [db loc]`. The arguments are as follows:

 - The path to the JSON configurations (as described below) with which to execute the pipeline.
 - Path to the sqlite database from which article information will be read.

An example of a multiple configuration file is at `config/configs_combined.json`.

<br>

**Configuration options**

The available configuration settings for a single configuration are as follows:

 - `corpusCol`: The name of the column like `description` from the database from which the model will be trained.
 - `denseSize1`: If using the feed forward network occurrence network, this the number of units to appear in the first dense layer.
 - `denseSize2`: If using the feed forward network occurrence network, this the number of units to appear in the second dense layer.
 - `dropoutRate`: The dropout rate to use for internal layers of a network from 0 to 1.
 - `kernelRegPenalty`: The L2 activation penalty to apply for internal layers of a network from 0 to 1.
 - `lstmSize`: If using the recurrent sequence LSTM network, the number of LSTM units to appear in the model.
 - `maxSeqLen`: If using the recurrent sequence LSTM network, the maximum sequence length to feed into the network. Sequences will be cut to [0,n) tokens or padded to be of length n where n equals this value.
 - `method`: The type of network to use. The value of "occurrence" will cause the pipeline to train with the feed forward network operating on word occurrences / co-occurrences. The value of "sequence" will cause the pipeline to train with the LSTM recurrent structure.
 - `numWords`: The maximum number of words with which to train. The top most frequent "n" words will be retained where n equals the value of this parameter.
 - `sourceCol`: The name of the column from the database indicating which news agency published an article.
 - `sourceIdCol`: The data frame column in which the unique numeric ID of an agency should be written. This value is not persisted but is useful when debugging.
 - `sourceIdVectorCol`: The data frame column in which a vectorization of an agency should be written. This value is not persisted but is useful when debugging.
 - `tokenVectorCol`: The data frame column in which the vectorization of the article content should be written. This value is not persisted but is useful when debugging.
 - `tokensCol`: The data frame column in which the tokenization of the article content should be written. This value is not persisted but is useful when debugging.

There are the following optional parameters as well:

 - `foxWeight`: The amount of resampling to apply for Fox between 0 (no resampling) and 1 (every article duplicated). This only impacts the training set. Defaults to 1.
 - `useWandb`: Flag indicating if results should be reported to Weights and Biases. Defaults to True.
 - `epochs`: The number of epochs for which the model should be trained. Defaults to 30.

<br>

**Database structure**

Note that the scripts expect a table or view in the sqlite database called `articles_clean_assigned` which can be created using `script/create_sets.py` and has the following columns:

 - `source`: String column indicating which agency published the article (represented by the row).
 - `title`: The text of the tile for the article (represented by the row).
 - `description`: The description provided the for the article (represented by the row) by the publishing agency.
 - `setAssignemnt`: Strings 'test', 'train', or 'validation' indicating in which set the article was assigned.

If persisting results of the model (using `run_single.py`), the predictions will be saved to a new table called `predictions`.

<br>

**File Formats**

For the JSON input files, running `run_single.py` expects a single JSON object with the configuration as demonstrated in `condfig/selected_network.json`. Meanwhile, running `run_set.py` expects a root object with the attribute `configs` which itself contains an array of objects with attributes `name` (the name of the configuration, will be reported as the "run name" in W&B) and `config` (the configuration as described above). See `config/configs_combined.json` for an example. One may also optionally include `project` in the root object for `run_set.py` which will override the name of the W&B project with which the run will be associated.

<br>

**Lime**

Note that LIME data is generated through the notebook at `notebook/Run Manually.ipnyb`.

<br>
<br>

Testing
----------------------------------------------------------------------------------------------------
Automated tests are provided via the Python standard `unittest` library. Simply execute nosetests to run:

```
$ nosetests
........................
----------------------------------------------------------------------
Ran 24 tests in 9.934s

OK
```

<br>
<br>

Release
----------------------------------------------------------------------------------------------------
This model itself does not have a release to production step but the sqlite database after running `run_single.py` can be used with the Who Wrote This open source web application or can be evaluated using SQL scripts provided in the `sql` directory.

<br>
<br>

Coding Standards
----------------------------------------------------------------------------------------------------
Please provide unit tests where possible and conform to the [Google Python and documentation style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md) where possible.

<br>
<br>

Related Projects
----------------------------------------------------------------------------------------------------
Note that this is in a series of related projects as linked:

 - [who-wrote-this-training](https://github.com/datadrivenempathy/who-wrote-this-training): logic for machine learning.
 - [who-wrote-this-server](https://github.com/datadrivenempathy/who-wrote-this-server): web application to demo the model.
 - [who-wrote-this-news-crawler](https://github.com/datadrivenempathy/who-wrote-this-news-crawler): crawler to record RSS feeds.

<br>
<br>

License and Open Source Libraries Used
----------------------------------------------------------------------------------------------------
This project is made available under the [MIT license](https://opensource.org/licenses/MIT) as described in `LICENSE.txt`. It uses the following open source libraries internally:

 - [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) used under the [MIT license](https://opensource.org/licenses/MIT).
 - [gensim](https://radimrehurek.com/gensim/) used under the [LGPLv2 license](https://github.com/RaRe-Technologies/gensim/blob/develop/COPYING).
 - [Keras](https://keras.io/) used under the [MIT license](https://github.com/keras-team/keras/blob/master/LICENSE).
 - [lime](https://github.com/marcotcr/lime) used under the [BSD license](https://github.com/marcotcr/lime/blob/master/LICENSE).
 - [lxml](https://lxml.de/) used under the [BSD license](https://github.com/lxml/lxml/blob/master/doc/licenses/BSD.txt).
 - [numpy](https://www.numpy.org/) used under the [BSD license](https://www.numpy.org/license.html#license).
 - [pandas](https://pandas.pydata.org/) used under the [BSD license](http://pandas.pydata.org/pandas-docs/stable/getting_started/overview.html#license).
 - [scikit_learn](https://scikit-learn.org/stable/) used under the [BSD license](https://github.com/scikit-learn/scikit-learn/blob/master/COPYING).
 - [tabulate](https://bitbucket.org/astanin/python-tabulate) used under the [MIT license](https://bitbucket.org/astanin/python-tabulate/src/master/LICENSE).
 - [tensorflow v1](https://www.tensorflow.org/) used under the [Apache v2 License](https://github.com/tensorflow/tensorflow/blob/master/LICENSE).
 - [textblob](https://textblob.readthedocs.io/en/dev/) used under the [MIT license](https://textblob.readthedocs.io/en/dev/license.html).
 - [wandb](https://www.wandb.com/) used under the [MIT license](https://github.com/wandb/client/blob/master/LICENSE).
