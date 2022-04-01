#!/usr/bin/env sh

wait_file() {
  local file="$1"; shift
  local wait_seconds="${1:-1800}"; shift # 30 minutes as default timeout
  until test $((wait_seconds--)) -eq 0 -o -e "$file" ; do sleep 1; done
  ((++wait_seconds))
}

export WORK_DIR='/work/syseng/users/sjdonado/workspace/wrf-baq-1km'
export AMLCS_DIR='/work/syseng/users/sjdonado/workspace/wrf-baq-1km/AML-CS.github.io'

cd $WORK_DIR

module load wrf/4.3-baq-1km miniconda

eval "$(conda shell.bash hook)"
conda activate wrf-baq-1km

rm -f ./output/report.json

echo "Setting up env variables..."
eval "$(./set_env_variables.py)"

echo "*** Debugging parameters ***"
echo "Created at: $CREATED_AT"
echo "Start date: $START_DATE"
echo "End date: $END_DATE"
echo "WRF interval hours: $WRF_INTERVAL_HOURS"
echo "GFS Start date: $GFS_START_DATE"
echo "GFS Time offset: $GFS_TIME_OFFSET"
echo "GFS interval hours: $GFS_INTERVAL_HOURS"
echo "NC variables: $NC_VARIABLES"
echo "BAQ station coordinates: $BAQ_STATION_COORDINATES"
echo "******"

./download_gfs_data.py
./fetch_ogimet_data.py
./ogimet_grib_interpolation.py

run-wps "$START_DATE" "$END_DATE" -i 3 --data-dir ./gfs-data

rm -f ./wrf_output
sbatch ./sbatch-run.sh

wait_file "./wrf_output" && {
  cat slurm.out.log

  echo "Generating gifs..."
  ./build_maps.py

  echo "Uploading to Github..."
  cp -R ./output/* $AMLCS_DIR/content/wrf-baq-1km/output

  cd $AMLCS_DIR

  git pull
  git add content/wrf-baq-1km/output/
  git commit -m "auto [$CREATED_AT]: update wrf-baq-1km output"
  git push
}

echo "Done!"
