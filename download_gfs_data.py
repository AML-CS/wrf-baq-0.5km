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

if __name__ == '__main__':
    Path('gfs-data').mkdir(parents=True, exist_ok=True)
    os.chdir('./gfs-data')

    dspath = os.environ.get('DS_PATH', None)
    gfs_start_date = os.environ.get('GFS_START_DATE', None)
    gfs_time_offset = int(os.environ.get('GFS_TIME_OFFSET', 0))
    gfs_interval_forecast = int(os.environ.get('GFS_INTERVAL_FORECAST', 0))
    gfs_interval_hours = int(os.environ.get('GFS_INTERVAL_HOURS', 0))

    start_date = datetime.strptime(gfs_start_date, '%Y-%m-%d %H')

    links =  [(
        start_date,
        str(index).zfill(3)
    ) for index in range(gfs_time_offset, gfs_interval_hours + 1, gfs_interval_forecast)]

    filelist = [(
        '{0}gfs.{1:%Y}{1:%m}{1:%d}/{1:%H}/atmos/gfs.t{1:%H}z.pgrb2.0p25.f{2}'.format(
            dspath,
            date,
            index
        ),
        'gfs_{0:%Y}{0:%m}{0:%d}_{0:%H}_00.pgrb2.0p25'.format(date + timedelta(hours=int(index))),
        date
    ) for (date, index) in links]

    for (file_url, filename, date) in filelist:
        file_base = os.path.basename(filename)

        if os.path.exists(file_base):
            print(f"{file_base} already exists")
            continue

        print('\nDownloading', file_url)
        req = requests.get(file_url, stream=True)
        filesize = int(req.headers['Content-length'])
        with open(file_base, 'wb') as outfile:
            chunk_size=1048576
            for chunk in req.iter_content(chunk_size=chunk_size):
                outfile.write(chunk)
                if chunk_size < filesize:
                    check_file_status(file_base, filesize)
        check_file_status(file_base, filesize)

    print('\nData saved in ./gfs-data')
