#!/usr/bin/env python3

import os
import requests
from datetime import datetime, timedelta

import reporter

if __name__ == '__main__':
    interval_hours = 6
    gfs_interval_forecast = 3

    gfs_start_date = datetime.utcnow() - timedelta(hours=gfs_interval_forecast)

    gfs_time_offset = gfs_start_date.hour % interval_hours
    gfs_start_date -= timedelta(hours=gfs_time_offset)

    start_date = gfs_start_date
    end_date = start_date + timedelta(hours=interval_hours)

    DS_PATH = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'
    res = requests.get(
        '{1}gfs.{0:%Y}{0:%m}{0:%d}/{0:%H}/atmos'.format(
            gfs_start_date, DS_PATH)
    )
    if 'pgrb2.0p25' not in res.text:
        gfs_start_date -= timedelta(hours=interval_hours)
        gfs_time_offset += interval_hours
        interval_hours += interval_hours

    # GFS data cycle: 6h (each 6h it's available the next 24h forecast with 3h interval)
    GFS_START_DATE = gfs_start_date.strftime('%Y-%m-%d %H')
    GFS_TIME_OFFSET = gfs_time_offset - gfs_time_offset % 6
    GFS_INTERVAL_FORECAST = gfs_interval_forecast
    GFS_INTERVAL_HOURS = interval_hours

    START_DATE = start_date.strftime('%Y-%m-%d %H')
    END_DATE = end_date.strftime('%Y-%m-%d %H')

    WRF_OUTPUT = os.path.abspath('./wrf_output')

    NC_VARIABLES = "wind,temp,uwind,vwind,press"

    # 10° 53' N, 074° 47' W
    BAQ_STATION_COORDINATES = "10.883333,-74.783333"

    reporter.add({
        'createdAt': datetime.utcnow().strftime('%Y-%m-%d %H:%M'),
        'startDate': START_DATE,
        'endDate': END_DATE,
        'ncVariables': NC_VARIABLES.split(','),
        'baqStationCoordinates': BAQ_STATION_COORDINATES.split(',')
    }, logger=False)

    CURRENT_DIRECTORY = os.getcwd()

    print(f"""
		export START_DATE='{START_DATE}';
		export END_DATE='{END_DATE}';
		export WRF_OUTPUT='{WRF_OUTPUT}';
		export DS_PATH='{DS_PATH}';
		export GFS_START_DATE='{GFS_START_DATE}';
		export GFS_TIME_OFFSET='{GFS_TIME_OFFSET}';
		export GFS_INTERVAL_FORECAST='{GFS_INTERVAL_FORECAST}';
		export GFS_INTERVAL_HOURS='{GFS_INTERVAL_HOURS}';
		export NC_VARIABLES='{NC_VARIABLES}';
		export BAQ_STATION_COORDINATES='{BAQ_STATION_COORDINATES}';
		export CURRENT_DIRECTORY='{CURRENT_DIRECTORY}';
	""")
