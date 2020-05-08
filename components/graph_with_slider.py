import pandas as pd
import dash_core_components as dcc


class GraphWithSlider:
    def __init__(self):
        self.df = pd.read_csv(
            'https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

    def initSlider(self):
        return dcc.Slider(
            id='year-slider',
            min=self.df['year'].min(),
            max=self.df['year'].max(),
            value=self.df['year'].min(),
            marks={str(year): str(year) for year in self.df['year'].unique()},
            step=None
        )

    def update_figure(self, selected_year):
        filtered_df = self.df[self.df.year == selected_year]
        traces = []

        for i in filtered_df.continent.unique():
            df_by_continent = filtered_df[filtered_df['continent'] == i]
            traces.append(dict(
                x=df_by_continent['gdpPercap'],
                y=df_by_continent['lifeExp'],
                text=df_by_continent['country'],
                mode='markers',
                opacity=0.7,
                marker={
                    'size': 15,
                    'line': {'width': 0.5, 'color': 'white'}
                },
                name=i
            ))

        return {
            'data': traces,
            'layout': dict(
                xaxis={'type': 'log', 'title': 'GDP Per Capita',
                       'range': [2.3, 4.8]},
                yaxis={'title': 'Life Expectancy', 'range': [20, 90]},
                legend={'x': 0, 'y': 1},
                hovermode='closest',
                transition={'duration': 500}
            )
        }
