import pandas as pd
import json
from urllib.request import urlopen

# reading config json file.
with open('config.json', 'r') as f:
    config_path = json.load(f)
    home_directory = config_path['home_directory']


class DataProcessing:
    """
    DataProcessing class is responsible for all data pre processing related tasks.
    """

    def __init__(self):
        """
        all files read in constructor once and then used in other methods to avoid multiple reads.
        """
        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            self.geojson = json.load(response)

        self.state_names_df = self.states = pd.read_csv(home_directory + 'state_names.csv', sep=';')
        self.accident_df = pd.read_csv(home_directory + "FARS/National/FARS2018NationalCSV/ACCIDENT.csv")

    def get_states_data(self):
        """
        get the number of fatalities per state for all us states.
        """
        deaths = self.accident_df.groupby(['STATE'])['FATALS'].sum()
        d = self.state_names_df.set_index('Number')['Code'].to_dict()
        deaths.index = deaths.index.map(d)
        return deaths

    def get_selected_state_data(self, selected_states):
        """
        get the deaths per counties for selected_states.
        :param selected_states: List of integers of selected states.
        """

        filtered_df = self.accident_df.loc[(self.accident_df['STATE'].isin(selected_states))]
        filtered_df['STATE'] = filtered_df['STATE'].map("{:02}".format)
        filtered_df['COUNTY'] = filtered_df['COUNTY'].map("{:03}".format)
        return filtered_df
