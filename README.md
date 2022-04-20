# WRF BAQ 0.5km, an Internet weather forecasting system based on WRF simulations with GFS + OGIMET observations running on an HPC cluster.
> ![arch-diagram](WRF-BAQ-0.5km.png)

## Data

- Granado folder location `/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km`
- BAQ Geojson Polygon `/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/Limite Distrito de Barranquilla.geojson`
- Notebooks `/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/notebooks`
- Last WRF output `/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/output`
- Last NOAA - GFS data `/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/gfs-data`
- Last OGIMET data `/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/ogimet-data`
- Last GRIB data (interpolated files) `/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/grib-data`
- All Cron logs `/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/cron-logs`


## How to run

- Cronjob
```bash
0 */3 * * * /work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/launch-cron.tcsh >> "/work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/cron-logs/cron_$(date "+\%Y\%m\%d\%H\%M").log" 2>&1
```
- Manually
```bash
cd /work/syseng/users/sjdonado/workspace/wrf-baq-0.5km
./run.sh
```
