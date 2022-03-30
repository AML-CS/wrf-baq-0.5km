#!/usr/bin/env sh

wait_file() {
  local file="$1"; shift
  local wait_seconds="${1:-1200}"; shift # 1200 seconds as default timeout
  until test $((wait_seconds--)) -eq 0 -o -e "$file" ; do sleep 1; done
  ((++wait_seconds))
}

module load wrf/4.3 miniconda

eval "$(conda shell.bash hook)"
conda activate wrf-baq-1km

rm -f ./report.json

echo "Setting up env variables..."
eval $(./set_env_variables.py)

# export NC_VARIABLES="wind,temp,uwind,vwind,press"
# export START_DATE="2022-03-29 06"

echo "*** Debugging parameters ***"
echo "Start date: $START_DATE"
echo "End date: $END_DATE"
echo "Interval hours: $INTERVAL_HOURS"
echo "GFS Start date: $GFS_START_DATE"
echo "GFS Time offset: $GFS_TIME_OFFSET"
echo "GFS interval forecast: $GFS_INTERVAL_FORECAST"
echo "NC variables: $NC_VARIABLES"
echo "BAQ station coordinates: $BAQ_STATION_COORDINATES"
echo "******"

./download_gfs_data.py
./fetch_ogimet_data.py
./ogimet_grib_interpolation.py

run-wps "$START_DATE" "$END_DATE" -i 3 --data-dir ./gfs-data

rm -f ./wrf_output
sbatch ./sbatch-run.sh

nc_variables=(${NC_VARIABLES//,/ })

wait_file "./wrf_output" && {
  cat slurm.out.log

  echo "Generating gifs..."
  ./generate_folium_gif.py

  echo "Uploading to aws..."
  for i in ${!nc_variables[@]}; do
    nc_var=${nc_variables[$i]}
    aws s3api put-object --bucket wrf-baq-1km --key "last/$nc_var.gif" --body "./gif-images/$nc_var.gif"
    aws s3api put-object-acl --bucket wrf-baq-1km --key "last/$nc_var.gif" --acl public-read
  done

  python -c 'import reporter; reporter.upload()'
}

echo "Done!"
