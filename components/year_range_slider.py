import dash_core_components as dcc


class YearRangeSlider:

    def __init__(self, data_processing):
        self.data = data_processing

    def year_slider(self):
        return dcc.RangeSlider(
            id='year-slider',
            min=self.data.accident_df['YEAR'].min(),
            max=self.data.accident_df['YEAR'].max(),
            value=[self.data.accident_df['YEAR'].min(), self.data.accident_df['YEAR'].max()],
            marks={str(year): str(year) for year in self.data.accident_df['YEAR'].unique()},
            step=None
        )
