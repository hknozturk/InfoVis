import plotly.express as px
from components.data_processing import DataProcessing

data_processing = DataProcessing()


class SunburstChart:
    def __init__(self):
        self.df = px.data.tips()
        self.data = data_processing.filter_accident_df
        data_processing.get_weather_info()

    def draw_pie(self):
        fig = px.sunburst(
            self.data, path=['WEATHER', 'HARM_EV'])
        return fig
