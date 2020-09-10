"""Module to processing data about flights"""
import re
from collections import namedtuple
from datetime import datetime, timedelta


def flight_duration(time_start, time_finish):
    """Returns the duration of flight"""
    datetime_start = datetime.strptime(time_start, '%I:%M %p')
    datetime_finish = datetime.strptime(time_finish, '%I:%M %p')
    if datetime_start < datetime_finish:
        return datetime_finish - datetime_start
    return datetime_finish - datetime_start + timedelta(days=1)


def get_value(string):
    """Get the value of the price of the flight"""
    return re.findall(r'[a-zA-Z]{3} ', string)[0]


def get_price(string):
    """Get the price of the flight"""
    return re.findall(r'\d{1,4}\,\d{3}', string)[0]


def process_flights(data):
    """Processing data about flights"""
    summary_results = []
    for flight_way in data:
        results = []
        info = namedtuple('info', 'date depart_time arrive_time'
                                  ' duration stops price value fl_class')
        for flight in flight_way:
            flight_info = info(flight.date,
                               flight.depart_time,
                               flight.arrive_time,
                               flight_duration(flight.depart_time, flight.arrive_time),
                               flight.stops,
                               get_price(flight.price),
                               get_value(flight.price),
                               flight.flight_class)
            results.append(flight_info)
        summary_results.append(results)
    return summary_results
