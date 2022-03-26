#!/usr/bin/env python3

import os
import sys
import time
import imageio
import json
import glob
from datetime import datetime, timedelta

import folium
import geojsoncontour
import numpy as np

from folium import plugins
from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt

import branca.colormap as cm
from matplotlib import colors as mcolors
from wrf import getvar, interplevel, to_np, latlon_coords

from PIL import Image
from pathlib import Path

import selenium.webdriver
from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True

driver = selenium.webdriver.Firefox(executable_path='/usr/bin/geckodriver', options=options)

start_date = datetime.strptime(os.environ.get('START_DATE', None), '%Y-%m-%d %H')
var_key = sys.argv[1]

nc = NetCDFFile('./wrf_output')
time_size = nc.dimensions['Time'].size

def get_data(nc_file: NetCDFFile, timeidx:int, dx: int):
    height = getvar(nc_file, 'height', timeidx=timeidx)
    u_all = getvar(nc_file, 'ua', timeidx=timeidx)
    v_all = getvar(nc_file, 'va', timeidx=timeidx)
    w_all = getvar(nc_file, 'wa', timeidx=timeidx)
    T_all = getvar(nc_file, 'tc', timeidx=timeidx)
    P_all = getvar(nc_file, 'pressure', timeidx=timeidx)

    P = interplevel(P_all, height, dx)
    T = interplevel(T_all, height, dx)
    u = interplevel(u_all, height, dx)
    v = interplevel(v_all, height, dx)
    w = interplevel(w_all, height, dx)

    return (T, u, v, np.sqrt(u ** 2 + v ** 2 + w ** 2), P)


def get_folium(nc_file: NetCDFFile, timeidx: int, var_key: str):
    (T, U, V, mag, P) = get_data(nc_file, timeidx, dx=1000)
    (lats, lons) = latlon_coords(mag)

    figure = plt.figure()
    ax = figure.add_subplot(111)

    variables = {
        'wind': ('Wind velocity in m/s', mag),
        'temp': ('Tempeture in celsius', T),
        'u_wind': ('U_Wind Velocity in m/s', U),
        'v_wind': ('V_Wind Velocity in m/s', V),
        'pressure': ('Pressure in hPa', P)
    }

    (caption, variable) = variables[var_key]

    contour = ax.contourf(lons, lats, variable, cmap=plt.cm.jet)
    cbar = figure.colorbar(contour)

    gj = json.loads(geojsoncontour.contourf_to_geojson(contourf=contour, ndigits=3, unit='m'))

    folium_map = folium.Map(
        location=[lats.mean() - 0.08, lons.mean()],
        tiles='Cartodb Positron',
        zoom_start=10,
        zoom_control=False,
        scrollWheelZoom=False,
        dragging=False
    )

    folium.GeoJson(
        gj,
        style_function=lambda x: {
            'color': x['properties']['stroke'],
            'weight': x['properties']['stroke-width'],
            'fillColor': x['properties']['fill'],
            'opacity': 0.4,
        },
        name='geojson'
    ).add_to(folium_map)

    colormap = cm.LinearColormap(
        colors=['darkblue', 'blue', 'cyan', 'green', 'greenyellow', 'yellow', 'orange', 'red', 'darkred'],
        index=np.array(cbar.values), vmin=cbar.values[0],
        vmax=cbar.values[len(cbar.values) - 1],
        caption=caption
    )

    folium_map.add_child(colormap)

    date = start_date + timedelta(hours=timeidx * 3) - timedelta(hours=5)
    folium_map.get_root().html.add_child(folium.Element('<span style="position:fixed;z-index:999;font-size:12px;margin:4px">{}</span>'.format(date)))

    return (folium_map, figure)


def get_image(timeidx: int, var_key: str):
    (f_map, fig) = get_folium(nc, timeidx, var_key)

    html_file = f"{var_key}_{timeidx}.html"
    png_file = f"{var_key}_{timeidx}.png"

    f_map.save(html_file)

    driver.set_window_size(600, 600)
    driver.get(f"file://{os.getcwd()}/{html_file}")

    time.sleep(2)
    driver.save_screenshot(png_file)

    img = imageio.imread(png_file)

    os.remove(html_file)
    os.remove(png_file)

    return img

if __name__ == '__main__':
    results = [get_image(timeidx, var_key) for timeidx in range(time_size)]

    imageio.mimwrite(f"{var_key}_{datetime.now()}.gif", results, fps=1)
