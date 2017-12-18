from enum import Enum


"""
The list of cryptocurrency exchanges supported by this application.

"""
class Clients(Enum):
    GDAX = 'gdax'
    KRAKEN = 'kraken'
    BITTREX = 'bittrex'
