#!/bin/python3
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
import sys

from netCDF4 import Dataset
from os import system
from wrf import getvar, interplevel, to_np, latlon_coords

def get_wind_data(data: Dataset, t: int, z: int):
    z *= 1000
    height = getvar(data, "height", timeidx=t)
    u_all = getvar(data, 'ua', units="m s-1", timeidx=t)
    v_all = getvar(data, 'va', units="m s-1", timeidx=t)
    w_all = getvar(data, 'wa', units="m s-1", timeidx=t)
    u = interplevel(u_all, height, z)
    v = interplevel(v_all, height, z)
    w = interplevel(w_all, height, z)
    
    return u, v, np.sqrt(u**2+v**2+w**2) 

dataset = 'forecast'
if len(sys.argv) == 2:
    dataset = sys.argv[1]

nc = Dataset(dataset)

crs = ccrs.PlateCarree()
cmap = plt.get_cmap('plasma')
lon = (-87, -70)
lat = (5, 18)

fig = plt.figure(figsize=(20, 12))
ax = fig.add_subplot(111, facecolor='None', projection=crs)
ax.coastlines(resolution='10m')
#ax.set_xlim(lon)
#ax.set_ylim(lat)

u, v, mag = get_wind_data(nc, t=1, z=6)
lats, lons = latlon_coords(u)
plot = ax.pcolormesh(lons, lats, mag, cmap=cmap)
cbar = fig.colorbar(plot)
cbar.ax.set_ylabel('Wind speed (m/s)', fontsize=20)
cbar.ax.tick_params(labelsize=20)

gl = ax.gridlines(crs=crs, draw_labels=True, alpha=0.5)
gl.xlabel_style = {'size': 20, 'color': 'black'}
gl.ylabel_style = {'size': 20, 'color': 'black'}
gl.top_labels = None
gl.right_labels = None

def init():
    plot.set_array(np.array([]))
    return plot,

def update(i):
    u, v, mag = get_wind_data(nc, i, 6)
    plot.set_array(np.ravel(mag.values))
    return plot,

for i in range(18):
    update(i)
    plt.savefig(f'img_{str(i).zfill(4)}.png', dpi=40, bbox_inches='tight', pad_inches=0)
    plt.gca()
    
system("convert -delay 40 -loop 0 img_*.png visualization.gif && rm img_*")
