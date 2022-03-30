#!/usr/bin/env python3

import os
import re
import imageio
import json
from pathlib import Path
from datetime import datetime, timedelta

import geojsoncontour
import numpy as np
import pandas as pd

from netCDF4 import Dataset as NetCDFFile
import matplotlib.pyplot as plt

from wrf import getvar, interplevel, to_np, latlon_coords

import plotly.graph_objects as go

nc_file = NetCDFFile('./wrf_output')
time_size = nc_file.dimensions['Time'].size


def get_data(nc_file: NetCDFFile, timeidx: int):
    dx = 150
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

    data = {
        'wind': ('Wind speed (m/s)', np.sqrt(u ** 2 + v ** 2)),
        'temp': ('Temperature (C)', T),
        'uwind': ('U wind speed (m/s)', u),
        'vwind': ('V wind speed (m/s)', v),
        'press': ('Pressure (hPa)', P)
    }

    return data


def geojson_title_to_float(title):
    result = re.search(
        r"([-]?([0-9]*[.])?[0-9]+)-([-]?([0-9]*[.])?[0-9]+)", title)
    groups = result.groups()

    value = np.median([float(groups[0]), float(groups[2])])

    return value


def gj_to_df(gj):
    gj_data = np.zeros([len(gj['features']), 2])

    for i in range(len(gj['features'])):
        gj['features'][i]['id'] = i
        gj_data[i, 0] = i
        gj_data[i, 1] = geojson_title_to_float(
            gj['features'][i]['properties']['title'])

    df = pd.DataFrame(gj_data, columns=['id', 'variable'])

    return df


def build_fig(lats, lons, caption, variable, date):
    contour = plt.contourf(lons, lats, variable, cmap=plt.cm.jet)

    gj = json.loads(geojsoncontour.contourf_to_geojson(
        contourf=contour, ndigits=4, unit='m'))
    df_contour = gj_to_df(gj)

    zmin = df_contour.variable.min() - df_contour.variable.median() / 10
    zmax = df_contour.variable.max() + df_contour.variable.median() / 10

    trace = go.Choroplethmapbox(
        geojson=gj,
        locations=df_contour.id,
        z=df_contour.variable,
        zmin=zmin,
        zmax=zmax,
        colorscale='jet',
        marker_line_width=0.1,
        marker=dict(opacity=0.2)
    )

    layout = go.Layout(
        title=f"{caption} - {date} GMT-5",
        title_x=0.5,
        width=600,
        margin=dict(t=26, b=0, l=0, r=0),
        font=dict(color='black', size=10),
        mapbox=dict(
            center=dict(
                lat=lats.mean().item(0),
                lon=lons.mean().item(0)
            ),
            zoom=11,
            style='carto-positron'
        )
    )

    fig = go.Figure(data=[trace], layout=layout)

    return fig


def get_image(timeidx: int, nc_var: str, start_date: datetime):
    date = start_date + timedelta(hours=timeidx * 3) - timedelta(hours=5)

    data = get_data(nc_file, timeidx)

    (caption, variable) = data[nc_var]
    (lats, lons) = latlon_coords(variable)

    fig = build_fig(lats, lons, caption, variable, date)

    png_file = f"{nc_var}_{timeidx}.png"
    try:
        fig.write_image(png_file)
    except Exception:
        return None

    img = imageio.imread(png_file)
    os.remove(png_file)

    return img


if __name__ == '__main__':
    Path('gif-images').mkdir(parents=True, exist_ok=True)
    os.chdir('./gif-images')

    start_date = datetime.strptime(
        os.environ.get('START_DATE', None), '%Y-%m-%d %H')
    nc_variables = os.environ.get('NC_VARIABLES', None).split(',')

    for nc_var in nc_variables:
        print(nc_var)
        results = [get_image(timeidx, nc_var, start_date)
                   for timeidx in range(time_size)]
        imageio.mimwrite(f"{nc_var}.gif", [
                         img for img in results if img is not None], fps=0.5)

    print("Data saved in ./gif-images")
