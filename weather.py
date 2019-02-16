import pandas as pd
import requests
import cache
import csv

# Some global variables that should not be altered in the code, but can be altered here
API_ENDPOINT = "http://api.worldweatheronline.com/premium/v1/past-weather.ashx"
API_KEY = "f46e6eab67824a55a1441132180912"


#### FUNCTIONS FOR WORKING WITH WEATHER API ####
# this is the 'scary' function, it will run through every day of the month in given years
# to get daily weather from weather API, then will return data as a list of dictionaries
column_names = ["date","maxtempC","mintempC","precipMM","humidity","cloudcover","city"]

def get_weather_data(location,years,months,column_names=column_names):
    list_of_days = []
    for year in years:
        for month in months:
            data_month = weather_request_24hr(location, month, year)
            city = data_month['data']['request'][0]['query']
            for day in data_month['data']['weather']:
                data = [day['date'],day['maxtempC'],day['mintempC'],day['hourly'][0]['precipMM'],day['hourly'][0]['humidity'],day['hourly'][0]['cloudcover'],city.replace(',','-')]
                dict_row = dict(zip(column_names,data))
                list_of_days.append(dict_row)
    return list_of_days

    

# takes list of [days] (given by get_weather_data() functions)
# and outputs them to a csv file
def dump_to_csv(csv_name, days, column_names=column_names):       
    with open(csv_name, 'w') as new_file:
        writer = csv.DictWriter(new_file, fieldnames=column_names)
        writer.writeheader()
        
        for row in days:
            writer.writerow(row)


# This function will get daily report for a given month
# returns a json list of dictionaries (days and their weither)
def weather_request_24hr(location, month, year):
    '''
    This function fetches the data for a 24 hr interval for a given city
    that is between the two given dates.
    
    DATE
    If you wish to retrieve weather between two dates, 
    use this  parameter to specify the ending date.
    Important: the enddate parameter must have the same month 
    and year as the date parameter.
        yyyy-MM-dd (Example: 2009-07-20 for 20 July 2009.)
        
    LOCATION
    City Name, State (US only)
    City Name, Country
        q=London,united+kingdom
    '''
    year = str(year)
    date    = year+'-'+month[0]
    enddate = year+'-'+month[1]
    
    
    params = {
        'q': location,
        'date': date,
        'enddate': enddate,
        'tp': 24,
        'key': API_KEY,
        'format': 'json'
    }
    json_obj = cache.cached_reqest(baseurl=API_ENDPOINT,params=params)    
    return json_obj
