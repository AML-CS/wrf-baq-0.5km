#!/usr/bin/env python3

import os
import re
import time
from pathlib import Path
from datetime import datetime

import pandas as pd
import numpy as np

from urllib.request import urlopen
from bs4 import BeautifulSoup

from metar import Metar
from metpy.units import units
from metpy.calc import wind_components

import reporter


def fetch(url):
    try:
        html = urlopen(url).read()
        soup = BeautifulSoup(html, features='html.parser')
        for script in soup(["script", "style"]):
            script.extract()
        return soup
    except Exception as e:
        print(e)
        return None


def fetch_metar_by_icao_and_date(icao, start_date, end_date):
    url = f"https://www.ogimet.com/display_metars2.php?lang=en&lugar={icao}&tipo=SA&ord=DIR&nil=NO&fmt=txt"

    url += '&ano={0:%Y}&mes={0:%m}&day={0:%d}&hora={0:%H}&min=00'.format(
        start_date)
    url += '&anof={0:%Y}&mesf={0:%m}&dayf={0:%d}&horaf={0:%H}&minf=59'.format(
        end_date)

    reporter.add({'ogimetUrl': url})

    print(f"Fetching... {url}", flush=True)
    soup = fetch(url)
    data = []
    if soup is None:
        return data
    text = soup.get_text()
    if f"No hay METAR/SPECI de {icao} en el periodo solicitado" in text:
        return data

    text = re.sub('\s\s+', ' ', text)
    matches = re.findall(r"\s(\d+)[\s]METAR\s(.*)=", text)
    for match in matches:
        if ',' not in match:
            data.append({'datetime': datetime.strptime(
                match[0], '%Y%m%d%H%M'), 'metar': match[1]})

    return data


def parse_wind_components(obs):
    u, v = wind_components(obs.wind_speed.value() *
                           units('knots'), obs.wind_dir.value() * units.degree)

    return (u.to(units('m/s')).magnitude, v.to(units('m/s')).magnitude)


def get_variables(metar):
    try:
        obs = Metar.Metar(metar)

        temp = obs.temp.value(units='K')
        (uwind, vwind) = parse_wind_components(obs)
        press = obs.press.value(units='HPA')

        return [temp, uwind, vwind, press]
    except Exception as e:
        return None


def save_hdf(date, station_coords, variables):
    df = pd.DataFrame(data=[station_coords + variables.tolist()],
                      columns=['lat', 'long', 'temp', 'uwind', 'vwind', 'press'])

    filename = 'metar_{0:%Y}{0:%m}{0:%d}_{0:%H}_00.h5'.format(date)
    df.to_hdf(filename, key='df')
    print(f"{filename} saved")


if __name__ == '__main__':
    station_icao = 'SKBQ'
    (station_lat, station_lon) = os.environ.get(
        'BAQ_STATION_COORDINATES', None).split(',')
    station_coords = [float(station_lat), float(station_lon)]

    gfs_interval_forecast = gfs_interval_forecast = int(
        os.environ.get('GFS_INTERVAL_FORECAST', 0))
    start_date = datetime.strptime(
        os.environ.get('START_DATE', None), '%Y-%m-%d %H')
    end_date = datetime.strptime(
        os.environ.get('END_DATE', None), '%Y-%m-%d %H')

    Path('ogimet-data').mkdir(parents=True, exist_ok=True)
    os.system('rm -f ./ogimet-data/*.h5')
    os.chdir('./ogimet-data')

    rows = fetch_metar_by_icao_and_date(station_icao, start_date, end_date)

    vars_acum = []
    for row in rows:
        date = row['datetime']
        variables = get_variables(row['metar'])

        if variables is None:
            continue

        vars_acum.append(variables)

        if date.hour % gfs_interval_forecast == 0:
            save_hdf(date, station_coords, np.median(vars_acum, axis=0))
            vars_acum = []

    print("Data saved in ./ogimet-data")
