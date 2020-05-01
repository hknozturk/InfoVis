import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from map import PlotlyMap
from graph_with_slider import GraphWithSlider

plotlyMap = PlotlyMap()
graphWithSlider = GraphWithSlider()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.Div([
        html.H3('Plotly Demos', style={'textAlign': 'center'})
    ]),
    dcc.Graph(figure=plotlyMap.drawMap()),
    dcc.Graph(id='graph-with-slider'),
    graphWithSlider.initSlider()
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    return graphWithSlider.update_figure(selected_year)


if __name__ == "__main__":
    app.run_server(debug=True)
