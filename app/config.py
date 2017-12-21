import os

class DefaultConfig(object):
    SQL_DB_URI = 'sqlite:////tmp/cctradebot.sqlite'
    API_KEY = os.environ.get("GDAX_API_KEY")
    API_SECRET = os.environ.get("GDAX_API_SECRET")
    API_PASSPHRASE = os.environ.get("GDAX_API_PASSPHRASE")
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    CONFIG_PATH = os.path.join(ROOT_DIR, 'logs')

config = DefaultConfig()