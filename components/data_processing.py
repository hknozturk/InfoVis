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

        self.state_names_populations_df = pd.read_csv(
            home_directory + 'state_names_population.csv', sep=';', index_col='Number')

        self.counties_names_df = pd.read_csv(
            home_directory + 'counties.csv', index_col='fips')
        self.counties_names_df.index = self.counties_names_df.index.map(
            "{:05}".format)
        # Warning accident_df has original copy of data don't change it
        # use filter_accident_df for showing and updating data.
        self.accident_df = self.read_data('ACCIDENT_n')
        self.filter_accident_df = self.accident_df

        # Warning person_df has original copy of data don't change it
        # use filter_person_df for showing and updating data.
        # self.person_df = self.read_data('PERSON')
        # self.filter_person_df = self.person_df

        # Warning vehicle_df has original copy of data don't change it
        # use filter_vehicle_df for showing and updating data.
        # self.vehicle_df = self.read_data('VEHICLE')
        # self.filter_vehicle_df = self.vehicle_df

        self.year_range = [2010, 2011, 2012,
                           2013, 2014, 2015, 2016, 2017, 2018]
        self.total_deaths = self.filter_accident_df.groupby(['STATE'])['FATALS'].sum()

    def get_states_data(self):
        """
        get the number of fatalities per state for all us states.
        """
        deaths = self.filter_accident_df.groupby(['STATE'])['FATALS'].sum()
        states_df = pd.concat([self.state_names_populations_df, deaths], axis=1)
        # total = self.accident_df.loc[(self.accident_df['YEAR'].isin(self.year_range))].groupby(['STATE'])['FATALS'].sum()
        # states_df['TOTAL_FATALS'] = total
        return states_df

    def get_selected_state_data(self, selected_states):
        """
        get the deaths per counties for selected_states.
        :param selected_states: List of integers of selected states.
        """
        filtered_df = self.filter_accident_df.loc[(
            self.filter_accident_df['STATE'].isin(selected_states))]
        filtered_df['STATE'] = filtered_df['STATE'].map("{:02}".format)
        filtered_df['COUNTY'] = filtered_df['COUNTY'].map("{:03}".format)
        filtered_df['fips'] = filtered_df['STATE'] + filtered_df['COUNTY']
        filtered_df.index = filtered_df['fips']
        counties_df = filtered_df.groupby(['STATE', 'COUNTY'])['FATALS'].sum()
        counties_df.index = counties_df.index.map('{0[0]}{0[1]}'.format)
        counties_df = pd.concat(
            [counties_df, self.counties_names_df], axis=1, join="inner")
        return counties_df

    def filter_data(self, selected_years, months, days, hours, f_values):
        """
        updating filter_accident_df with range in selected_years.
        :param selected_years: List of years range from range slider.
        :param months: List of month selected on month bar chart filter.
        :param days: List of days selected on day bar chart filter.
        :param hours: List of hours selected on hour bar chart filter.
        :param f_values: List of check boxes filter selected in filter checkboxes.
        """
        years_list = list(range(selected_years[0], selected_years[1] + 1))
        self.year_range = years_list
        self.filter_accident_df = self.accident_df.loc[(
            self.accident_df['YEAR'].isin(years_list))]
        # self.filter_person_df = self.person_df.loc[(
        #     self.person_df['YEAR'].isin(years_list))]
        # self.filter_vehicle_df = self.vehicle_df.loc[(
        #     self.vehicle_df['YEAR'].isin(years_list))]

        self.total_deaths = self.filter_accident_df.groupby(['STATE'])['FATALS'].sum()
        # bar chart filters
        if months:
            self.filter_accident_df = self.filter_columns(
                self.filter_accident_df, 'MONTH', months)
            # self.filter_person_df = self.filter_columns(
            #     self.filter_person_df, 'MONTH', months)
        if days:
            self.filter_accident_df = self.filter_columns(
                self.filter_accident_df, 'DAY_WEEK', days)
        if hours:
            self.filter_accident_df = self.filter_columns(self.filter_accident_df, 'HOUR', hours)

        # check box filters
        if 'DRUNK_DR' in f_values:
            self.filter_accident_df = self.filter_columns_on_condition(self.filter_accident_df, 'DRUNK_DR')
        if 'L_STATUS' in f_values:
            self.filter_accident_df = self.filter_columns_on_condition(self.filter_accident_df, 'L_STATUS')
        if 'SPEEDREL' in f_values:
            self.filter_accident_df = self.filter_columns_on_condition(self.filter_accident_df, 'SPEEDREL')
        if 'WRK_ZONE' in f_values:
            self.filter_accident_df = self.filter_columns_on_condition(self.filter_accident_df, 'WRK_ZONE')

    def get_years_timeline(self):
        """
        returning accident and fatals years timeline.
        """
        timeline_df = pd.DataFrame()
        timeline_df['ACCIDENT'] = self.filter_accident_df['YEAR'].value_counts()
        timeline_df['FATALS'] = self.filter_accident_df.groupby(['YEAR'])['FATALS'].sum()
        timeline_df['PERSONS'] = self.filter_accident_df.groupby('YEAR')['person_count'].sum()
        return timeline_df

    def filter_columns(self, df, column_name, values):
        return df.loc[(df[column_name].isin(values))]

    def filter_columns_on_condition(self, df, column_name):
        return df.loc[(df[column_name] > 0)]

    def get_sunburst_data(self):
        """
        group fatals by weather and then return mapped weather list as mentioned in weather_dict
        """
        weather_dict = {
            0: 'Clear', 1: 'Clear', 2: 'Rain', 3: 'Rain', 4: 'Snow', 5: 'Low visibility', 6: 'Other',
            7: 'Low visibility', 8: 'Other', 10: 'Other', 11: 'Low visibility', 12: 'Rain',
            98: 'Not reported', 99: 'Not reported'
        }
        harmful_event_dict = {
            1: 'Overturn', 8: 'Pedestrian', 9: 'Pedestrian', 10: 'Railway', 12: 'Motor Vehicle', 14: 'Motor Vehicle',
            54: 'Motor Vehicle', 55: 'Motor Vehicle', 16: 'Other Objects', 17: 'Other Objects', 18: 'Other Objects',
            43: 'Other Objects', 53: 'Other Objects', 59: 'Other Objects', 73: 'Other Objects', 21: 'Bridge',
            23: 'Bridge',
            24: 'Barrier', 25: 'Barrier', 26: 'Barrier', 30: 'Barrier', 31: 'Barrier', 32: 'Barrier', 33: 'Barrier',
            34: 'Barrier', 35: 'Barrier', 38: 'Barrier', 40: 'Barrier', 48: 'Barrier', 49: 'Barrier', 50: 'Barrier',
            51: 'Barrier', 52: 'Barrier', 57: 'Barrier', 41: 'Tree', 42: 'Tree', 91: 'Unknown', 98: 'Unknown',
            99: 'Unknown'
        }
        sun_burst_df = pd.DataFrame()
        sun_burst_df['FATALS'] = self.filter_accident_df['FATALS']
        sun_burst_df['WEATHER'] = self.filter_accident_df['WEATHER'].map(
            weather_dict)
        sun_burst_df['HARM_EV'] = self.filter_accident_df['HARM_EV'].map(
            harmful_event_dict)
        sun_burst_df['HARM_EV'] = sun_burst_df['HARM_EV'].fillna('Unknown')
        return sun_burst_df

    def get_accident_data_ordered_by_states(self, sort_by):
        """
        returns ordered filter_accident_df to populate list_items (list component)
        """
        states = self.state_names_populations_df.copy()
        grouped_states = self.filter_accident_df.groupby(['STATE'])
        population_sums = states[map(str, self.year_range)].sum(axis=1)
        states['NumberOfAccidents'] = grouped_states.size()
        states['AccidentsPerMil'] = round(grouped_states.size() * 1000000 / \
                                    population_sums, 2)
        states['NumberOfDeaths'] = grouped_states['FATALS'].sum()
        states['DeathsPerMil'] = round(grouped_states['FATALS'].sum() * 1000000 / \
                                 population_sums, 2)
        states['AvgArrivalTime'] = round(grouped_states['RESPONSE_TIME'].mean(), 2)
        states['AvgHospitalArrivalTime'] = round(grouped_states['HOSP_ARR_TIME'].mean(), 2)
        states['Total_deaths'] = self.total_deaths
        states['Percentage'] = round((states['NumberOfDeaths']/states['Total_deaths'])*100, 2)
        states.fillna(0, inplace=True)
        if sort_by:
            return states.sort_values(by=[sort_by], ascending=False)
        return states

    def get_data_grouped_by_times(self, group_by_value):
        grouped_data = self.filter_accident_df.groupby([group_by_value])

        if group_by_value == 'HOUR':
            return grouped_data['FATALS'].sum().drop([99])
        else:
            return grouped_data['FATALS'].sum()

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
            temp_df = pd.read_csv(path)
            a_df = a_df.append(temp_df, ignore_index=True)
        return a_df

    # method to add columns from person and vehicle file to accident
    @staticmethod
    def update_accident(years=[2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]):
        for year in years:
            path = home_directory + str(year) + "/" + 'ACCIDENT_n' + ".CSV"
            a_df = pd.read_csv(path, encoding='iso-8859-1', index_col='ST_CASE')
            path = home_directory + str(year) + "/" + 'PERSON' + ".CSV"
            p_df = pd.read_csv(path, encoding='iso-8859-1')
            path = home_directory + str(year) + "/" + 'VEHICLE' + ".CSV"
            v_df = pd.read_csv(path, encoding='iso-8859-1')

            # adding total person count in accident
            p_df['person_count'] = 1
            p_count = p_df.groupby(['ST_CASE'])['person_count'].sum()
            a_df['person_count'] = p_count

            speeding = v_df.query('SPEEDREL > 0 and SPEEDREL < 8').groupby('ST_CASE')['SPEEDREL'].count()
            a_df['SPEEDREL'] = speeding

            licence = v_df.query('L_STATUS != 6').groupby('ST_CASE')['L_STATUS'].count()
            a_df['L_STATUS'] = licence
            path = home_directory + str(year) + "/" + 'ACCIDENT_n' + ".CSV"
            a_df.to_csv(path)
            #
            print(a_df.shape)

    @staticmethod
    def remove_extra_column(years=[2010]):
        for year in years:
            path = home_directory + str(year) + "/" + 'ACCIDENT_n' + ".CSV"
            a_df = pd.read_csv(path, encoding='iso-8859-1', index_col='ST_CASE')
            a_df.drop(['Unnamed: 0', 'VE_TOTAL', 'VE_FORMS',
                       #'PVH_INVL', 'PEDS', 'PERNOTMVIT', 'PERMVIT',
                       'PERSONS', 'CITY', 'DAY', 'MINUTE', 'NHS',
                       #'RUR_URB', 'FUNC_SYS', 'RD_OWNER',
                       'ROUTE', 'TWAY_ID', 'TWAY_ID2', 'MILEPT', 'LATITUDE', 'LONGITUD', 'SP_JUR', 'MAN_COLL', 'RELJCT1',
                       'RELJCT2', 'TYP_INT', 'REL_ROAD', 'LGT_COND', 'WEATHER1', 'WEATHER2', 'SCH_BUS', 'RAIL', 'NOT_HOUR',
                       'NOT_MIN', 'ARR_HOUR', 'ARR_MIN', 'HOSP_HR', 'HOSP_MN', 'CF1', 'CF2', 'CF3'], axis=1, inplace=True)
            a_df.to_csv(path)
            print(a_df.shape)

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

    # def calculate_arrival_times(self):
    #     """
    #     this static method calculates average arrival times of EMP to scene and to hospital.
    #     :param hour: dataframe that grouped by states.
    #     """
    #     hour_range = range(0, 23)
    #     min_range = range(0, 59)

    #     filter_times = dataFrame[(dataFrame['NOT_MIN'].isin(min_range)) &
    #                              (dataFrame['NOT_HOUR'].isin(hour_range)) &
    #                              (dataFrame['ARR_MIN'].isin(min_range)) &
    #                              (dataFrame['ARR_HOUR'].isin(hour_range))
    #                              ]

    #     filter_times.loc[(filter_times['NOT_HOUR'] >
    #                       filter_times['ARR_HOUR']), 'ARR_HOUR'] = 24

    #     filter_times['AVG_ARR_TIME'] = (
    #         filter_times['ARR_HOUR'] - filter_times['NOT_HOUR']) * 60 + (filter_times['ARR_MIN'] - filter_times['NOT_MIN'])

    #     grouped_by_states = self.filter_accident_df.groupby(['STATE'])['RESPONSE_TIME'].mean()
    #     return grouped_by_states['AVG_ARR_TIME'].mean()
