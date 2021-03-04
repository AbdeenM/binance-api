from common.scripts.binance_spot import *
from common.scripts.binance_spot.model.constant import *
from common.scripts.binance_spot.base.printobject import *
from common.scripts.binance_spot.exception.binanceapiexception import BinanceApiException
import os
import sys
import logging
sys.path.insert(0, '/home/mephisto/Work/Project Algo/algo-trading/')


# Configuring logger
logger = logging.getLogger('algo-trading')
logger.setLevel(level=logging.INFO)

# Setting logger handler
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Declaring binance account credentials
API_KEY = os.getenv('binance_api_key')
SECRET_KEY = os.getenv('binance_secret_key')

# Initializing REST and Socket clients
api_client = RequestClient(api_key=API_KEY, secret_key=SECRET_KEY, debug=False)
subscription_client = SubscriptionClient(
    api_key=API_KEY, secret_key=SECRET_KEY)

# Defining callback function and error function for socket subscriptions
def callback(data_type: 'SubscribeMessageType', event: 'any'):
    if data_type == SubscribeMessageType.RESPONSE:
        print('Event ID: ', event)
    elif data_type == SubscribeMessageType.PAYLOAD:
        print('=========== Subscription Payload Data ===========')
        PrintBasic.print_obj(event)

        # Uncomment below to stop subscribtion
        # subscription_client.unsubscribe_all()
    else:
        print('Unknown Data: ', event)


def error(e: 'BinanceApiException'):
    print(e.error_code + e.error_message)


# Example 1: Getting old trade lookup (REST)
old_trade = api_client.get_old_trade_lookup(symbol='BTCUSDT',
                                            limit=10)

print('======= Example 1: Old Trade Look up Data =======')
PrintMix.print_data(old_trade)
print('=================================================')


# Example 2: Getting CandlStick Data (REST)
candle_data = api_client.get_candlestick_data(symbol='BTCUSDT',
                                              interval=CandlestickInterval.MIN1,
                                              startTime=None,
                                              endTime=None,
                                              limit=10)

print('======= Example 2: Kline/Candlestick Data =======')
PrintMix.print_data(candle_data)
print('=================================================')


# Example 3: Getting Symbol Price Ticker Data (REST)
symbol_price = api_client.get_symbol_price_ticker(symbol='BTCUSDT')

print('====== Example 3: Symbol Price Ticker Data ======')
PrintMix.print_data(symbol_price)
print('=================================================')


# Example 4: Getting Order Data (REST)
get_order = api_client.get_order(symbol='BTCUSDT',
                                 orderId='some-order-id')

print('=========== Example 4: Get Order Data ===========')
# PrintMix.print_data(get_order)
print('=================================================')

# Example 5: Posting an Order to binance (REST)
post_order = api_client.post_test_order(symbol='BTCUSDT',
                                        side=OrderSide.BUY,
                                        ordertype=OrderType.MARKET,
                                        timeInForce=None,
                                        quantity=9,
                                        quoteOrderQty=None,
                                        price=None,
                                        newClientOrderId=None,
                                        stopPrice=None,
                                        icebergQty=None,
                                        newOrderRespType=OrderRespType.FULL)

print('=========== Example 5: Post Order Data ==========')
PrintMix.print_data(post_order)
print('=================================================')

# Example 6: Subscribe to Trade Stream
subscription_client.subscribe_trade_event(symbol='btcusdt',
                                          callback=callback,
                                          error_handler=error)

# Example 7: Subscribe to Symbol Book Ticker
subscription_client.subscribe_symbol_bookticker_event(symbol='btcusdt',
                                                      callback=callback,
                                                      error_handler=error)

# Example 8: Subscribe to Candle Stick
subscription_client.subscribe_candlestick_event(symbol='btcusdt',
                                                interval=CandlestickInterval.MIN1,
                                                callback=callback,
                                                error_handler=error)
