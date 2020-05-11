import dash_html_components as html


class ListItem:
    def __init__(self, data_processing):
        self.data = data_processing

    def generateItems(self):
        self.list = []
        for index, row in self.data.get_accident_data_ordered_by_states().iterrows():
            self.list.append(html.Li([
                html.Div([
                    html.Div([
                        html.Img(src="./assets/flags/" +
                                 row['Code'].lower()+".svg", className="state-flag"),
                        html.Span([row['Code']])
                    ], className="grid-cell"),
                    html.Small([row['Name']], className="grid-cell"),
                    html.Div([
                        html.Img(title="Total number of deaths", src="./assets/icons/cemetery.svg",
                                 className="list-item-icon")
                    ], className='grid-cell'),
                    html.Span(['Total: ' + str(row['Total Death'])],
                              className="grid-cell"),
                    html.Div([html.Img(title="Average number of vehicle involved", src="./assets/icons/transport.svg",
                                       className="list-item-icon")], className='grid-cell'),
                    html.Span(['Avg: ' + str(round(row['Avg Cars Involved'], 2))],
                              className="grid-cell")
                ], className="list-item")
            ], className="styled-list-item"))

        return self.list
