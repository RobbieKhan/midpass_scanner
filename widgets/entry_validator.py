def validator_int(user_input, new_value):
    del new_value
    try:
        if len(user_input) >= 1 and user_input != '-' and user_input is not None:
            _user_input = int(user_input)
    except ValueError:
        return False
    return True


def validator_float(user_input, new_value):
    del new_value
    try:
        if len(user_input) >= 1 and user_input != '-' and user_input is not None:
            _user_input = float(user_input)
    except ValueError:
        return False
    return True


def validator_uint(user_input, new_value):
    if new_value == '-':
        return False
    try:
        if len(user_input) >= 1 and user_input is not None:
            _user_input = int(user_input)
    except ValueError:
        return False
    return True
