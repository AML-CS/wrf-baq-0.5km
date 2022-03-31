#!/usr/bin/env python3

import os
import re
import glob
from pathlib import Path

import numpy as np
import pandas as pd
from datetime import datetime

import pygrib

import reporter


def get_indexes_by_coord(coord, station_point, threshold=0.01):
    for (i, grid) in enumerate(coord):
        for (j, point) in enumerate(grid):
            if abs(point - station_point) <= threshold:
                return (i, j)


def update_message_value(grb, metar_value):
    lats, lons = grb.latlons()

    (i, i_j) = get_indexes_by_coord(lats, station_coords[0], threshold=1)
    (j_i, j) = get_indexes_by_coord(lons, station_coords[1], threshold=0.1)

    n_temp = np.array(grb.values, copy=True)
    n_temp[i, j] = metar_value
    grb['values'] = n_temp

    return grb.tostring()


def load_metar(grbs, filename):
    metar = pd.read_hdf(filename)

    surface_temp = grbs.select(name='Temperature')[41]
    surface_uwind = grbs.select(name='U component of wind')[41]
    surface_vwind = grbs.select(name='V component of wind')[41]
    surface_press = grbs.select(name='Surface pressure')[0]

    reporter.add({
        'interpolatedVariables': [
            f"{surface_temp}",
            f"{surface_uwind}",
            f"{surface_vwind}",
            f"{surface_press}"
        ]
    })

    metar_data_by_messagenumber = {
        surface_temp.messagenumber: metar.temp,
        surface_uwind.messagenumber: metar.uwind,
        surface_vwind.messagenumber: metar.vwind,
        surface_press.messagenumber: metar.press
    }

    return metar_data_by_messagenumber


def save_grib(messages, filename):
    grbout = open(filename, 'wb')

    for msg in messages:
        grbout.write(msg)

    grbout.close()


if __name__ == '__main__':
    (station_lat, station_lon) = os.environ.get(
        'BAQ_STATION_COORDINATES', None).split(',')
    station_coords = (float(station_lat), 359.75 + float(station_lon))

    for metar_file in glob.glob('./ogimet-data/*.h5'):
        date = datetime.strptime(
            metar_file, './ogimet-data/metar_%Y%m%d_%H_00.h5')
        grib_file = './gfs-data/gfs_{0:%Y}{0:%m}{0:%d}_{0:%H}_00.pgrb2.0p25'.format(
            date)

        print(f"Interpolate {grib_file}, based on {metar_file}")

        grbs = pygrib.open(grib_file)
        metar_data_by_messagenumber = load_metar(grbs, metar_file)

        messages = []
        for grb in grbs:
            if grb.messagenumber in metar_data_by_messagenumber.keys():
                messages.append(update_message_value(
                    grb, metar_data_by_messagenumber[grb.messagenumber]))
            else:
                messages.append(grb.tostring())

        grbs.close()

        save_grib(messages, grib_file)

        print(f"{grib_file} saved in ./gfs-data")
