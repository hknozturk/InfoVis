import dash_html_components as html


class ListItem:
    def __init__(self, data_processing):
        self.data = data_processing

    def generateItems(self):
        self.list = []
        for index, row in self.data.state_names_df.iterrows():
            self.list.append(html.Li([
                html.Div([
                    html.Span([row['Name']]),
                    html.Small([row['Code']])
                ])
            ], className="styled-list-item"))

        return self.list
