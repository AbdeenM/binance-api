# Binance API Library

[![Status](https://img.shields.io/badge/build-passing-green.svg?branch=main)](https://github.com/AbdeenM/binance-api)
[![Python](https://img.shields.io/badge/Python-v3.8.5-blue.svg?logo=python)](https://www.python.org/)

A python library that implements the Binance Exchange REST API and Web socket communication.

## Installation

```Bash
$ pip install solo-binance-api
```

You can uninstall the library anytime by running:

```Bash
$ pip uninstall -y solo-binance-api
```

## Getting Started

Various implemenation for methods has been developed, a Docs is in progress to better illustrate the functions made, below is is an initial setup you can add to monitor logs and initialize your connection.

```Python
import os
import logging

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
```

## Usage

```Python
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
```

## Project Status

This project has great potential for improvements for the moment only the Binance Spot API is implemented based on their documentation, currently i wont be updating or modifying it due to time shortage but feel free to contribute!

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Please make sure to update tests as appropriate.

## License

Released under the **[MIT License](http://mit-license.org/)**

Authored and Maintained by **[Abdeen Mohamed](https://github.com/AbdeenM)**