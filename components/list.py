import dash_html_components as html
import dash_core_components as dcc
from components.list_item import ListItem


class List:
    def __init__(self, data_processing):
        self.listItem = ListItem(data_processing)

    def generateList(self):
        listItems = self.listItem.generateItems()

        return html.Div([
            html.Div([
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
                    style={'font-size': '14px', 'margin-bottom': '5px'}
                )
            ]),
            html.Ul(listItems)
        ])
