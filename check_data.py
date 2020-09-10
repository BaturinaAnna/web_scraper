"""Module for checking data about dates and cities for flight"""
from datetime import datetime
from collections import namedtuple
from get_available_cities_and_dates import get_lists_of_available_cities, \
    get_lists_of_available_dates


def check_number_of_cities(iata_codes):
    """Check if the number of cities is two and the cities are not the same"""
    if len(iata_codes) == 2:
        if iata_codes[0] == iata_codes[1]:
            print('You entered the same cities')
            return False
        return True
    print('You entered the wrong number of cities')
    return False


def check_cities_available_to_flight(city_from, city_to):
    """Check if the cities are available for flight"""
    flag_from = False
    flag_to = False
    available_cities_from = get_lists_of_available_cities('from')
    available_cities_to = get_lists_of_available_cities('to')
    for city in available_cities_from:
        if city_from == city:
            flag_from = True
            break
    for city in available_cities_to:
        if city_to == city:
            flag_to = True
            break
    if not flag_from:
        print('There is no flights from the departure city')
        return False
    if not flag_to:
        print('There is no flights to the arrival city')
        return False
    return True


def check_year_month(date, direction):
    """Check if the date is available for flight"""
    available_ym = get_lists_of_available_dates(direction)
    for year_month in available_ym:
        if year_month == datetime.strftime(date, '%Y-%m'):
            return True
    print('The year or month of {} are not available for flight'.format(direction))
    return False

def check_date(dates_for_check):
    """Checks if the date exists and makes datetime object"""
    dates = []
    for date_for_check in dates_for_check:
        try:
            date = datetime.strptime(date_for_check, '%Y-%m %d')
        except ValueError:
            print('You entered a nonexistent date')
            return False
        dates.append(date)
    return dates

def make_tuple(data, flights):
    """Makes namedtuple ((city_from, city_to), (first_flight second_flight))"""
    data_tuple = namedtuple('data_tuple', 'cities dates')
    cities_tuple = namedtuple('cities_tuple', 'city_from city_to')
    if flights == 1:
        dates_tuple = namedtuple('dates_tuple', 'first_flight')
    elif flights == 2:
        dates_tuple = namedtuple('dates_tuple', 'first_flight second_flight')
    dates = check_date(data[1])
    if dates is not False:
        if check_number_of_cities(data[0]):
            return data_tuple(cities_tuple(*data[0]), dates_tuple(*dates))
        return False
    return False


def check_data(data_to_check):
    """Checking the whole data about dates and cities for flight"""
    if len(data_to_check[1]) == 1:
        data = make_tuple(data_to_check, 1)
        if data is not False and check_year_month(data.dates.first_flight, 'depart'):
            if check_cities_available_to_flight(data.cities.city_from, data.cities.city_to):
                return data
        return False
    if len(data_to_check[1]) == 2:
        data = make_tuple(data_to_check, 2)
        if data is not False and check_year_month(data.dates.first_flight, 'depart') and\
                    check_year_month(data.dates.second_flight, 'return'):
            if check_cities_available_to_flight(data.cities.city_from, data.cities.city_to) and\
                    check_cities_available_to_flight(data.cities.city_to, data.cities.city_from):
                return data
        return False
    print('You entered the wrong number of dates')
    return False
