import json
import multiprocessing
import sys

import harness_util

NUM_ARGS = 1
USAGE_STR = 'python run_set.py [json_file]'


def main():

    if len(sys.argv) < NUM_ARGS + 1:
        print(USAGE_STR)
        return

    json_file_path = sys.argv[1]
    harness_factory = harness_util.TemplateHarnessFactory()

    print('>>> Reading ' + json_file_path)
    with open(json_file_path) as f:
        contents = json.load(f)

    for next_named_config in contents['configs']:
        def process(named_config):
            name = named_config['name']
            print('>>> Running ' + name)
            config = named_config['config']
            harness = harness_factory.build(config)
            harness.run('who-wrote-this', name, config)

        process = multiprocessing.Process(target=process, args=(next_named_config,))
        process.start()
        process.join()


if __name__ == '__main__':
    main()
