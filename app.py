"""
bokeh serve --show app.py
"""
import time

from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, curdoc
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
import numpy as np

from snapshot import Snapshot, load_latest_snapshot


def wgs84_to_web_mercator(xs, ys):
    """Convert lat, lon to Web Mercator coords.

    Taken from https://stackoverflow.com/questions/57178783/how-to-plot-latitude-and-longitude-in-bokeh
    """
    K = 6378137
    wm_lons = [x * (K * np.pi / 180.0) for x in xs]
    wm_lats = [np.log(np.tan((90 + y) * np.pi / 360.0)) * K for y in ys]

    return (wm_lons, wm_lats)


p = figure(
    title="buses",
    x_axis_label="longitude",
    y_axis_label="latitude",
    x_range=(3200000, 3250000),  # range bounds in web mercator coordinates
    y_range=(5010000, 5020000),
    x_axis_type="mercator",
    y_axis_type="mercator",
    # tools="hover,pan,wheel_zoom,zoom_in,zoom_out,reset",
    tooltips="license: @license\ntime: @time",
)
tile_provider = get_provider(CARTODBPOSITRON)
p.add_tile(tile_provider)

source = ColumnDataSource({"lat": [], "lon": [], "licence": []})

bus_renderer = p.circle(
    x="lon",
    y="lat",
    size=5,
    # fill_color="col",
    fill_color="blue",
    line_color=None,
    fill_alpha=0.5,
    source=source,
)

ds = bus_renderer.data_source


def update1():
    import random

    new_data = {}
    xs, ys = wgs84_to_web_mercator(
        [28.8 + random.random() * 0.4], [40.9 + random.random() * 0.3]
    )
    new_data["lon"] = ds.data["lon"] + xs
    new_data["lat"] = ds.data["lat"] + ys
    new_data["licence"] = ds.data["licence"] + ["abidin"]
    ds.data = new_data
    print("Hi!")


def update():
    ss: Snapshot = load_latest_snapshot()
    vehicle_data = [(v.Boylam, v.Enlem, v.Plaka, v.Saat) for v in ss.vehicles]
    xs, ys, licences, times = zip(*vehicle_data)
    wm_lons, wm_lats = wgs84_to_web_mercator(xs=xs, ys=ys)
    new_data = {"lon": wm_lons, "lat": wm_lats, "license": licences, "time": times}
    ds.data = new_data
    print("Hi!", ss.ts, time.time(), len(ss.vehicles), xs[:3], ys[:3], licences[:3])


update()
curdoc().add_root(p)
curdoc().add_periodic_callback(callback=update, period_milliseconds=60000)
