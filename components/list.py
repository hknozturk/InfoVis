import dash_html_components as html
import dash_core_components as dcc
from components.list_item import ListItem


class List:
    def __init__(self, data_processing):
        self.listItem = ListItem(data_processing)

    def generateList(self, sort_by, dark_theme):
        listItems = self.listItem.generateItems(sort_by)

        if dark_theme:
            background_color = 'rgb(34, 34, 34)'
        else:
            background_color = 'rgb(255, 255, 255)'

        return html.Div([
            html.Div([
                html.Span(['Sort By:'], style={'width': '80px'}),
                dcc.Dropdown(
                    id='sort-list',
                    options=[
                        {'label': 'Deaths per 1 million',
                            'value': 'NumberOfDeaths'},
                        {'label': 'Accidents per 1 million',
                            'value': 'NumberOfAccidents'},
                        {'label': 'EMT arrival time to scene',
                         'value': 'AvgArrivalTime'},
                        {'label': 'EMT arrival time to hospital',
                         'value': 'AvgHospitalArrivalTime'}
                    ],
                    value=sort_by,
                    searchable=False,
                    clearable=False,
                    style={'fontSize': '14px',
                           'width': '-webkit-fill-available'}
                )
            ], style={'position': 'sticky', 'top': 0, 'zIndex': 10, 'display': 'flex', 'alignItems': 'center', 'backgroundColor': background_color}),
            html.Ul(listItems, style={'marginTop': '10px'})
        ])
