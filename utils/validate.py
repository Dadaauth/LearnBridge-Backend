


def validate_input(input):
    """
    Validate the input
    """
    if not input:
        return False
    return True

def validate_fields(required: set, given: dict) -> bool:
    """
    Validate the fields of a dictionary
    """
    for key in required:
        if key not in given.keys():
            return False
        else:
            if not validate_input(given[key]):
                return False
    return True