"""Run a collection of configurations for the test harness.

Run a collection of configurations for the test harness which are represented as a JSON file file
with a configs key whose json array value contains individual configurations to be executed. It
expects JSON like:

{
    "configs": [
	    {
            "name": "descr-occ-accept-fix-1",
			"config": {
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
        }
    ]
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
import multiprocessing
import sys

import harness_util

NUM_ARGS = 1
USAGE_STR = 'python run_set.py [json_file]'


def run_configuration(contents, verbose=True):
    """Run a set of configurations.

    Args:
        contents: Dictionary which has a 'contents' key whose list value contains configurations
            that should be run.
        verbose: Flag indicating if status updates should be printed. Defaults to true.
    """
    harness_factory = harness_util.TemplateHarnessFactory()

    for next_named_config in contents['configs']:

        def process(named_config):
            name = named_config['name']

            if verbose:
                print('>>> Running ' + name)

            config = named_config['config']
            harness = harness_factory.build(config)
            harness.run('who-wrote-this', name, config)

        process = multiprocessing.Process(target=process, args=(next_named_config,))
        process.start()
        process.join()


def run_file(json_file_path, verbose=True):
    """Run all of the configurations found within a file.

    Args:
        json_file_path: The string path to the file with a series of configurations with which a
            training harness should be run.
        verbose: Flag indicating if status updates should be printed. Defaults to true.
    """
    if verbose:
        print('>>> Reading ' + json_file_path)

    with open(json_file_path) as f:
        contents = json.load(f)

    run_configuration(contents, verbose=verbose)


def main():
    """Run the script using CLI args."""
    if len(sys.argv) < NUM_ARGS + 1:
        print(USAGE_STR)
        return

    json_file_path = sys.argv[1]



if __name__ == '__main__':
    main()
