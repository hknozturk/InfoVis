import dash_html_components as html


class ListItem:
    def __init__(self, data_processing):
        self.data = data_processing

    def generateItems(self, sort_by):
        self.list = []
        self.font_weights = [500, 500, 500, 500, 500, 500]
        if sort_by == 'AccidentsPerMil':
            self.font_weights = [600, 500, 500, 500, 500, 500]
        elif sort_by == 'NumberOfAccidents':
            self.font_weights = [500, 600, 500, 500, 500, 500]
        elif sort_by == 'DeathsPerMil':
            self.font_weights = [500, 500, 600, 500, 500, 500]
        elif sort_by == 'NumberOfDeaths':
            self.font_weights = [500, 500, 500, 600, 500, 500]
        elif sort_by == 'AvgArrivalTime':
            self.font_weights = [500, 500, 500, 500, 600, 500]
        else:
            self.font_weights = [500, 500, 500, 500, 500, 600]

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
                        html.Img(title="Accidents per million / Total Accidents", src="./assets/icons/transport.svg",
                                 className="list-item-icon")
                    ], className='grid-cell'),
                    html.Div([
                        html.Small([str(round(row['AccidentsPerMil'], 2)) + '/1M'],
                                   style={'fontWeight': self.font_weights[0]}, title="Accidents per million"),
                        html.Small([str(int(row['NumberOfAccidents']))],
                                   style={'fontWeight': self.font_weights[1]}, title="Total accidents")
                    ], className="grid-cell"),
                    html.Div([
                        html.Img(title="Deaths per million / Total Deaths", src="./assets/icons/cemetery.svg",
                                 className="list-item-icon")
                    ], className='grid-cell'),
                    html.Div([
                        html.Small([str(round(row['DeathsPerMil'], 2)) + '/1M'],
                                   style={'fontWeight': self.font_weights[2]}, title="Deaths per million"),
                        html.Small([str(int(row['NumberOfDeaths']))],
                                   style={'fontWeight': self.font_weights[3]}, title="Total deaths")
                    ], className="grid-cell"),
                    html.Div([html.Img(title="Average time of EMTs arrival to scene / hospital", src="./assets/icons/arr_hospital.svg",
                                       className="list-item-icon")], className='grid-cell'),
                    html.Div([
                        html.Small([str(round(row['AvgArrivalTime'], 2)) + 'min'],
                                   style={'fontWeight': self.font_weights[4]}, title="EMT arrival to scene"),
                        html.Small([str(round(row['AvgHospitalArrivalTime'], 2)) + 'min'],
                                   style={'fontWeight': self.font_weights[5]}, title="EMT arrival to hospital")
                    ], className="grid-cell")
                ], className="list-item")
            ], className="styled-list-item"))

        return self.list
