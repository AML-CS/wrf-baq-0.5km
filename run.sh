#!/usr/bin/env sh

wait_file() {
  local file="$1"; shift
  local wait_seconds="${1:-700}"; shift # 700 seconds as default timeout
  until test $((wait_seconds--)) -eq 0 -o -e "$file" ; do sleep 1; done
  ((++wait_seconds))
}

module load wrf/4.3 miniconda

echo "Setting up env variables..."
eval $(./set_env_variables.py)

echo "*** Debugging parameters ***"
echo "Start date: $START_DATE"
echo "End date: $END_DATE"
echo "GFS Start date: $GFS_START_DATE"
echo "GFS Time offset: $GFS_TIME_OFFSET"
echo "NC variables: $NC_VARIABLES"
echo "******"

./download_gfs_data.py

run-wps "$START_DATE" "$END_DATE" -i 3 -g 1000 --data-dir ./gfs-data

rm -f ./wrf_output
sbatch ./sbatch-run.sh

eval "$(conda shell.bash hook)"
conda activate wrf-baq-1km

# nc_variables=(${NC_VARIABLES//,/ })

# wait_file "./wrf_output" && {
#   cat slurm.out.log

#   echo "Generate folium gif..."
#   ./generate_folium_gif.py

#   for i in ${!nc_variables[@]}; do
#     nc_var=${nc_variables[$i]}
#     aws s3api put-object --bucket wrf-baq-1km --key "$nc_var.gif" --body "./gif-images/$nc_var.gif"
#     aws s3api put-object-acl --bucket wrf-baq-1km --key "$nc_var.gif" --acl public-read
#   done
# }

echo "Done!"