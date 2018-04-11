#!/usr/bin/env python

import os
import sys
from subprocess import check_call, check_output
from datetime import datetime
import ruamel.yaml as yaml


def s3_get_config(key):
    check_call(['aws', 's3', 'cp', key, '/mnt/input/config.yml'])


def s3_get(input):
    path = input.strip()

    # Recursive sync/cp ignores single objects, so differentiate based
    # on the input path specified
    if path[len(path) - 1] == '/':
        check_call(['aws', 's3', 'sync', input, '/mnt/input/'])
    else:
        check_call(['aws', 's3', 'cp', input, '/mnt/input/'])


def s3_put(output, version, timestamp):
    check_call(['aws', 's3', 'sync', '/mnt/output/',
                os.path.join(output, version, timestamp)])


def run_ashlar(arguments):
    check_call(' '.join(['ashlar'] + arguments), shell=True)


def main():

    try:
        # Get config for this job
        if 'CONFIG' in os.environ:
            config = yaml.load(os.environ.get('CONFIG'), Loader=yaml.Loader)
        elif len(sys.argv) > 1:
            s3_get_config(sys.argv[1])
            with open('/mnt/input/config.yml') as f:
                config = yaml.load(f, Loader=yaml.Loader)
        else:
            raise ValueError('''A CONFIG environment variable or an S3 config
                                object must be provided''')

        # Sync the inputs from S3
        for input in config['inputs']:
            s3_get(input)

        # Launch the ASHLAR job with given parameters
        run_ashlar(config['arguments'])

        # Get ASHLAR version for writing results
        version = check_output(['ashlar', '--version'])

        # Create datestamp for writing results
        timestamp = datetime.now().isoformat()

        # Sync the output to S3
        s3_put(config['output'], version, timestamp)

    except Exception as e:
        print(e)
        return 1


if __name__ == "__main__":
    main()
