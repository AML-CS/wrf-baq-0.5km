## Cronjob

```bash
MAILTO="sjdonado@uninorte.edu.co"
0 */3 * * * sjdonado /work/syseng/users/sjdonado/workspace/wrf-baq-1km/run.sh >> "/work/syseng/users/sjdonado/workspace/wrf-baq-1km/cron_$(date '+%Y-%m-%d_%H:%M:%S').log" 2>&1
```

## Granado folder location

`/work/syseng/users/sjdonado/workspace/wrf-baq-1km`
