## Cronjob

```bash
# * * * * * echo "test" >> "/work/syseng/users/sjdonado/workspace/wrf-baq-1km/cron_test_$(date "+\%Y\%m\%d\%H\%M").log" 2>&1
# */5  * * * * /work/syseng/users/sjdonado/workspace/wrf-baq-1km/launch-cron.tcsh >> "/work/syseng/users/sjdonado/workspace/wrf-baq-1km/cron_$(date "+\%Y\%m\%d\%H\%M").log" 2>&1
0 */3 * * * /work/syseng/users/sjdonado/workspace/wrf-baq-1km/launch-cron.tcsh >> "/work/syseng/users/sjdonado/workspace/wrf-baq-1km/cron_$(date "+\%Y\%m\%d\%H\%M").log" 2>&1
```

## Granado folder location

`/work/syseng/users/sjdonado/workspace/wrf-baq-1km`
