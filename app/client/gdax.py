from app import config
import gdax
from app.client.base_client import BaseClient


class GDAXClient(BaseClient):
    
    def __init__(self, logger, product_id='BTC-USD'):
        self.logger = logger
        self.auth_client = self.new_client()
        self.product_id = product_id
        
    def new_client(self):
        return gdax.AuthenticatedClient(
            config.API_KEY,
            config.API_SECRET,
            config.API_PASSPHRASE)

    def get_product_ticker(self):
        return float(self.auth_client.get_product_ticker(product_id=self.product_id)['price'])

    def buy_coin(self, amount, tx):
        self.auth_client.buy(type='market', size='{}'.format(amount),
                             product_id=tx)

    def sell_coin(self, amount, tx):
        self.auth_client.sell(type='market', size='{}'.format(amount),
                              product_id=tx)