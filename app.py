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

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.Div([
        html.H4('Additional Visualisations', style={'textAlign': 'center'})
    ], className="card"),
    html.Div([
        dcc.Graph(figure=plotlyMap.drawMap(),
                  style={'width': '100%', 'height': '100%'})
    ], className="card"),
    html.Div([
        html.H4('Dashboard Parameter Settings', style={'textAlign': 'center'}),
        html.Div([
            html.Span('Year slider', className='settingsLabel'),
            graphWithSlider.initSlider()
        ])
    ], className="card"),
    html.Div([
        dcc.Graph(id='graph-with-slider',
                  style={'width': '100%', 'height': '100%'})
    ], className="card"),
    html.Div([

    ], className="card")
], className="wrapper")


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')]
)
def update_figure(selected_year):
    return graphWithSlider.update_figure(selected_year)


if __name__ == "__main__":
    app.run_server(debug=True)
