# WRF BAQ 0.5km Forecast
> A web weather forecasting system based on GFS - NOAA data interpolated with METAR reports running every 3h on the Granado HPC cluster.

![arch-diagram](WRF-BAQ-0.5km.png)

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

## Output

```bash
Setting up env variables...
*** Debugging parameters ***
Created at: 2022-05-07 05:00
Start date: 2022-05-07 00
End date: 2022-05-07 09
WRF interval hours: 3
WRF output: /work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/wrf_output
NOAA AWS Bucket: noaa-gfs-bdp-pds
GFS Start date: 2022-05-07 00
GFS Time offset: 0
GFS interval hours: 9
Ogimet Start Date: 2022-05-07 00
Ogimet End Date: 2022-05-07 06
NC variables: pwater,temp,wind,uwind,vwind,press
BAQ station coordinates: 10.883333,-74.783333
******
{
    "AcceptRanges": "bytes",
    "LastModified": "Sat, 07 May 2022 03:36:30 GMT",
    "ContentLength": 509235124,
    "ETag": "\"3ebc35a347b251cebb92c8145604db82\"",
    "ContentType": "binary/octet-stream",
    "Metadata": {}
}
{
    "AcceptRanges": "bytes",
    "LastModified": "Sat, 07 May 2022 03:38:18 GMT",
    "ContentLength": 545133773,
    "ETag": "\"176adcc8f35959e13c0298ae44c2bc41\"",
    "ContentType": "binary/octet-stream",
    "Metadata": {}
}
{
    "AcceptRanges": "bytes",
    "LastModified": "Sat, 07 May 2022 03:40:13 GMT",
    "ContentLength": 548240765,
    "ETag": "\"0b1acc85b5826636a6c4495c49f4e2e8\"",
    "ContentType": "binary/octet-stream",
    "Metadata": {}
}
{
    "AcceptRanges": "bytes",
    "LastModified": "Sat, 07 May 2022 03:40:04 GMT",
    "ContentLength": 549193441,
    "ETag": "\"742327fd0cbf77227ed6e3180e5544db\"",
    "ContentType": "binary/octet-stream",
    "Metadata": {}
}
LOGGER: {'gfsUrls': ['gfs.20220507/00/atmos/gfs.t00z.pgrb2.0p25.f000', 'gfs.20220507/00/atmos/gfs.t00z.pgrb2.0p25.f003', 'gfs.20220507/00/atmos/gfs.t00z.pgrb2.0p25.f006', 'gfs.20220507/00/atmos/gfs.t00z.pgrb2.0p25.f009']}
Downloading... gfs.20220507/00/atmos/gfs.t00z.pgrb2.0p25.f000
Downloading... gfs.20220507/00/atmos/gfs.t00z.pgrb2.0p25.f003
Downloading... gfs.20220507/00/atmos/gfs.t00z.pgrb2.0p25.f006
Downloading... gfs.20220507/00/atmos/gfs.t00z.pgrb2.0p25.f009
Data saved in ./gfs-data
LOGGER: {'ogimetUrl': 'https://www.ogimet.com/display_metars2.php?lang=en&lugar=SKBQ&tipo=SA&ord=DIR&nil=NO&fmt=txt&ano=2022&mes=05&day=07&hora=00&min=00&anof=2022&mesf=05&dayf=07&horaf=06&minf=59'}
Fetching... https://www.ogimet.com/display_metars2.php?lang=en&lugar=SKBQ&tipo=SA&ord=DIR&nil=NO&fmt=txt&ano=2022&mes=05&day=07&hora=00&min=00&anof=2022&mesf=05&dayf=07&horaf=06&minf=59
metar_20220507_00_00.h5 saved
metar_20220507_03_00.h5 saved
Data saved in ./ogimet-data
Interpolate ./gfs-data/gfs_20220507_00_00.pgrb2.0p25.t000z, based on ./ogimet-data/metar_20220507_00_00.h5
LOGGER: {'interpolatedVariables': ['563:Temperature:K (instant):regular_ll:surface:level 0:fcst time 0 hrs:from 202205070000', '548:U component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 100000 Pa:fcst time 0 hrs:from 202205070000', '549:V component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 100000 Pa:fcst time 0 hrs:from 202205070000', '561:Surface pressure:Pa (instant):regular_ll:surface:level 0:fcst time 0 hrs:from 202205070000']}
./gfs-data/gfs_20220507_00_00.pgrb2.0p25.t000z saved in ./gfs-data
Interpolate ./gfs-data/gfs_20220507_03_00.pgrb2.0p25.t003z, based on ./ogimet-data/metar_20220507_03_00.h5
LOGGER: {'interpolatedVariables': ['563:Temperature:K (instant):regular_ll:surface:level 0:fcst time 3 hrs:from 202205070000', '548:U component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 100000 Pa:fcst time 3 hrs:from 202205070000', '549:V component of wind:m s**-1 (instant):regular_ll:isobaricInhPa:level 100000 Pa:fcst time 3 hrs:from 202205070000', '561:Surface pressure:Pa (instant):regular_ll:surface:level 0:fcst time 3 hrs:from 202205070000']}
./gfs-data/gfs_20220507_03_00.pgrb2.0p25.t003z saved in ./gfs-data
Running geogrid...
Success complete
Running ungrib...
Using /work/syseng/users/sjdonado/workspace/wrf-baq-0.5km/gfs-data
Success complete
Running metgrid...
Success complete
149.382 seconds
Submitted batch job 468103
Running real.exe...
Success complete
2.625 seconds
Running wrf.exe...
Success complete
869.927 seconds
Generating gifs...
pwater
temp
wind
uwind
vwind
press
Data saved in ./output
Uploading to Github...
Already up to date.
[master 1a1d9eb] auto [2022-05-07 05:00]: BAQ 0.5km WRF output
 12 files changed, 2122 insertions(+), 2120 deletions(-)
 rewrite output/press.gif (93%)
 rewrite output/press.html (60%)
 rewrite output/pwater.gif (95%)
 rewrite output/report.json (76%)
 rewrite output/temp.gif (95%)
 rewrite output/uwind.gif (94%)
 rewrite output/vwind.gif (94%)
 rename output/{pwater.html => vwind.html} (54%)
 rewrite output/wind.gif (94%)
warning: current Git remote contains credentials
To https://github.com/AML-CS/wrf-baq-0.5km.git
   2e84c5d..1a1d9eb  master -> master
Done!
```

## Docs

- [WRF + WRFDA Granado HPC](https://aml-cs.github.io/posts/wrf-wrfda-syseng-unhpc/)
- [Thesis report](https://slides.com/sjdonado/wrf-baq-05km)
