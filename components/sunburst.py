import plotly.express as px
from components.data_processing import DataProcessing

data_processing = DataProcessing()


class SunburstChart:

    def draw_pie(self):
        df = data_processing.get_sunburst_data()
        fig = px.sunburst(df, path=['WEATHER', 'HARM_EV'], values='FATALS')
        return fig
