import dash_html_components as html
import dash_core_components as dcc


class FilterDataDropdown:
    def __init__(self, filter_value):
        self.filter_value = filter_value

    def generate_dropdown(self):
        return html.Div([
            dcc.Dropdown(
                id='filter-data',
                options=[
                        {'label': 'Fatality', 'value': 'FATALS'},
                        {'label': 'Speeding', 'value': 'SPEEDREL'},
                        {'label': 'Drinking', 'value': 'DR_DRINK'},
                        {'label': 'Driver License', 'value': 'L_TYPE'}
                        ],
                value=self.filter_value,
                searchable=False,
                clearable=False,
                style={'fontSize': '14px',
                       'width': '-webkit-fill-available'}
            )
        ], style={'marginTop': '10px', 'padding': '10px'})
