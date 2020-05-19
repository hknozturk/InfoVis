import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
        fig.update_layout(margin=dict(t=20, b=20, r=20, l=20), paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#67748E"))
        return fig

    def months_bar_plot(self):
        months_fatal_df = self.data.get_data_grouped_by_times('MONTH')
        fig = go.Figure(data=[
            go.Bar(x=months_fatal_df.index, y=months_fatal_df, marker={
                'color': months_fatal_df, 'colorscale': 'reds'})
        ])
        fig.update_traces(marker_line_color='rgb(87, 48, 48)',
                          marker_line_width=1)
        fig.update_layout(coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#67748E"),
                          plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, r=30, l=30), height=120,
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
        fig.update_traces(marker_line_color='rgb(87, 48, 48)',
                          marker_line_width=1)
        fig.update_layout(coloraxis_showscale=False, paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#67748E"),
                          plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, r=30, l=30), height=120,
                          clickmode="event+select",
                          xaxis=dict(
                              tickmode='array',
                              tickvals=days_fatal_df.index,
                              ticktext=['Sun', 'Mon', 'Tue', 'Wed',
                                        'Thu', 'Fri', 'Sat']
                          )
                          )
        return fig

    def hours_bar_plot(self):
        hours_fatal_df = self.data.get_data_grouped_by_times('HOUR')
        am = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        pm = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        fig = go.Figure()
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Bar(
            x=-hours_fatal_df[am], y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], name='AM', customdata=hours_fatal_df[am],
            orientation='h', marker={
                'color': hours_fatal_df[am], 'colorscale': 'reds'}, hovertemplate='%{y} AM: %{customdata}'),
            secondary_y=False)

        fig.add_trace(go.Bar(
            x=hours_fatal_df[pm], y=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], name='PM', customdata=hours_fatal_df[pm],
            orientation='h', marker={
                'color': hours_fatal_df[pm], 'colorscale': 'reds'}, hovertemplate='%{y} PM: %{customdata}'),
            secondary_y=True)

        fig.update_yaxes(title_text="AM", secondary_y=False, dtick=1)
        fig.update_yaxes(title_text="PM", secondary_y=True, dtick=1)

        fig.update_traces(marker_line_color='rgb(87, 48, 48)',
                          marker_line_width=1)
        fig.update_layout(coloraxis_showscale=False, showlegend=False, paper_bgcolor='rgba(0,0,0,0)',
                          font=dict(color="#67748E"),
                          plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=0, r=50, l=50), height=300,
                          barmode='relative', clickmode="event+select", xaxis={'showticklabels': False})

        return fig

    @staticmethod
    def retrieve_selected_barchart_item(selected_data):
        """
        return list of selected bar in bar chart.
        :param selected_data: List of points that is selected on bar chart.
        """
        selected_items = []
        points = selected_data.get('points')

        for point in points:
            item = point.get('x')
            selected_items.append(item)

        return selected_items

    @staticmethod
    def retrieve_selected_hours(selected_data):
        """
        return list of selected bar in bar chart.
        :param selected_data: List of points that is selected on bar chart.
        """
        selected_items = []
        points = selected_data.get('points')

        for point in points:
            item = point.get('pointIndex')
            if point.get('curveNumber') is 1:
                item += 12
            selected_items.append(item)

        return selected_items
