import dash_html_components as html
from components.list_item import ListItem


class List:
    def __init__(self, data_processing):
        self.listItem = ListItem(data_processing)

    def generateList(self):
        listItems = self.listItem.generateItems()

        return html.Ul(listItems)
