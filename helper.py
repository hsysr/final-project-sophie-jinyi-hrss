from datetime import datetime
import base64


def type_check(value, types):
    """Check whether the input value is of certain types

    This function checks the type of the input value. If
    the type of the input value matches any type in the
    types list, the function returns True, otherwise it
    returns False

    :param value: the input
    :param types: list of types containing the matching types

    :returns: Boolean containing whether the input matches types
    """
    for ty in types:
        if isinstance(value, ty):
            return True
    return False


def validate_input_dict(input_dict, validation_dict):
    """Check whether the input dictionary match the validation
    dictionary

    This function checks if the dictionary has all the keys
    in the validation dictionary. If any key is missing, it
    returns False. It then checkes if the type of value of each
    key matches the types in validation dictionary. If all the value
    types matches, the function returns True. Otherwise it returns
    False

    :param input_dict: dictionry containing input data
    :param validation_dict: dictionry containing required keys
                            and correspoding value types

    :returns: Boolean containing whether the input dictionary is valid
    """
    for key in validation_dict.keys():
        if key in input_dict:
            if not type_check(input_dict[key], validation_dict[key]):
                return False
        else:
            return False
    return True


def num_parse(input_str):
    """Parse the input string into an integer

    This function tries to cast the input string into an integer.
    If the string does not represent a valid integer, the function
    will return None

    :param input_str: string containing the input

    :returns: int containing the correspoding integer if the
              string is valid, None otherwise
    """
    try:
        num = int(input_str)
    except ValueError:
        return None
    else:
        return num


def timestamp_format(timestamp):
    """Format the timestamp to format of '%Y-%m-%d %H:%M:%S'

    This function tries to cast the input string datetime object into a string.
    A return should be in format as shown by the example "2018-03-09 11:00:36".

    :param timestamp: datetime containing the correspoding timestamp

    :returns: timestamp_string: string containing the datatime with the
              format of '%Y-%m-%d %H:%M:%S'
    """
    timestamp_string = datetime.strftime(timestamp, '%Y-%m-%d %H:%M:%S')
    return timestamp_string


def image2b64(filename):
    """Convert image to base64 string

    This function tries to open an image file, and encode the image file into
    a base 64 string.

    :param filename: str containing the input filepath

    :returns: string containing the encoded image as a base64 string
    """
    with open(filename, "rb") as image_file:
        b64_bytes = base64.b64encode(image_file.read())
    b64_string = str(b64_bytes, encoding='utf-8')
    return b64_string
