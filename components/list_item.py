import dash_html_components as html
import pandas as pd
import json

with open('config.json', 'r') as f:
    config_path = json.load(f)
    home_directory = config_path['home_directory']
class ListItem:
    def __init__(self):
        self.states = pd.read_csv(home_directory + 'state_names.csv', sep=';')
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
