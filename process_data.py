"""Module for functions, that get required parameters from entered string and
asks the user to enter the parameters in right format while it is necessary"""
import re
from check_data import check_data


def get_data_from_string(data):
    """Get IATA-codes and dates from string"""
    data = data.upper()
    iata_codes = re.findall(r'[a-zA-Z]{3}', data)
    dates = re.findall(r'\d{4}\-\d{2} \d{2}', data)
    return iata_codes, dates


def get_satisfying_data():
    """Get string with parameters in right format"""
    data = str(input())
    data_to_check = get_data_from_string(data)
    def question():
        print('Do you want to try to enter again? yes/no')
        answer = str(input())
        if answer == 'yes':
            return get_satisfying_data()
        if answer == 'no':
            return False
        print('Please, follow the instructions')
        return question()
    processed_data = check_data(data_to_check)
    if processed_data is not False:
        return processed_data
    return question()
