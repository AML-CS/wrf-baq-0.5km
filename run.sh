#!/usr/bin/env bash

wait_file() {
  local file="$1"; shift
  local wait_seconds="${1:-700}"; shift # 700 seconds as default timeout

  until test $((wait_seconds--)) -eq 0 -o -e "$file" ; do sleep 1; done

  ((++wait_seconds))
}

module load wrf/4.3 miniconda

eval $(./set_env_variables.py)

echo $START_DATE
echo $END_DATE
echo $GFS_START_DATE
echo $GFS_TIME_OFFSET

./download_gfs_data.py

run-wps "$START_DATE" "$END_DATE" -i 3 -g 1000 --data-dir ./gfs-data

sbatch ./sbatch-run.sh

eval "$(conda shell.bash hook)"
conda activate wrf-baq-1km

wait_file "./wrf_output" && {
	./generate_folium_gif.py "wind"
	./generate_folium_gif.py "temp"
}
