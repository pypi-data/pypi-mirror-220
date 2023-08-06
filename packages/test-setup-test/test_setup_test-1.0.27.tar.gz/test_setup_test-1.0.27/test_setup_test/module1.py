import random, re, string, uuid, jwt, math, pytz
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from time import time
from random import randint
from hashids import Hashids
from slugify import slugify

def str_to_bool(s):
    """
    Converts a string to a boolean value.

    The function checks if the stripped and lowercase version of the string is 'true' or 'false'.
    If it matches 'true', the function returns boolean True.
    If it matches 'false', the function returns boolean False.
    Otherwise, it returns None.

    Parameters:
        s (str): The input string to be converted to a boolean value.

    Returns:
        bool or None: The converted boolean value if the string is 'true' or 'false'. Otherwise, None.

    Example:
        >>> str_to_bool('True')
        True
        >>> str_to_bool('False')
        False
        >>> str_to_bool('invalid')
        None

    """
    if s.strip().lower() == 'true': # If the stripped and lowercase string is 'true'
        return True # Return boolean True
    elif s.strip().lower() == 'false': # If the stripped and lowercase string is 'false'
        return False # Return boolean False
    else: 
        return None # Return None if the string is neither 'true' nor 'false'

def format_email(email):
    """
    Formats an email address.

    This function takes an email address as input and performs the following operations:
        - If the email is not empty or None, it removes leading and trailing whitespace and converts it to lowercase.
        - If the email is empty or None, it returns the email as it is.

    Parameters:
        email (str): The email address to be formatted.

    Returns:
        str: The formatted email address, or the original email if it is empty or None.

    Example:
        >>> format_email("  john@example.com ")
        'john@example.com'
        >>> format_email("MARY@example.com")
        'mary@example.com'
        >>> format_email("")
        ''
        >>> format_email(None)
        None

    """
    if email:  # If the email is not empty or None
        return email.strip().lower() # Remove leading/trailing whitespace and convert to lowercase
    return email # Return the email as it is if it is empty or None