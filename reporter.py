#!/usr/bin/env python3

import os
import json

dir = os.environ.get('WORK_DIR', './')
REPORT_FILENAME = f"{dir}/output/report.json"

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
