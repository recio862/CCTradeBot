class BaseClient(object):
    def get_current_price(self):
        raise NotImplementedError("Must implement fetching current price!")

    def buy_coin(self, *args, **kwargs):
        raise NotImplementedError("Must implement buying coin!")

    def sell_coin(self, *args, **kwargs):
        raise NotImplementedError("Must implement selling coin!")
