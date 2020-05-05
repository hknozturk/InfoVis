import dash_html_components as html
import pandas as pd


class ListItem:
    def __init__(self):
        self.states = pd.read_csv('./datasets/state_names.csv', sep=';')
        self.generateItems()

    def generateItems(self):
        self.list = []
        for index, row in self.states.iterrows():
            self.list.append(html.Li([
                html.Div([
                    html.Span([row['Name']]),
                    html.Small([row['Code']])
                ])
            ], className="styled-list-item"))

        return self.list
