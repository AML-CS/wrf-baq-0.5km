#!/usr/bin/env python3

import os
import requests
from datetime import datetime, timedelta

import reporter

if __name__ == '__main__':
    WRF_INTERVAL_HOURS = 3
    gfs_interval_hours = 6

    start_date = datetime.utcnow() - timedelta(hours=WRF_INTERVAL_HOURS)

    gfs_time_offset = start_date.hour % gfs_interval_hours
    gfs_start_date = start_date - timedelta(hours=gfs_time_offset)

    start_date_offset = start_date.hour % WRF_INTERVAL_HOURS
    start_date -= timedelta(hours=start_date_offset)

    end_date = start_date + timedelta(hours=gfs_interval_hours)

    DS_PATH = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'

    # res = requests.get(
    #     '{1}gfs.{0:%Y}{0:%m}{0:%d}/{0:%H}/atmos/gfs.t{0:%H}z.pgrb2.0p25.f000'.format(
    #         gfs_start_date, DS_PATH)
    # )
    # if res.status_code != 200 or 'gfs.t{0:%H}z.pgrb2.0p25.f000'.format(gfs_start_date) not in res.text:
    #     gfs_start_date -= timedelta(hours=gfs_interval_hours)
    #     gfs_time_offset += gfs_interval_hours
    #     gfs_interval_hours += gfs_interval_hours

    # GFS data cycle: 6h (each 6h it's available the next 24h forecast with 3h interval)
    GFS_START_DATE = gfs_start_date.strftime('%Y-%m-%d %H')
    GFS_TIME_OFFSET = gfs_time_offset - gfs_time_offset % 6
    GFS_INTERVAL_HOURS = gfs_interval_hours

    START_DATE = start_date.strftime('%Y-%m-%d %H')
    END_DATE = end_date.strftime('%Y-%m-%d %H')

    WRF_OUTPUT = os.path.abspath('./wrf_output')

    NC_VARIABLES = "pwater,temp,wind,uwind,vwind,press"

    # 10° 53' N, 074° 47' W
    BAQ_STATION_COORDINATES = "10.883333,-74.783333"

    CREATED_AT = datetime.utcnow().strftime('%Y-%m-%d %H:%M')

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
		export DS_PATH='{DS_PATH}';
		export GFS_START_DATE='{GFS_START_DATE}';
		export GFS_TIME_OFFSET='{GFS_TIME_OFFSET}';
		export GFS_INTERVAL_HOURS='{GFS_INTERVAL_HOURS}';
		export NC_VARIABLES='{NC_VARIABLES}';
		export BAQ_STATION_COORDINATES='{BAQ_STATION_COORDINATES}';
	""")
