import plotly.graph_objects as go
import plotly.express as px


class BarPlot:

    def __init__(self, data_processing):
        self.data = data_processing

    def timeline_bar_plot(self):
        timeline_df = self.data.get_years_timeline()
        fig = go.Figure(data=[
            go.Bar(name='Accidents', x=timeline_df.index,
                   y=timeline_df['ACCIDENT'], marker_color='rgb(98,109,250)'),
            go.Bar(name='Persons', x=timeline_df.index,
                   y=timeline_df['PERSONS'], marker_color='rgb(5,204,150)'),
            go.Bar(name='Fatals', x=timeline_df.index,
                   y=timeline_df['FATALS'], marker_color='rgb(239,84,59)')
        ])
        fig.update_layout(margin=dict(t=50, b=0, r=0, l=0))
        return fig

    def months_bar_plot(self):
        months_fatal_df = self.data.get_data_grouped_by_months()
        fig = go.Figure(data=[
            go.Bar(name="Anani siktim oc",
                   x=months_fatal_df.index, y=months_fatal_df, marker={'color': months_fatal_df, 'colorscale': 'reds'})
        ])
        fig.update_layout(coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, r=10, l=10), height=200,
                          xaxis=dict(
                              tickmode='array',
                              tickvals=months_fatal_df.index,
                              ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May',
                                        'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                          )
                          )

        return fig
