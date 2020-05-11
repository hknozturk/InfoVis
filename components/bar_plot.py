import plotly.graph_objects as go


class BarPlot:

    def __init__(self, data_processing):
        self.data = data_processing

    def timeline_bar_plot(self):
        timeline_df = self.data.get_years_timeline()
        fig = go.Figure(data=[
            go.Bar(name='Accidents', x=timeline_df.index, y=timeline_df['ACCIDENT']),
            go.Bar(name='Fatals', x=timeline_df.index, y=timeline_df['FATALS'])
        ])
        return fig
