"""Utility to execute a single configuration.

Train an article authorship classifier and save predictions using a configuration given as a Python
dictionary or path to JSON file. It expects JSON like:

{
    "corpusCol": "description",
    "denseSize1": 32,
    "denseSize2": 16,
    "dropoutRate": 0,
    "kernelRegPenalty": 0.01,
    "method": "occurrence",
    "numWords": 30000,
    "sourceCol": "source",
    "sourceIdCol": "sourceId",
    "sourceIdVectorCol": "sourceIdVector",
    "tokenVectorCol": "tokenVector",
    "tokensCol": "tokens"
}

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

import json
import sqlite3
import sys

import keras
import numpy
import pandas

import harness_util

NUM_ARGS = 5
USAGE_STR = 'python run_single.py [path to json config] [project name] [run name] [path to sqlite] [write predictions]'


def run_config(config, project_name, run_name, conn, write_predictions):
    """Train an article authorship classifier and save predictions.

    Args:
        config: Python dictionary describing with what parameters the harness should run.
        project_name: The name of the project. Will be used in wandb if enabled.
        run_name: The name of the run. Will be used in wandb if enabled.
        conn: DB API v2 compliant database connection.
        write_predictions: Flag indicating if predictions should be written to the db.
    """
    harness_factory = harness_util.TemplateHarnessFactory()
    harness = harness_factory.build(config, conn=conn)
    results = harness.run(project_name, run_name, config)

    target_frame = results.get_data_frame()
    model = results.get_model()

    if not write_predictions:
        return

    vector_frame_col = target_frame[config['tokenVectorCol']]
    vector_array = numpy.array(vector_frame_col.tolist())

    if config['method'] == 'sequence':
        vector_array = keras.preprocessing.sequence.pad_sequences(
            vector_array,
            maxlen=config['maxSeqLen']
        )

    predictions = model.predict(vector_array)
    source_mapping = results.get_source_ids().get_mapping()

    source_mapping_invert = {}
    for source in source_mapping:
        source_index = source_mapping[source]
        target_frame[source + '_prediction'] = predictions[:,source_index]
        source_mapping_invert[source_index] = source

    target_frame['prediction'] = list(map(
        lambda x: source_mapping_invert[x],
        numpy.argmax(predictions, axis=1)
    ))

    output_frame = pandas.DataFrame()
    output_frame['title'] = target_frame['title']
    output_frame['description'] = target_frame['description']
    output_frame['actualSource'] = target_frame[config['sourceCol']]
    output_frame['setAssignment'] = target_frame['set_assignment']
    output_frame['cnnScore'] = target_frame['CNN_prediction']
    output_frame['foxScore'] = target_frame['Fox_prediction']
    output_frame['dailyMailScore'] = target_frame['Daily Mail_prediction']
    output_frame['drudgeReportScore'] = target_frame['Drudge Report_prediction']
    output_frame['newYorkTimesScore'] = target_frame['New York Times_prediction']
    output_frame['bbcScore'] = target_frame['BBC_prediction']
    output_frame['breitbartScore'] = target_frame['Breitbart_prediction']
    output_frame['wallStreetJournalScore'] = target_frame['Wall Street Journal_prediction']
    output_frame['voxScore'] = target_frame['Vox_prediction']
    output_frame['nprScore'] = target_frame['NPR_prediction']
    output_frame['prediction'] = target_frame['prediction']

    output_frame.to_sql('predictions', conn)
    conn.commit()


def main():
    """Run a single configuration through the pipeline using command line arguments."""
    if len(sys.argv) != NUM_ARGS + 1:
        print(USAGE_STR)
        return

    config_path = sys.argv[1]
    project_name = sys.argv[2]
    run_name = sys.argv[3]
    conn_path = sys.argv[4]
    write_predictions = sys.argv[5].lower() == 't'

    with open(config_path) as f:
        config = json.load(f)

    conn = sqlite3.connect(conn_path)

    run_config(config, project_name, run_name, conn, write_predictions)


if __name__ == '__main__':
    main()
