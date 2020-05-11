import plotly.express as px


class SunburstChart:
    def __init__(self):
        self.df = px.data.tips()

    def draw_pie(self):
        fig = px.sunburst(
            self.df, path=['day', 'time', 'sex'], values='total_bill')
        return fig
