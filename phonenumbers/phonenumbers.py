import re
import logging


# phone number regex extraction
phonePattern = re.compile(r'''
(\d{3})    # area code is 3 digits (e.g. '800')
(\d{3})    # trunk is 3 digits (e.g. '555')
(\d{4})    # rest of number is 4 digits (e.g. '1212')
(\d*)      # extension is optional and can be any number of digits
$          # end of string
''', re.VERBOSE)


def get_numbers_from_file(file='code_challenge_data_1.txt'):
    """
    Open file a readonly and return a list of strings
    :param file:
    :return:
    """
    try:
        phone_numbers = open(file, 'r').readlines()
    except FileExistsError:
        logging.error(f'File {file} does not exist.')
    return phone_numbers


def parse_phone_numbers(phone_numbers):
    """
    1. get  numbers only from string
    2. check if there's country code
    3. search for area code, phone num, and extension
    4. return the list of parse numbers
    :param phone_numbers:
    :return:
    """
    phonenum_list = []
    for number in phone_numbers:
        # Country Code is defaulted to US(1)
        phone_info = {'Area Code': '', 'Country Code': 1, 'Phone Number': '', 'Extension': ''}
        num_only = re.findall('[0-9]+', number)  # get numbers only
        if len(num_only[0]) <= 3 and len(num_only) > 3:  # check if the first set for country code
            num_info = phonePattern.search(''.join(num_only[1:])).groups()
            phone_info['Country Code'] = num_only[0]
        else:
            num_info = phonePattern.search(''.join(num_only)).groups()
        phone_info['Area Code'] = num_info[0]
        phone_info['Phone Number'] = '-'.join(num_info[1:3])
        phone_info['Extension'] = num_info[3]
        phonenum_list.append(phone_info)
    return phonenum_list


def get_phone_numbers():
    """
    Read file and return parse numbers
    :return:
    """
    phone_numbers = get_numbers_from_file()
    num_list = parse_phone_numbers(phone_numbers)
    return num_list
