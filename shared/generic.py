import re

def loose_string_equal(a_string: str, b_string: str) -> bool:
    """
    Used for testing inputs with similar values.
    """

    # normalise strings
    a_string = a_string.lower()
    b_string = b_string.lower()

    # remove crap from string
    a_string = re.sub(r"[^\w\s]", "", a_string)
    b_string = re.sub(r"[^\w\s]", "", b_string)

    # Compare the cleaned, lowercased strings
    return a_string == b_string
