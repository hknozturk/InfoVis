import dash_daq as daq
import dash_html_components as html


class SwitchToggle:
    def __init__(self):
        self.darkMode = False

    def generateToggle(self):
        return html.Div([
            daq.BooleanSwitch(id='dark-mode-toggle', on=self.darkMode,
                                 label=['Light', 'Dark'], color="#9B51E0", className="dark-mode-toggle")
        ])

    def updateLayoutStyle(self, darkMode):
        if darkMode:
            return {'background-color': 'rgb(51, 51, 51)'}
        else:
            return {'background-color': 'rgb(199, 199, 199)'}

    def updateCardStyle(self, darkMode):
        if darkMode:
            return [{'background-color': 'rgb(34, 34, 34)', 'color': 'rgb(199, 189, 189)'} for i in range(5)]
        else:
            return [{'background-color': 'rgb(255, 255, 255)', 'color': 'rgb(24, 24, 24)'} for i in range(5)]
