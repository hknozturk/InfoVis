import plotly.express as px
from components.data_processing import DataProcessing
import numpy as np

data_processing = DataProcessing()


class SunburstChart:

    def draw_pie(self):
        df = data_processing.get_sunburst_data()
        fig = px.sunburst(df, path=['WEATHER', 'HARM_EV'], values='FATALS', color='FATALS',
                          color_continuous_scale='reds')
        fig.update_layout(margin=dict(t=10, b=10, r=0, l=0))
        return fig
