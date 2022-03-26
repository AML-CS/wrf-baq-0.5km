#!/usr/bin/env python3

import os
import sys
import requests
import time
from pathlib import Path
from datetime import datetime, timedelta

def check_file_status(filepath, filesize):
    sys.stdout.write('\r')
    sys.stdout.flush()
    size = int(os.stat(filepath).st_size)
    percent_complete = (size/filesize)*100
    sys.stdout.write('%.3f %s' % (percent_complete, '% Completed'))
    sys.stdout.flush()

def parsed_hour(date):
    return str(date.hour).zfill(2)

if __name__ == '__main__':
    Path('gfs-data').mkdir(parents=True, exist_ok=True)
    os.system('rm -f ./gfs-data/*')

    dspath = os.environ.get('DS_PATH', None)
    gfs_start_date = os.environ.get('GFS_START_DATE', None)
    time_offset = int(os.environ.get('GFS_TIME_OFFSET', 0))

    date = datetime.strptime(gfs_start_date, '%Y-%m-%d %H')

    links =  [(date, str(index).zfill(3)) for index in range(time_offset, time_offset + 10, 3)]
    filelist = [('gfs.{0:%Y}{0:%m}{0:%d}/{1}/atmos/gfs.t{1}z.pgrb2full.0p50.f{2}'.format(date, parsed_hour(date), index), date) for (date, index) in links]

    for (file, date) in filelist:
        filename=dspath+file
        file_base = os.path.basename(file)
        print('Downloading', filename)
        req = requests.get(filename, stream=True)
        filesize = int(req.headers['Content-length'])
        with open(file_base, 'wb') as outfile:
            chunk_size=1048576
            for chunk in req.iter_content(chunk_size=chunk_size):
                outfile.write(chunk)
                if chunk_size < filesize:
                    check_file_status(file_base, filesize)
        check_file_status(file_base, filesize)

    os.system("mv gfs.* ./gfs-data")

    print('Data saved in ./gfs-data')
