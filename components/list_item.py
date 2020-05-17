import dash_html_components as html


class ListItem:
    def __init__(self, data_processing):
        self.data = data_processing

    def generateItems(self, sort_by):
        self.list = []
        self.font_weights = [500, 500, 500, 500]
        if sort_by == 'NumberOfAccidents':
            self.font_weights = [600, 500, 500, 500]
        elif sort_by == 'AvgArrivalTime':
            self.font_weights = [500, 500, 600, 500]
        elif sort_by == 'AvgHospitalArrivalTime':
            self.font_weights = [500, 500, 500, 600]
        else:
            self.font_weights = [500, 600, 500, 500]

        for _, row in self.data.get_accident_data_ordered_by_states(sort_by).iterrows():
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
                        html.Img(title="Accidents per million", src="./assets/icons/transport.svg",
                                 className="list-item-icon")
                    ], className='grid-cell'),
                    html.Small([str(round(row['NumberOfAccidents'], 2)) + '/1M'],
                               className="grid-cell", style={'fontWeight': self.font_weights[0]}),
                    html.Div([
                        html.Img(title="Deaths per million", src="./assets/icons/cemetery.svg",
                                 className="list-item-icon")
                    ], className='grid-cell'),
                    html.Small([str(round(row['NumberOfDeaths'], 2)) + '/1M'],
                               className="grid-cell", style={'fontWeight': self.font_weights[1]}),
                    html.Div([html.Img(title="Average arrival time of EMTs to accident scenes (min)", src="./assets/icons/arr_scene.svg",
                                       className="list-item-icon")], className='grid-cell'),
                    html.Small([str(round(row['AvgArrivalTime'], 2)) + 'min'],
                               className="grid-cell", style={'fontWeight': self.font_weights[2]}),
                    html.Div([html.Img(title="Average arrival time of EMTs to hospitals (min)", src="./assets/icons/arr_hospital.svg",
                                       className="list-item-icon")], className='grid-cell'),
                    html.Small([str(round(row['AvgHospitalArrivalTime'], 2)) + 'min'],
                               className="grid-cell", style={'fontWeight': self.font_weights[3]})
                ], className="list-item")
            ], className="styled-list-item"))

        return self.list
