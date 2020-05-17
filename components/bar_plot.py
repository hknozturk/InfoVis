import plotly.graph_objects as go


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
