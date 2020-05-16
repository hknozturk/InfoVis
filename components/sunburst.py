import plotly.express as px
from components.data_processing import DataProcessing

data_processing = DataProcessing()


class SunburstChart:
    def __init__(self):
        self.data = data_processing.filter_accident_df
        self.weather = data_processing.get_weather_info()
        self.event = data_processing.get_harmful_event()

    def draw_pie(self):
        fig = px.sunburst(
            # self.data, path=[self.weather, self.event])
        return fig
