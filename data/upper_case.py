import os

def upper_case_file_names(years=[2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010]):
        """
        reading local data in years list
        :param years: List of years to read from local file system.
        """
        for year in years:
        	for file in os.listdir('./' + str(year)):
        		name, ext = os.path.splitext(file)
        		os.rename(os.path.join('./' + str(year), file), os.path.join('./' + str(year), name.upper() + ext.upper()))


if __name__ == '__main__':
	upper_case_file_names()