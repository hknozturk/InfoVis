import dash_core_components as dcc
import dash_html_components as html


class ChecklistFilterAttributes:
    def __init__(self):
        pass

    def generate_checklist(self):
        return html.Div([
            html.Label('Filter accidents'),
            dcc.Checklist(
                id='check_box',
                options=[
                    {'label': 'Speeding', 'value': 'SPEEDREL'},
                    {'label': 'Drinking', 'value': 'DRUNK_DR'},
                    {'label': 'Driver License', 'value': 'L_TYPE'}
                ],
                value=[],
                persistence='persisted',
                labelStyle={'display': 'inline-block'},
                style={'marginTop': '-15px',
                       'marginLeft': '10px', 'marginRight': '10px'}
            )
        ])
