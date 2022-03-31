#!/usr/bin/env sh

WORK_DIR='/work/syseng/users/sjdonado/workspace/wrf-baq-1km'
cd $WORK_DIR

module load wrf/4.3 miniconda

eval "$(conda shell.bash hook)"
conda activate wrf-baq-1km

echo "Setting up env variables..."
eval $(./set_env_variables.py)

echo "*** Debugging parameters ***"
echo "Start date: $START_DATE"
echo "End date: $END_DATE"
echo "WRF interval hours: $WRF_INTERVAL_HOURS"
echo "GFS Start date: $GFS_START_DATE"
echo "GFS Time offset: $GFS_TIME_OFFSET"
echo "GFS interval hours: $GFS_INTERVAL_HOURS"
echo "NC variables: $NC_VARIABLES"
echo "BAQ station coordinates: $BAQ_STATION_COORDINATES"
echo "******"

run-wps --help
