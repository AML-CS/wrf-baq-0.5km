#!/usr/bin/env python3

import os
import json
import subprocess

dir = os.environ.get('CURRENT_DIRECTORY', './')
REPORT_FILENAME = f"{dir}/report.json"

def read_file():
    if os.path.exists(REPORT_FILENAME):
        with open(REPORT_FILENAME, 'r') as f:
            data = json.load(f)
        return data

    data = {}
    update_file(data)
    return data


def update_file(data):
    with open(REPORT_FILENAME, 'w+') as f:
        json.dump(data, f)


def add(new_data: dict, logger=True):
    if logger:
        print('LOGGER:', new_data)

    data = read_file()
    update_file(data | new_data)


def upload():
    subprocess.run(['aws', 's3api', 'put-object', '--bucket=wrf-baq-1km',
                   f"--key=last/report.json", f"--body={REPORT_FILENAME}"])
    subprocess.run(['aws', 's3api', 'put-object-acl', '--bucket=wrf-baq-1km',
                   f"--key=last/report.json", '--acl', 'public-read'])
