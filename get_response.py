"""Module to get response from website"""
from collections import namedtuple
from datetime import datetime
import requests
from lxml import html


def set_params(data, params):
    """Set right parameters for request"""
    params['DC'] = data.cities.city_from
    params['AC'] = data.cities.city_to
    params['AM'] = datetime.strftime(data.dates.first_flight, '%Y-%m')
    params['AD'] = datetime.strftime(data.dates.first_flight, '%d')
    if len(data.dates) == 1:
        params['TT'] = 'OW'
    if len(data.dates) == 2:
        params['TT'] = 'RT'
        params['RM'] = datetime.strftime(data.dates.second_flight, '%Y-%m')
        params['RD'] = datetime.strftime(data.dates.second_flight, '%d')
    return params


def get_response(data):
    """Make request to the website"""
    url = 'https://www.airblue.com/bookings/flight_selection.aspx'
    headers = {'Pragma': 'no-cache',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64;'
                             ' Trident/7.0; tv:11.0) like Gecko',
               'Content-length': '0',
               'Connection': 'Keep-Alive',
               'Host': 'www.airblue.com'}
    parameters = {'TT': '',  # type of trip
                  'DC': '',  # departure city
                  'AC': '',  # arrival city
                  'AM': '',  # arrival yyyy-mm
                  'AD': '',  # arrival dd
                  'RM': '',  # returning yyyy-mm
                  'RD': '',  # returning dd
                  'FI': 'on',  # fixed dates
                  'CC': '',  # class --- '' - All Cabins
                  'PA': '1',  # number of adults
                  'PC': '',  # number of children
                  'PI': ''}  # number of infants
    parameters = set_params(data, parameters)
    response = requests.get(url, params=parameters, headers=headers)
    if response.status_code == 200:
        tree = html.fromstring(response.text)
        return tree
    return None


def check_errors(tree):
    """Check that there are available flights"""
    if tree is None:
        return False
    if len(tree.xpath('/html/body/div/div/form')) == 1:
        print('Flights are not available on the dates selected')
        return False
    return True

def check_availability_flights(tree):
    """Check that there are available flights"""
    for tr_var in tree.xpath('//form[@class="search_results "]//tbody/tr'):
        if tr_var.get('class') == 'no_flights_found':
            print('Flights are not available on the dates selected')
            return False
    return True

def get_flights(data, tree):
    """Get data about available flights"""
    summary_result = []
    for i, date in enumerate(data.dates):
        resulted_flights = []
        number_of_trip = str(i + 1)
        path = '//div/table[@id="trip_{}_date_{}_{}_{}"]'.format(number_of_trip,
                                                                 datetime.strftime(date, '%Y'),
                                                                 datetime.strftime(date, '%m'),
                                                                 datetime.strftime(date, '%d'))
        number_of_results = len(tree.xpath('{}/tbody'.format(path)))
        flight = namedtuple('flight', 'depart_time arrive_time stops price date flight_class')
        date_of_arrive = tree.xpath('{}/caption/text()'.format(path))[0].strip()
        class_of_cabin = tree.xpath('{}//label/strong/text()'.format(path))[0]
        for j in range(1, number_of_results + 1):
            flight_variant = flight(
                tree.xpath('{}/tbody[{}]'
                           '//td[@class="time leaving"]/text()'.format(path, str(j)))[0],
                tree.xpath('{}/tbody[{}]'
                           '//td[@class="time landing"]/text()'.format(path, str(j)))[0],
                tree.xpath('{}/tbody[{}]'
                           '//td[@class="route"]/span/text()'.format(path, str(j)))[0],
                tree.xpath(
                    '{}//tbody[{}]//label'
                    .format(
                        path, str(j)))[0].get('data-title').replace('All Travellers:', '').strip(),
                date_of_arrive,
                class_of_cabin)
            resulted_flights.append(flight_variant)
        summary_result.append(resulted_flights)
    return summary_result

def get_data_about_flights(data):
    """Unites functions of the module"""
    tree = get_response(data)
    if check_errors(tree) and check_availability_flights(tree):
        result = get_flights(data, tree)
        return result
    return False
