import os
from urllib.request import urlopen
import json
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

with open('config.json', 'r') as f:
    config_path = json.load(f)
    home_directory = config_path['home_directory']


class PlotlyMap:
    def __init__(self):
        self.token = os.getenv('MAPBOX_PUBLIC_TOKEN')
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            self.counties = json.load(response)

    def draw_map(self, selected_states=[]):
        if selected_states:
            return self.draw_counties_map(selected_states)
        deaths = self.get_states_data()
        fig = go.Figure(data=go.Choropleth(
            locations=deaths.index,  # Spatial coordinates
            z=deaths,  # Data to be color-coded
            colorscale='Reds',
            locationmode='USA-states',
            colorbar_title="Deaths",
        ))

        fig.update_layout(
            geo_scope='usa',  # limite map scope to USA
        )

        return fig

    def draw_counties_map(self, selected_states):
        filtered_df = self.get_selected_state_data(selected_states)
        fips = (filtered_df['STATE'].astype(str) + filtered_df['COUNTY'].astype(str)).unique()
        fig = go.Figure(
            go.Choropleth(geojson=self.counties, locations=fips,
                          z=filtered_df.groupby(['STATE', 'COUNTY'])['FATALS'].sum(),
                          colorscale="Reds", zmin=0, zmax=50,
                          marker_opacity=0.5, marker_line_width=0))
        fig.update_layout(mapbox_style="carto-positron", geo_scope='usa',
                          mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129})
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig

    def get_states_data(self):
        accident_df = pd.read_csv(
            home_directory + "FARS/National/FARS2018NationalCSV/ACCIDENT.csv")
        map_df = pd.read_csv(home_directory + 'state_names.csv', sep=';')
        deaths = accident_df.groupby(['STATE'])['FATALS'].sum()
        d = map_df.set_index('Number')['Code'].to_dict()
        deaths.index = deaths.index.map(d)

        return deaths

    def get_selected_state_data(self, selected_states):
        accident_df = pd.read_csv(
            home_directory + "FARS/National/FARS2018NationalCSV/ACCIDENT.csv")
        filtered_df = accident_df.loc[
            (accident_df['STATE'].isin(selected_states))]
        filtered_df['STATE'] = filtered_df['STATE'].map("{:02}".format)
        filtered_df['COUNTY'] = filtered_df['COUNTY'].map("{:03}".format)
        return filtered_df
