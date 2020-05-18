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
from components.sunburst import SunburstChart
from components.checklist_filter_attributes import ChecklistFilterAttributes

# importing data_processing module
from components.data_processing import DataProcessing

from attributes.crash_level import *

# dataProcessing object has all methods related data pre processing
# We can pass dataProcessing object to other components to get the data.
dataProcessing = DataProcessing()

plotlyMap = PlotlyMap(dataProcessing)
yearSlider = YearRangeSlider(dataProcessing)
barPlot = BarPlot(dataProcessing)
graphWithSlider = GraphWithSlider()
listComponent = List(dataProcessing)
switchToggle = SwitchToggle()
sunBurst = SunburstChart(dataProcessing)
checklist = ChecklistFilterAttributes()

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
            checklist.generate_checklist(),
            html.Div([
                html.Label('Year slider'),
                yearSlider.year_slider(),
            ], style={'marginTop': '20px'}),
            html.Div([
                html.Label('Filter months'),
                dcc.Graph(id='months-filter', figure=barPlot.months_bar_plot(),
                          style={'marginLeft': '10px'},
                          config={
                    'displayModeBar': False
                })
            ], style={'marginTop': '40px'}),
            html.Div([
                html.Label('Filter days'),
                dcc.Graph(id='days-filter', figure=barPlot.days_bar_plot(),
                          style={'marginLeft': '10px'},
                          config={
                    'displayModeBar': False
                })
            ], style={'marginTop': '40px'}),
            html.Div([
                html.Label('Filter hours'),
                dcc.Graph(id='hours-filter', figure=barPlot.hours_bar_plot(),
                          style={'marginLeft': '10px'},
                          config={
                    'displayModeBar': False
                })
            ], style={'marginTop': '40px'})
        ])
    ], className="card"),
    html.Div(id='card-2', children=[
        dcc.Graph(figure=plotlyMap.draw_map(),
                  id='map',
                  style={'width': '100%', 'height': '100%'})
    ], className="card"),
    html.Div(id='card-3', children=[
        html.Div(id="list-component", children=[
            listComponent.generateList("DeathsPerMil", False)
        ], className="scrollable", style={'margin': '4px'})
    ], className="card"),
    html.Div(id='card-4', children=[
        dcc.Graph(figure=barPlot.timeline_bar_plot(),
                  id='timeline_bar_plot',
                  style={'width': '100%', 'height': '100%'})
    ], className="card"),
    html.Div(id='card-5', children=[
        dcc.Graph(figure=sunBurst.draw_pie(),
                  id='sunburst',
                  style={'width': '100%', 'height': '100%'})
    ], className="card")
], className="wrapper")


@app.callback(
    [Output('map', 'figure'),
     Output('timeline_bar_plot', 'figure'),
     Output('sunburst', 'figure'),
     Output('list-component', 'children')],
    [Input('year-range-slider', 'value'),
     Input('months-filter', 'selectedData'),
     Input('days-filter', 'selectedData'),
     Input('check_box', 'value'),
     Input('map', 'selectedData'),
     Input('dark-mode-toggle', 'on'),
     Input('sort-list', 'value')]
)
def update_figure(selected_years, s_months, s_days, f_values, selected_data, dark_mode, list_sort_value):
    # print(f_values)
    state_ids = []
    months = []
    days = []
    if selected_data:
        state_ids = plotlyMap.retrieve_selected_states(selected_data)
    if s_months:
        months = barPlot.retrieve_selected_barchart_item(s_months)
    if s_days:
        days = barPlot.retrieve_selected_barchart_item(s_days)

    dataProcessing.filter_data(selected_years, months, days, f_values)

    return [plotlyMap.draw_map(selected_states=state_ids, dark_theme=dark_mode), barPlot.timeline_bar_plot(),
            sunBurst.draw_pie(), listComponent.generateList(list_sort_value, dark_mode)]


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
