import plotly.graph_objects as go


class PlotlyMap:

    def __init__(self, data_processing):
        self.data = data_processing

    def draw_map(self, selected_states=[]):
        if selected_states:
            return self.draw_counties_map(selected_states)
        deaths = self.data.get_states_data()
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
        filtered_df = self.data.get_selected_state_data(selected_states)
        fips = (filtered_df['STATE'].astype(str) +
                filtered_df['COUNTY'].astype(str)).unique()
        fig = go.Figure(
            go.Choropleth(geojson=self.data.geojson, locations=fips,
                          z=filtered_df.groupby(['STATE', 'COUNTY'])[
                              'FATALS'].sum(),
                          colorscale="Reds", zmin=0, zmax=50,
                          marker_opacity=0.5, marker_line_width=0))
        fig.update_layout(mapbox_style="carto-positron", geo_scope='usa',
                          mapbox_zoom=3, mapbox_center={"lat": 37.0902, "lon": -95.7129})
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        return fig
