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
