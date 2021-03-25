
def parse_str_with_space(var: str) -> str:
    """ return string without multiply whitespaces
    Example: var = "My name  is   John    "
    Return var = "My name is John"
    """
    str_list = list(filter(None, var.split(' ')))
    return ' '.join(x for x in str_list)
