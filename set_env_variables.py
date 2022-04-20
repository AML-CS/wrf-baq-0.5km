#!/usr/bin/env python3

import os
from datetime import datetime, timedelta

import reporter

if __name__ == '__main__':
    NOAA_AWS_BUCKET = 'noaa-gfs-bdp-pds'
    NC_VARIABLES = "pwater,temp,wind,uwind,vwind,press"
    # 10° 53' N, 074° 47' W
    BAQ_STATION_COORDINATES = "10.883333,-74.783333"

    WRF_INTERVAL_HOURS = 3
    gfs_interval_hours = 6

    utcnow = datetime.utcnow()

    start_date = utcnow - timedelta(hours=WRF_INTERVAL_HOURS)

    gfs_time_offset = start_date.hour % gfs_interval_hours
    gfs_start_date = start_date - timedelta(hours=gfs_time_offset)

    start_date_offset = start_date.hour % WRF_INTERVAL_HOURS
    start_date -= timedelta(hours=start_date_offset)

    end_date = start_date + timedelta(hours=gfs_interval_hours)

    OGIMET_START_DATE = start_date.strftime('%Y-%m-%d %H')
    OGIMET_END_DATE = end_date.strftime('%Y-%m-%d %H')

    next_window_offset = utcnow.hour % WRF_INTERVAL_HOURS
    if next_window_offset == 2:
        end_date += timedelta(hours=WRF_INTERVAL_HOURS)
        gfs_interval_hours += WRF_INTERVAL_HOURS

    key = 's3://{1}/gfs.{0:%Y}{0:%m}{0:%d}/{0:%H}/atmos/gfs.t{0:%H}z.pgrb2.0p25.f000'.format(
        gfs_start_date, NOAA_AWS_BUCKET)
    exit_code = os.system(f"aws s3 ls --no-sign-request {key}")
    if exit_code != 0:
        gfs_start_date -= timedelta(hours=gfs_interval_hours)
        gfs_time_offset += gfs_interval_hours
        gfs_interval_hours += gfs_interval_hours

    GFS_START_DATE = gfs_start_date.strftime('%Y-%m-%d %H')
    GFS_TIME_OFFSET = gfs_time_offset - gfs_time_offset % 3
    GFS_INTERVAL_HOURS = gfs_interval_hours

    START_DATE = start_date.strftime('%Y-%m-%d %H')
    END_DATE = end_date.strftime('%Y-%m-%d %H')

    CREATED_AT = utcnow.strftime('%Y-%m-%d %H:%M')

    WRF_OUTPUT = os.path.abspath('./wrf_output')

    reporter.add({
        'createdAt': CREATED_AT,
        'startDate': START_DATE,
        'endDate': END_DATE,
        'ncVariables': NC_VARIABLES.split(','),
        'ogimetStationCoordinates': BAQ_STATION_COORDINATES.split(',')
    }, logger=False)

    print(f"""
		export CREATED_AT='{CREATED_AT}';
		export START_DATE='{START_DATE}';
		export END_DATE='{END_DATE}';
		export WRF_INTERVAL_HOURS='{WRF_INTERVAL_HOURS}';
		export WRF_OUTPUT='{WRF_OUTPUT}';
		export NOAA_AWS_BUCKET='{NOAA_AWS_BUCKET}';
		export GFS_START_DATE='{GFS_START_DATE}';
		export GFS_TIME_OFFSET='{GFS_TIME_OFFSET}';
		export GFS_INTERVAL_HOURS='{GFS_INTERVAL_HOURS}';
		export OGIMET_START_DATE='{OGIMET_START_DATE}';
		export OGIMET_END_DATE='{OGIMET_END_DATE}';
		export NC_VARIABLES='{NC_VARIABLES}';
		export BAQ_STATION_COORDINATES='{BAQ_STATION_COORDINATES}';
	""")
