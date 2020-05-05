import dash_html_components as html


class ListItem:
    def __init__(self):
        self.generateItems()

    def generateItems(self):
        self.list = []
        for n in range(20):
            self.list.append(html.Li([n]))

        return self.list
