import time
import gdax
import traceback
import logging
from logging.handlers import RotatingFileHandler
from app.config import config
from app.client import gdax as gdax_client

def create_logger():
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    logFile = '/root/tradebot/logs/tradebot'
    log_handler = RotatingFileHandler(logFile, mode='a', maxBytes=50*1024*1024,
                                      backupCount=3, encoding=None, delay=0)
    log_handler.setFormatter(log_formatter)
    log_handler.setLevel(logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)
    return logger

class MeanReversal(object):
    """
    The values passed to our mean reversal will determine how the strategy is executed.

     price_tick_interval = 1  # Time in seconds to store each price tick interval
     time_window = 10  # Time in minutes to look back
     amount_per_transaction = 0.0001  # Amount of BTC to trade per transaction
     margin_to_trade = 75  # Margin difference between average and current prices
     time_to_wait_for_refresh = 30 # Time in minutes before it refreshes the ability to buy or sell again
     transaction_type = 'BTC-USD'
    """
    def __init__(self, time_window=10, amount_per_transaction=0.0001, margin_to_trade=75, transaction_type='btc-usd',
                 price_tick_interval=1, logger=None, time_to_wait_for_refresh=30, name="TradeBot",
                 long_term_price_tick_window=720, long_term_margin_block=1000, client=None):
        
        self.time_window = time_window
        self.amount_per_transaction = amount_per_transaction
        self.margin_to_trade = margin_to_trade
        self.transaction_type = transaction_type
        self.price_tick_interval = price_tick_interval
        self.logger = logger if logger else logging.getLogger()
        self.time_to_wait_for_refresh = time_to_wait_for_refresh
        self.buys = list()
        self.sells = list()
        self.state = None
        self.current_time = time.time()
        self.price_ticks = list()
        self.long_term_price_ticks = time.time()
        self.long_term_price_tick_window = long_term_price_tick_window
        self.long_term_margin_block = long_term_margin_block
        self.name = name
        self.client = client

    def buy(self, price, average):
        self.buys.append(price)
        self.logger.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        self.logger.info("Performing a market BUY for {}".format(self.name))
        self.logger.info("Current price: {}".format(price))
        self.logger.info("{} min average: {}".format(self.time_window, average))
        self.logger.info("Current list of sells: {}\nCurrent list of buys: {}".format(self.sells, self.buys))
        self.logger.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        self.client.buy_coin(price, self.amount_per_transaction, self.transaction_type)

    def sell(self, price, average):
        self.sells.append(price)
        self.logger.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        self.logger.info("Performing a market SELL for {}".format(self.name))
        self.logger.info("Current price: {}".format(price))
        self.logger.info("{} min average: {}".format(self.time_window, average))
        self.logger.info("Current list of sells: {}\nCurrent list of buys: {}".format(self.sells, self.buys))
        self.logger.info("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        self.client.sell_coin(price, self.amount_per_transaction, self.transaction_type)

def run_loop(trade_bots):
    trade_bots[0].logger.info("Beginning trades!")

    while True:
        try:
            next_price = trade_bots[0].client.get_current_price()
        except Exception as exc:
            logger.error("Exception querying ticker: {}\n...continuing.".format(exc))
            continue
        for trade_bot in trade_bots:
            try:
                for trade_bot in trade_bots:
                    trade_bot.price_ticks.append(float(next_price))
                    trade_bot.long_term_price_ticks.append(float(next_price))
                    if len(trade_bot.price_ticks) > (trade_bot.time_window * 60):
                        trade_bot.price_ticks.pop(0)
                    if len(trade_bot.long_term_price_ticks) > (trade_bot.long_term_price_tick_window * 60):
                        trade_bot.long_term_price_ticks.pop(0)

                    average = sum(trade_bot.price_ticks)/len(trade_bot.price_ticks)
                    if (time.time() - trade_bot.current_time) > (60 * trade_bot.time_to_wait_for_refresh):
                        trade_bot.current_time = time.time()
                        trade_bot.state = None

                    if abs(average - float(next_price)) > trade_bot.margin_to_trade:
                        if next_price - average < 0 and (trade_bot.state == 'buy' or trade_bot.state is None):
                            trade_bot.buy_bitcoin(next_price, average)
                            trade_bot.current_time = time.time()
                            trade_bot.state = 'sell'
                        elif next_price - average > 0 and (trade_bot.state == 'sell' or trade_bot.state is None):
                            trade_bot.sell_bitcoin(next_price, average)
                            trade_bot.current_time = time.time()
                            trade_bot.state = 'buy'
            except Exception as exc:
                logger.error("Exception with message: {}".format(exc))
                if trade_bot.state == 'buy':
                    trade_bot.state = 'sell'
                elif trade_bot.state == 'sell':
                    trade_bot.state = 'buy'
                trade_bot.current_time = time.time()
        # Changing this can effect the number of price ticks stored
        time.sleep(trade_bots[0].price_tick_interval)

if __name__ == '__main__':
    bots = list()

    logger = create_logger()
    bot = MeanReversal(time_window=30,
                             amount_per_transaction=0.0001,
                             margin_to_trade=150,
                             logger=logger,
                             time_to_wait_for_refresh=60,
                             name="trade-btc-150margin-30min",
                       client=gdax_client.GDAXClient(logger, product_id='BTC-USD'))
    bots.append(bot)

    run_loop(bots)
