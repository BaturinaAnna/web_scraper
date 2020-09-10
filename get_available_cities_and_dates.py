"""Module to get cities and dates that are available for flight"""
import requests
from lxml import html

URL = 'https://www.airblue.com/'

HEADERS = {'Pragma': 'no-cache',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; tv:11.0) like Gecko',
           'Content-length': '0',
           'Connection': 'Keep-Alive',
           'Host': 'www.airblue.com'}

TREE = html.fromstring(requests.get(URL, headers=HEADERS, params=None).text)

def get_lists_of_available_cities(direction):
    """get list of cities from website that available for flight in to- or from- direction"""
    available_cities = []
    directions = {'from': 1, 'to': 2}
    option_cities = TREE.xpath(
        '//form[@method="get"]'
        '/span[@class="fieldset cities"]/select[{}]/option'.format(directions[direction]))
    for city in option_cities:
        available_cities.append(city.get('value'))
    return available_cities

def get_lists_of_available_dates(direction):
    """get list of dates from website that available for returning"""
    available_dates = []
    option_dates = TREE.xpath(
        '//div[@class="fieldset dates"]/div[@class="{}"]/select/option'.format(direction))
    for date in option_dates:
        value = date.get('value')
        if value is not None:
            available_dates.append(value)
    return available_dates
