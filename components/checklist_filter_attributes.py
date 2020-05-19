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
                    {'label': 'Work Zone', 'value': 'WRK_ZONE'},
                    {'label': 'Invalid Driver License', 'value': 'L_STATUS'}
                ],
                value=[],
                persistence='persisted',
                labelStyle={'display': 'inline-block'},
                style={'marginTop': '-3px',
                       'marginLeft': '10px', 'marginRight': '10px', 'lineHeight': '0.75'}
            )
        ])
