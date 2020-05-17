import plotly.express as px

class SunburstChart:

    def __init__(self, data_processing):
        self.data = data_processing

    def draw_pie(self):
        df = self.data.get_sunburst_data()
        fig = px.sunburst(df, path=['WEATHER', 'HARM_EV'], values='FATALS', color='FATALS',
                          color_continuous_scale='reds')
        fig.update_layout(margin=dict(t=10, b=10, r=0, l=0))
        return fig
