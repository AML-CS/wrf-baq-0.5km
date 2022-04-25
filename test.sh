#!/usr/bin/env sh

WORK_DIR='/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km'
cd $WORK_DIR

module load wrf/4.3-baq-0.5km miniconda

eval "$(conda shell.bash hook)"
conda activate wrf-baq-0.5km

echo "Setting up env variables..."
eval $(./set_env_variables.py)

echo "*** Debugging parameters ***"
echo "Created at: $CREATED_AT"
echo "Start date: $START_DATE"
echo "End date: $END_DATE"
echo "WRF interval hours: $WRF_INTERVAL_HOURS"
echo "WRF output: $WRF_OUTPUT"
echo "NOAA AWS Bucket: $NOAA_AWS_BUCKET"
echo "GFS Start date: $GFS_START_DATE"
echo "GFS Time offset: $GFS_TIME_OFFSET"
echo "GFS interval hours: $GFS_INTERVAL_HOURS"
echo "Ogimet Start Date: $OGIMET_START_DATE"
echo "Ogimet End Date: $OGIMET_END_DATE"
echo "NC variables: $NC_VARIABLES"
echo "BAQ station coordinates: $BAQ_STATION_COORDINATES"
echo "******"
