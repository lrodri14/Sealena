"""
    This main_utilities.py file contains all the variable declarations and function for the main app to perform
    correctly.
"""
import requests
import random
from Sealena.settings import X_RAPID_API_QUOTES_ENDPOINT, X_RAPID_API_KEY_QUOTES, X_RAPID_API_KEY_HOST_QUOTES

api_key = X_RAPID_API_KEY_QUOTES
host = X_RAPID_API_KEY_HOST_QUOTES
quote_categories = ['love', 'god', 'wisdom', 'beauty', 'dreams']
endpoint = X_RAPID_API_QUOTES_ENDPOINT
headers = {'x-rapidapi-key': api_key, 'x-rapidapi-host': host}
querystring = {'category': random.choice(quote_categories), 'count': '1'}


def collect_quote():
    """
        DOCSTRING:
        This collect quote function is used to retrieve a quote from the famous-quotes API, this will be returned as a
        tuple containing the quote itself and it's author.
    """
    response = requests.get(endpoint, headers=headers, params=querystring).json()
    try:
        quote = response[0]['text']
        author = response[0]['author']
    except:
        quote = 'Try not to become a man of success, but rather try to become a man of value'
        author = 'Albert Einstein'
    return tuple([quote, author])
