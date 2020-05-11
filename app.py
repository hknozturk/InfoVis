import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from components.map import PlotlyMap
from components.graph_with_slider import GraphWithSlider
import custom_dash_index
from components.list import List
from components.switch_toggle import SwitchToggle
from components.year_range_slider import YearRangeSlider
from components.bar_plot import BarPlot

# importing data_processing module
from components.data_processing import DataProcessing

# dataProcessing object has all methods related data pre processing
# We can pass dataProcessing object to other components to get the data.
dataProcessing = DataProcessing()

plotlyMap = PlotlyMap(dataProcessing)
yearSlider = YearRangeSlider(dataProcessing)
barPlot = BarPlot(dataProcessing)
graphWithSlider = GraphWithSlider()
listComponent = List(dataProcessing)
switchToggle = SwitchToggle()

app = dash.Dash(__name__)
app.index_string = custom_dash_index.indexString

theme = {
    'dark': False,
    'detail': '#007439',
    'primary': '#00EA64',
    'secondary': '#6E6E6E'
}

server = app.server

app.layout = html.Div(id="app-layout", children=[
    html.Div(id='card-1', children=[
        switchToggle.generateToggle(),
        html.Div([
            listComponent.generateList()
        ], className="scrollable", style={'margin': '4px'})
    ], className="card"),
    html.Div(id='card-2', children=[
        dcc.Graph(figure=plotlyMap.draw_map(),
                  id='map',
                  style={'width': '100%', 'height': '100%'})
    ], className="card"),
    html.Div(id='card-3', children=[
        html.H4('Dashboard Parameter Settings', style={'textAlign': 'center'}),
        html.Div([
            html.Span('Year slider'),
            yearSlider.year_slider()
        ])
    ], className="card"),
    html.Div(id='card-4', children=[
        dcc.Graph(figure=barPlot.timeline_bar_plot(),
                  id='timeline_bar_plot',
                  style={'width': '100%', 'height': '100%'})
    ], className="card"),
    html.Div(id='card-5', children=[

    ], className="card")
], className="wrapper")


@app.callback(
    Output('map', 'figure'),
    [Input('year-range-slider', 'value'),
     Input('map', 'selectedData')]
)
def update_figure(selected_years, selected_data):
    dataProcessing.filter_data(selected_years)
    if selected_data is None:
        return plotlyMap.draw_map()
    else:
        state_ids = plotlyMap.retrieve_selected_states(selected_data)
        return plotlyMap.draw_map(state_ids)


@app.callback(
    Output('app-layout', 'style'),
    [Input('dark-mode-toggle', 'on')]
)
def update_style_layout(darkMode):
    return switchToggle.updateLayoutStyle(darkMode)


@app.callback(
    [Output('card-1', 'style'),
     Output('card-2', 'style'),
     Output('card-3', 'style'),
     Output('card-4', 'style'),
     Output('card-5', 'style')],
    [Input('dark-mode-toggle', 'on')]
)
def update_card_style(darkMode):
    return switchToggle.updateCardStyle(darkMode)


if __name__ == "__main__":
    app.run_server(debug=True)
