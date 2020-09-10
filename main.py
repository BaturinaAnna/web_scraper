"""Module for the main function of programm"""
from process_data import get_satisfying_data
from get_response import get_data_about_flights
from process_flights import process_flights
from improve_results import make_to_string, combine_results, get_total_price


def show_available_tickets():
    """The main function, calls additional functions"""
    print('Enter the names of cities and dates of flights in a string format: \n'
          'FFF TTT yyyy-mm dd yyyy-mm dd\n'
          'where FFF - IATA-code of city of departure\n'
          '      TTT - IATA-code of city of arriving\n'
          '      yyyy-mm dd - the date of departure and arrival (the second is up to your need)')
    data = get_satisfying_data()
    if data:
        flights = get_data_about_flights(data)
        if flights:
            processed_flights = process_flights(flights)
            result_in_string = make_to_string(processed_flights)
            print('RESULTS:')
            if len(processed_flights) == 1:
                for result in result_in_string[0]:
                    print(result)
            elif len(processed_flights) == 2:
                combinations = combine_results(result_in_string)
                for combination in combinations:
                    print(combination[0])
                    print(combination[1])
                    print('The total cost of round-trip flight:'
                          ' {0:.3f} \n'.format(get_total_price(combination)))

show_available_tickets()
