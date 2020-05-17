import plotly.graph_objects as go
import plotly.express as px


class PlotlyMap:

    def __init__(self, data_processing):
        self.data = data_processing

    def draw_map(self, selected_states=[], dark_theme=False):
        if selected_states:
            return self.draw_counties_map(selected_states, dark_theme)
        states_df = self.data.get_states_data()
        fig = go.Figure(data=px.choropleth(
            states_df,
            locations='Code',
            color='FATALS',
            color_continuous_scale='Reds',
            locationmode='USA-states',
            hover_name='Name',
            hover_data=['FATALS']
        ))

        self.set_layout(fig, dark_theme)

        return fig

    def draw_counties_map(self, selected_states, dark_theme):
        filtered_df = self.data.get_selected_state_data(selected_states)
        fig = go.Figure(
            px.choropleth(filtered_df, geojson=self.data.geojson, locations=filtered_df.index,
                          color='FATALS',
                          hover_name='county_name',
                          hover_data=['FATALS'],
                          color_continuous_scale="Reds"))

        self.set_layout(fig, dark_theme)

        return fig

    def retrieve_selected_states(self, selected_states):
        """
        return list of state id to update map figure.
        :param selected_states: List of points that is selected on map.
        """
        selected_states_id = []
        points = selected_states.get('points')
        states = self.data.state_names_df
        states['Number'] = states.index

        for point in points:
            location = point.get('location')
            state = states.loc[states['Code'] == location, 'Number']

            if len(state.to_numpy()) > 0:
                state_id = state.to_numpy()[0]
                selected_states_id.append(state_id)

        return selected_states_id

    def set_layout(self, fig, dark_theme):
        if dark_theme:
            return fig.update_layout(
                geo=dict(bgcolor='rgb(34, 34, 34)',
                         lakecolor='rgb(74,128,245)'),
                paper_bgcolor='rgb(34, 34, 34)',
                plot_bgcolor='rgb(34, 34, 34)',
                font={"color": "White"},
                geo_scope='usa',
                margin={"r": 0, "t": 40, "l": 0, "b": 0},
                clickmode="event+select")
        else:
            return fig.update_layout(
                geo=dict(bgcolor='rgb(255, 255, 255)',
                         lakecolor='rgb(74,128,245)'),
                paper_bgcolor='rgb(255, 255, 255)',
                plot_bgcolor='rgb(255, 255, 255)',
                font={"color": "Black"},
                geo_scope='usa',
                margin={"r": 0, "t": 40, "l": 0, "b": 0},
                clickmode="event+select")
