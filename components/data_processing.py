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

        self.state_names_df = self.states = pd.read_csv(
            home_directory + 'state_names.csv', sep=';')

        # Warning accident_df has original copy of data don't change it
        # use filter_accident_df for showing and updating data.
        self.accident_df = self.read_accident_data()
        self.filter_accident_df = self.accident_df

    def get_states_data(self):
        """
        get the number of fatalities per state for all us states.
        """
        deaths = self.filter_accident_df.groupby(['STATE'])['FATALS'].sum()
        d = self.state_names_df.set_index('Number')['Code'].to_dict()
        deaths.index = deaths.index.map(d)
        return deaths

    def get_selected_state_data(self, selected_states):
        """
        get the deaths per counties for selected_states.
        :param selected_states: List of integers of selected states.
        """

        filtered_df = self.filter_accident_df.loc[(
            self.filter_accident_df['STATE'].isin(selected_states))]
        filtered_df['STATE'] = filtered_df['STATE'].map("{:02}".format)
        filtered_df['COUNTY'] = filtered_df['COUNTY'].map("{:03}".format)
        return filtered_df

    def filter_data(self, selected_years):
        """
        updating filter_accident_df with range in selected_years.
        :param selected_years: List of years range from range slider.
        """
        years_list = list(range(selected_years[0], selected_years[1] + 1))
        self.filter_accident_df = self.accident_df.loc[(
            self.accident_df['YEAR'].isin(years_list))]

    def get_years_timeline(self):
        """
        returning accident and fatals years timeline.
        """
        timeline_df = pd.DataFrame()
        timeline_df['ACCIDENT'] = self.filter_accident_df['YEAR'].value_counts()
        timeline_df['FATALS'] = self.filter_accident_df.groupby(['YEAR'])['FATALS'].sum()
        return timeline_df

    @staticmethod
    def read_accident_data(years=[2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]):
        """
        reading local data in years list
        :param years: List of years to read from local file system.
        """
        a_df = pd.DataFrame()
        for year in years:
            path = home_directory + str(year) + "/ACCIDENT.CSV"
            temp_df = pd.read_csv(path)
            a_df = a_df.append(temp_df, ignore_index=True)
        return a_df
