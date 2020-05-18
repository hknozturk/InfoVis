import plotly.graph_objects as go


class BarPlot:

    def __init__(self, data_processing):
        self.data = data_processing

    def timeline_bar_plot(self):
        timeline_df = self.data.get_years_timeline()
        fig = go.Figure(data=[
            go.Bar(name='Accidents', x=timeline_df.index,
                   y=timeline_df['ACCIDENT'], marker_color='rgb(98,109,250)'),
            go.Bar(name='Persons', x=timeline_df.index,
                   y=timeline_df['PERSONS'], marker_color='rgb(5,204,150)'),
            go.Bar(name='Fatals', x=timeline_df.index,
                   y=timeline_df['FATALS'], marker_color='rgb(239,84,59)')
        ])
        fig.update_layout(margin=dict(t=50, b=0, r=0, l=0), paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#67748E"))
        return fig

    def months_bar_plot(self):
        months_fatal_df = self.data.get_data_grouped_by_times('MONTH')
        fig = go.Figure(data=[
            go.Bar(x=months_fatal_df.index, y=months_fatal_df, marker={
                'color': months_fatal_df, 'colorscale': 'reds'})
        ])
        fig.update_layout(coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#67748E"),
                          plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, r=10, l=10), height=150,
                          clickmode="event+select",
                          xaxis=dict(
                              tickmode='array',
                              tickvals=months_fatal_df.index,
                              ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May',
                                        'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                          ))
        return fig

    def days_bar_plot(self):
        days_fatal_df = self.data.get_data_grouped_by_times('DAY_WEEK')
        fig = go.Figure(data=[
            go.Bar(x=days_fatal_df.index, y=days_fatal_df, marker={
                'color': days_fatal_df, 'colorscale': 'reds'})
        ])
        fig.update_layout(coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#67748E"),
                          plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, r=10, l=10), height=150,
                          clickmode="event+select",
                          xaxis=dict(
                              tickmode='array',
                              tickvals=days_fatal_df.index,
                              ticktext=['Sun', 'Mon', 'Tue', 'Wed',
                                        'Thu', 'Fri', 'Sat']
                          )
                          )
        return fig

    @staticmethod
    def retrieve_selected_months(months_data):
        """
        return list of selected months.
        :param months_data: List of points that is selected on months bar chart.
        """
        selected_months = []
        points = months_data.get('points')

        for point in points:
            month_number = point.get('x')
            selected_months.append(month_number)

        return selected_months
