import os
from urllib.request import urlopen
import json
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
load_dotenv()


class PlotlyMap:
    def __init__(self):
        self.token = os.getenv('MAPBOX_PUBLIC_TOKEN')
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            self.counties = json.load(response)

    def drawMap(self):
        df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/fips-unemp-16.csv",
                         dtype={"fips": str})

        fig = go.Figure(go.Choroplethmapbox(geojson=self.counties, locations=df.fips, z=df.unemp,
                                            colorscale="Viridis", zmin=0, zmax=12, marker_line_width=0))
        fig.update_layout(mapbox_style="light", mapbox_accesstoken=self.token,
                          mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129})
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

        return fig
