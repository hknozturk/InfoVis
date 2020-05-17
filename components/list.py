import dash_html_components as html
import dash_core_components as dcc
from components.list_item import ListItem


class List:
    def __init__(self, data_processing):
        self.listItem = ListItem(data_processing)

    def generateList(self, order_by):
        listItems = self.listItem.generateItems(order_by)

        return html.Div([
            html.Div([
                html.Span(['Sort By:'], style={'width': '80px'}),
                dcc.Dropdown(
                    id='list-filter',
                    options=[
                        {'label': 'Number of deaths', 'value': 'NumberOfDeaths'},
                        {'label': 'Number of accidents',
                            'value': 'NumberOfAccidents'},
                        {'label': 'EMT arrival time to scene',
                         'value': 'AvgArrivalTime'},
                        {'label': 'EMT arrival time to hospital',
                         'value': 'AvgHospitalArrivalTime'}
                    ],
                    value='NumberOfDeaths',
                    searchable=False,
                    clearable=False,
                    style={'fontSize': '14px',
                           'width': '-webkit-fill-available'}
                )
            ], style={'position': 'sticky', 'top': 0, 'zIndex': 10, 'display': 'flex', 'alignItems': 'center', 'backgroundColor': 'white'}),
            html.Ul(listItems, style={'marginTop': '10px'})
        ])
