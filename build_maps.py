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

import wrf
from netCDF4 import Dataset as NetCDFFile

import folium
import plotly.graph_objects as go

import matplotlib.pyplot as plt
import branca.colormap as cm

from shapely.geometry import shape, Point

nc_file = NetCDFFile('./wrf_output')
time_size = nc_file.dimensions['Time'].size

with open('./Limite Distrito de Barranquilla.geojson') as f:
    baq_geojson = json.load(f)
    baq_polygon = shape(baq_geojson['features'][0]['geometry'])


def get_data(nc_file: NetCDFFile, timeidx: int):
    desiredlev = 150
    height = wrf.getvar(nc_file, 'height', timeidx=timeidx)

    u_all = wrf.getvar(nc_file, 'ua', timeidx=timeidx)
    v_all = wrf.getvar(nc_file, 'va', timeidx=timeidx)
    T_all = wrf.getvar(nc_file, 'tc', timeidx=timeidx)
    P_all = wrf.getvar(nc_file, 'pressure', timeidx=timeidx)
    pw = wrf.getvar(nc_file, 'pw', timeidx=timeidx)

    P = wrf.interplevel(P_all, height, desiredlev)
    T = wrf.interplevel(T_all, height, desiredlev)
    u = wrf.interplevel(u_all, height, desiredlev)
    v = wrf.interplevel(v_all, height, desiredlev)

    data = {
        'pwater': ('Precipitable Water (kg/m2)', pw),
        'temp': ('Temperature (C)', T),
        'wind': ('Wind speed (m/s)', np.sqrt(u ** 2 + v ** 2)),
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


def build_gif_frame(lats, lons, caption, variable, date):
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
    date = start_date + timedelta(hours=timeidx * time_size) - timedelta(hours=5)

    data = get_data(nc_file, timeidx)

    (caption, variable) = data[nc_var]
    (lats, lons) = wrf.latlon_coords(variable)

    fig = build_gif_frame(lats, lons, caption, variable, date)

    png_file = f"{nc_var}_{timeidx}.png"
    try:
        fig.write_image(png_file)
    except Exception:
        return None

    img = imageio.imread(png_file)
    os.remove(png_file)

    if timeidx == time_size - 1:
        build_folium_map(lats, lons, caption, variable, date)

    return img


def build_folium_map(lats, lons, caption, variable, start_date):
    vmin = variable.min() - variable.median() / 10
    vmax = variable.max() + variable.median() / 10

    contour = plt.contourf(lons, lats, variable,
                           cmap=plt.cm.jet, vmin=vmin, vmax=vmax)
    cbar = plt.colorbar(contour)

    gj = json.loads(geojsoncontour.contourf_to_geojson(
        contourf=contour, ndigits=4, unit='m'))

    f_map = folium.Map(
        location=[lats.mean(), lons.mean()],
        tiles='Cartodb Positron',
        zoom_start=12
    )

    folium.GeoJson(
        gj,
        style_function=lambda x: {
            'color': x['properties']['stroke'],
            'weight': x['properties']['stroke-width'],
            'fillColor': x['properties']['fill'],
            'opacity': 0.3
        },
        name='contour'
    ).add_to(f_map)

    colormap = cm.LinearColormap(
        colors=['darkblue', 'blue', 'cyan', 'green', 'greenyellow', 'yellow', 'orange', 'red', 'darkred'],
        index=np.array(cbar.values),
        vmin=cbar.values[0],
        vmax=cbar.values[len(cbar.values) - 1],
        caption=caption
    )
    f_map.add_child(colormap)

    folium.GeoJson(
        baq_geojson,
        style_function=lambda x: {
            'color': 'rgb(12, 131, 242)',
            'fillColor': 'rgba(255, 0, 0, 0)'
        },
        name='baq_map'
    ).add_to(f_map)

    var_geo_bounds = wrf.geo_bounds(variable)
    for lat in np.arange(var_geo_bounds.bottom_left.lat, var_geo_bounds.top_right.lat, 0.01):
        for lon in np.arange(var_geo_bounds.bottom_left.lon, var_geo_bounds.top_right.lon, 0.02):
            if baq_polygon.contains(Point(lon, lat)):
                x, y = wrf.ll_to_xy(nc_file, lat, lon)
                value = round(variable[x.item(0), y.item(0)].values.item(0), 2)
                folium.Marker(
                    location=[lat, lon],
                    popup=None,
                    icon=folium.DivIcon(
                        html=f"""<span style="font-size: 16px; color: yellow; -webkit-text-stroke: 1px black;">{value}</span>""")
                ).add_to(f_map)

    f_map.get_root().html.add_child(folium.Element(
        '<p style="text-align:center;font-size:14px;margin:4px">{} GMT-5</p>'.format(start_date)))

    f_map.save(f"{nc_var}.html")


if __name__ == '__main__':
    Path('output').mkdir(parents=True, exist_ok=True)
    os.system('rm -f ./output/*.gif ./output/*.html')
    os.chdir('./output')

    start_date = datetime.strptime(
        os.environ.get('START_DATE', None), '%Y-%m-%d %H')
    nc_variables = os.environ.get('NC_VARIABLES', None).split(',')

    for nc_var in nc_variables:
        print(nc_var)
        results = [get_image(timeidx, nc_var, start_date)
                   for timeidx in range(time_size)]
        imageio.mimwrite(f"{nc_var}.gif", [
                         img for img in results if img is not None], fps=0.5)

    print("Data saved in ./output")
