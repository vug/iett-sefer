"""
bokeh serve --show app.py
"""
from collections import defaultdict

from bokeh.models import ColumnDataSource, MultiLine
from bokeh.plotting import figure, curdoc
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
import numpy as np

from snapshot import load_latest_snapshots


def lat2wmlat(lat: float) -> float:
    """Convert latitude in degrees to Web Mercator latitude.

    Taken from https://stackoverflow.com/questions/57178783/how-to-plot-latitude-and-longitude-in-bokeh
    """
    K = 6378137
    wm_lat = np.log(np.tan((90 + lat) * np.pi / 360.0)) * K
    return wm_lat


def lon2wmlon(lon: float) -> float:
    """Convert longidute in degrees to Web Mercator longitude."""
    K = 6378137
    wm_lon = lon * (K * np.pi / 180.0)
    return wm_lon


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

# lines connecting successive N locations of a bus
line_source = ColumnDataSource({"lat": [], "lon": [], "licence": []})
glyph = MultiLine(xs="lon", ys="lat", line_color="blue", line_width=1, line_alpha=0.5)
bus_line_renderer = p.add_glyph(line_source, glyph)

# disks indicating latest location of a bus
circle_source = ColumnDataSource({"lat": [], "lon": [], "licence": []})
bus_circle_renderer = p.circle(
    x="lon",
    y="lat",
    size=2.5,
    fill_color="blue",
    line_color=None,
    fill_alpha=0.5,
    source=circle_source,
)


def update():
    snapshots = load_latest_snapshots(2)

    lic2bus = defaultdict(list)
    # Group each snapshot by license plates
    # license -> [buses with that license in successive snapshots]
    for snapshot in snapshots:
        for bus in snapshot.vehicles:
            if bus.Plaka is None:
                continue
            lic2bus[bus.Plaka].append(bus)

    new_data = {
        "lon": [[lon2wmlon(bus.Boylam) for bus in buses] for buses in lic2bus.values()],
        "lat": [[lat2wmlat(bus.Enlem) for bus in buses] for buses in lic2bus.values()],
        "license": list(lic2bus.keys()),
        "time": [buses[-1].Saat for buses in lic2bus.values()],
    }

    bus_line_renderer.data_source.data = new_data
    print(
        "Hi!",
        new_data["lon"][:3],
        new_data["lat"][:3],
        new_data["license"][:3],
        new_data["time"][:3],
    )

    new_data["lon"] = [vals[-1] for vals in new_data["lon"]]
    new_data["lat"] = [vals[-1] for vals in new_data["lat"]]
    bus_circle_renderer.data_source.data = new_data


update()
curdoc().add_root(p)
curdoc().add_periodic_callback(callback=update, period_milliseconds=60000)
