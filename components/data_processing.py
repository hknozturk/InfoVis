import pandas as pd
import json
from urllib.request import urlopen
import numpy as np

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
        self.accident_df = self.read_data('ACCIDENT_n')
        self.filter_accident_df = self.accident_df

        # Warning person_df has original copy of data don't change it
        # use filter_person_df for showing and updating data.
        self.person_df = self.read_data('PERSON')
        self.filter_person_df = self.person_df

        # Warning vehicle_df has original copy of data don't change it
        # use filter_vehicle_df for showing and updating data.
        self.vehicle_df = self.read_data('VEHICLE')
        self.filter_vehicle_df = self.vehicle_df

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
        self.filter_person_df = self.person_df.loc[(
            self.person_df['YEAR'].isin(years_list))]
        self.filter_vehicle_df = self.vehicle_df.loc[(
            self.vehicle_df['YEAR'].isin(years_list))]

    def get_years_timeline(self):
        """
        returning accident and fatals years timeline.
        """
        timeline_df = pd.DataFrame()
        timeline_df['ACCIDENT'] = self.filter_accident_df['YEAR'].value_counts()
        timeline_df['FATALS'] = self.filter_accident_df.groupby(['YEAR'])[
            'FATALS'].sum()
        timeline_df['PERSONS'] = self.filter_person_df['YEAR'].value_counts()
        return timeline_df

    # def get_weather_info(self):
    #     weather_df = self.filter_accident_df['']
    #     return weather_df

    def get_accident_data_ordered_by_states(self):
        """
        returns ordered filter_accident_df to populate list_items (list component)
        """
        states = self.state_names_df.copy().set_index(['Number'])
        grouped_states = self.filter_accident_df.groupby(['STATE'])
        states['NumberOfAccidents'] = grouped_states.size()
        states['NumberOfDeaths'] = grouped_states['FATALS'].sum()
        states['AvgArrivalTime'] = grouped_states['RESPONSE_TIME'].mean()
        states['AvgHospitalArrivalTime'] = grouped_states['HOSP_ARR_TIME'].mean()
        states.fillna(0, inplace=True)

        return states.sort_values(by=['NumberOfDeaths'], ascending=False)

    def calculate_arrival_times(self):
        """
        this static method calculates average arrival times of EMP to scene and to hospital.
        :param hour: dataframe that grouped by states.
        """
        # hour_range = range(0, 23)
        # min_range = range(0, 59)
        #
        # filter_times = dataFrame[(dataFrame['NOT_MIN'].isin(min_range)) &
        #                          (dataFrame['NOT_HOUR'].isin(hour_range)) &
        #                          (dataFrame['ARR_MIN'].isin(min_range)) &
        #                          (dataFrame['ARR_HOUR'].isin(hour_range))
        #                          ]
        #
        # filter_times.loc[(filter_times['NOT_HOUR'] >
        #                   filter_times['ARR_HOUR']), 'ARR_HOUR'] = 24
        #
        # filter_times['AVG_ARR_TIME'] = (
        #     filter_times['ARR_HOUR'] - filter_times['NOT_HOUR']) * 60 + (filter_times['ARR_MIN'] - filter_times['NOT_MIN'])

        # grouped_by_states = self.filter_accident_df.groupby(['STATE'])['RESPONSE_TIME'].mean()
        # return grouped_by_states['AVG_ARR_TIME'].mean()

    @staticmethod
    def read_data(file_name, years=[2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]):
        """
        reading data from local storage for years in years list.
        :param years: List of years to read from local file system.
        :param file_name: String of the file to read from local storage.
        """
        a_df = pd.DataFrame()
        for year in years:
            path = home_directory + str(year) + "/" + file_name + ".CSV"
            temp_df = pd.read_csv(path, encoding='iso-8859-1')
            if 'YEAR' not in temp_df.columns:
                temp_df['YEAR'] = year
            a_df = a_df.append(temp_df, ignore_index=True)
        return a_df

    @staticmethod
    def calculate_response_times(dataFrame, file_name, year):
        """
        this static method calculates average arrival times of EMP to scene and to hospital.
        :param hour: dataframe that grouped by states.
        """
        dataFrame['RESPONSE_TIME'] = 0
        hour_range = range(0, 23)
        min_range = range(0, 59)

        filter_times = dataFrame[(dataFrame['NOT_MIN'].isin(min_range)) &
                                 (dataFrame['NOT_HOUR'].isin(hour_range)) &
                                 (dataFrame['ARR_MIN'].isin(min_range)) &
                                 (dataFrame['ARR_HOUR'].isin(hour_range))
                                 ]

        filter_times.loc[(filter_times['NOT_HOUR'] >
                          filter_times['ARR_HOUR']), 'ARR_HOUR'] = 24

        filter_times['RESPONSE_TIME'] = (filter_times['ARR_HOUR'] - filter_times['NOT_HOUR']) * 60 + (
            filter_times['ARR_MIN'] - filter_times['NOT_MIN'])

        dataFrame['RESPONSE_TIME'] = filter_times['RESPONSE_TIME']
        path = home_directory + str(year) + "/" + file_name + "_n.CSV"
        dataFrame.to_csv(path)

    @staticmethod
    def calculate_hospital_arrival_times(dataFrame, file_name, year):
        """
        this static method calculates time taken to arrive hospital from accident scene.
        It is a separate method from calculate_response_times because, not recorded times for notification and hospital arrival might affect each other.
        """
        dataFrame['HOSP_ARR_TIME'] = 0
        hour_range = range(0, 23)
        min_range = range(0, 59)

        filter_times = dataFrame[
            (dataFrame['ARR_MIN'].isin(min_range)) &
            (dataFrame['ARR_HOUR'].isin(hour_range)) &
            (dataFrame['HOSP_MN'].isin(min_range)) &
            (dataFrame['HOSP_HR'].isin(hour_range))
        ]

        filter_times.loc[(filter_times['ARR_HOUR'] >
                          filter_times['HOSP_HR']), 'HOSP_HR'] = 24

        filter_times['HOSP_ARR_TIME'] = (filter_times['HOSP_HR'] - filter_times['ARR_HOUR']) * 60 + (
            filter_times['HOSP_MN'] - filter_times['ARR_MIN'])

        dataFrame['HOSP_ARR_TIME'] = filter_times['HOSP_ARR_TIME']
        path = home_directory + str(year) + "/" + file_name + "_n.CSV"
        dataFrame.to_csv(path)
