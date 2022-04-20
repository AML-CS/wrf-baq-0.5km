#!/usr/bin/env python3

import os
import glob
from pathlib import Path
from datetime import datetime, timedelta

import reporter


def clean_folder():
    gfs_files = glob.glob('./gfs-data/*')
    outdated = len(gfs_files) - 3
    if outdated > 0:
        os.system(f"rm -f {' '.join(gfs_files[:outdated])}")


if __name__ == '__main__':
    Path('gfs-data').mkdir(parents=True, exist_ok=True)
    clean_folder()
    os.chdir('./gfs-data')

    aws_bucket = os.environ.get('NOAA_AWS_BUCKET', None)
    gfs_start_date = os.environ.get('GFS_START_DATE', None)
    gfs_time_offset = int(os.environ.get('GFS_TIME_OFFSET', 0))
    wrf_interval_hours = int(os.environ.get('WRF_INTERVAL_HOURS', 0))
    gfs_interval_hours = int(os.environ.get('GFS_INTERVAL_HOURS', 0))

    start_date = datetime.strptime(gfs_start_date, '%Y-%m-%d %H')

    links = [(
        start_date,
        str(index).zfill(3)
    ) for index in range(gfs_time_offset, gfs_interval_hours + gfs_time_offset + 1, wrf_interval_hours)]

    filelist = [(
        'gfs.{0:%Y}{0:%m}{0:%d}/{0:%H}/atmos/gfs.t{0:%H}z.pgrb2.0p25.f{1}'.format(
            date,
            index
        ),
        'gfs_{0:%Y}{0:%m}{0:%d}_{0:%H}_00.pgrb2.0p25.t{1}z'.format(
            date + timedelta(hours=int(index)),
            index
        ),
        date
    ) for (date, index) in links]

    reporter.add({'gfsUrls': [obj[0] for obj in filelist]})

    for (key, filename, date) in filelist:
        file_base = os.path.basename(filename)

        if os.path.exists(file_base):
            print(f"{file_base} already exists")
            continue

        print('Downloading...', key)
        os.system(
            f"aws s3api get-object --no-sign-request --bucket {aws_bucket} --key {key} {filename}")

    print('Data saved in ./gfs-data')
