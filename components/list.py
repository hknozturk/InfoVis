import dash_html_components as html
from components.list_item import ListItem


class List:
    def __init__(self):
        self.listItem = ListItem()
        self.generateList()

    def generateList(self):
        listItems = self.listItem.generateItems()

        return html.Ul(listItems)
