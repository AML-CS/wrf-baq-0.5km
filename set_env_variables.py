#!/usr/bin/env python3

import os
import requests
from datetime import datetime, timedelta

if __name__ == '__main__':
	now = datetime.utcnow()

	gfs_time_offset = now.hour % 6
	gfs_start_date = datetime(now.year, now.month, now.day, now.hour - gfs_time_offset)

	DS_PATH = 'https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod/'

	req = requests.get(
		'{2}gfs.{0:%Y}{0:%m}{0:%d}/{0:%H}/atmos'.format(
			gfs_start_date,
			DS_PATH
		),
		stream=True
	)

	if req.status_code != 200:
		gfs_start_date -= timedelta(hours=6)
		gfs_time_offset += 6

	start_date = datetime(now.year, now.month, now.day, now.hour - now.hour % 6)
	end_date = start_date + timedelta(hours=9)

	GFS_START_DATE = gfs_start_date.strftime('%Y-%m-%d %H')
	GFS_TIME_OFFSET = gfs_time_offset - gfs_time_offset % 6

	START_DATE = start_date.strftime('%Y-%m-%d %H')
	END_DATE = end_date.strftime('%Y-%m-%d %H')

	WRF_OUTPUT = os.path.abspath('./wrf_output')

	NC_VARIABLES = "wind,temp,u_wind,v_wind,pressure"

	print(f"""
		export START_DATE='{START_DATE}';
		export END_DATE='{END_DATE}';
		export WRF_OUTPUT='{WRF_OUTPUT}';
		export DS_PATH='{DS_PATH}';
		export GFS_START_DATE='{GFS_START_DATE}';
		export GFS_TIME_OFFSET='{GFS_TIME_OFFSET}';
		export NC_VARIABLES='{NC_VARIABLES}';
	""")
