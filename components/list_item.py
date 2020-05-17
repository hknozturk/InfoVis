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
                    html.Span([row['Name']], className="grid-cell",
                              style={'fontWeight': '600'}),
                    html.Div([
                        html.Img(title="Total number of accidents", src="./assets/icons/transport.svg",
                                 className="list-item-icon")
                    ], className='grid-cell'),
                    html.Span([str(int(row['NumberOfAccidents']))],
                              className="grid-cell"),
                    html.Div([
                        html.Img(title="Total number of deaths", src="./assets/icons/cemetery.svg",
                                 className="list-item-icon")
                    ], className='grid-cell'),
                    html.Span([str(int(row['NumberOfDeaths']))],
                              className="grid-cell", style={'fontWeight': '600'}),
                    html.Div([html.Img(title="Average arrival time of EMTs to accident scenes (min)", src="./assets/icons/arr_scene.svg",
                                       className="list-item-icon")], className='grid-cell'),
                    html.Span([str(round(row['AvgArrivalTime'], 2)) + ' m'],
                              className="grid-cell"),
                    html.Div([html.Img(title="Average arrival time of EMTs to hospitals (min)", src="./assets/icons/arr_hospital.svg",
                                       className="list-item-icon")], className='grid-cell'),
                    html.Span([str(round(row['AvgHospitalArrivalTime'], 2)) + ' m'],
                              className="grid-cell")
                ], className="list-item")
            ], className="styled-list-item"))

        return self.list
