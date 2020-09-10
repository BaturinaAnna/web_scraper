"""Module for making a sting-answer from the data"""
from itertools import product
from process_flights import get_price


def sort_by_price(data):
    """Sorts list by the price of the tickets"""
    data[0].sort(key=lambda i: float(i.price.replace(',', '.')))
    return data


def make_to_string(data):
    """Makes a sting-answer from the data"""
    data = sort_by_price(data)
    sum_results = []
    for res in data:
        results = []
        for result in res:
            results.append('Date: {}. Departs in {}, Arrives in {}. '
                           'Duration of flight = {}, {}. '
                           'Price: {} in {}. Class: {}'.format(result.date,
                                                               result.depart_time,
                                                               result.arrive_time,
                                                               result.duration,
                                                               result.stops,
                                                               result.price,
                                                               result.value,
                                                               result.fl_class))
        sum_results.append(results)
    return sum_results


def combine_results(data):
    """Combines results to get all variants of round trip"""
    list_of_combinations = list(product(data[0], data[1]))
    return list_of_combinations


def get_total_price(combination):
    """Counts a total price of two flights in combination"""
    return float(get_price(combination[0]).replace(',', '.')) +\
           float(get_price(combination[1]).replace(',', '.'))
