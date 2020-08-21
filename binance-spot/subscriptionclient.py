import urllib.parse

from common.scripts.binance_spot.constant.system import WebSocketDefine
from common.scripts.binance_spot.impl.websocketrequestimpl import WebsocketRequestImpl
from common.scripts.binance_spot.impl.websocketconnection import WebsocketConnection
from common.scripts.binance_spot.impl.websocketwatchdog import WebSocketWatchDog
from common.scripts.binance_spot.impl.restapirequestimpl import RestApiRequestImpl
from common.scripts.binance_spot.model import *
from common.scripts.binance_spot.model.constant import *

# For develop
from common.scripts.binance_spot.base.printobject import *


class SubscriptionClient(object):

    def __init__(self, **kwargs):
        '''
        Create the subscription client to subscribe the update from server.

        :param kwargs: The option of subscription connection.
            api_key: The public key applied from common.scripts.binance_spot.
            secret_key: The private key applied from common.scripts.binance_spot.
            uri: Set the URI for subscription.
            is_auto_connect: When the connection lost is happening on the subscription line, specify whether the client
                            reconnect to server automatically. The connection lost means:
                                Caused by network problem
                                The connection close triggered by server (happened every 24 hours)
                            No any message can be received from server within a specified time, see receive_limit_ms
            receive_limit_ms: Set the receive limit in millisecond. If no message is received within this limit time,
                            the connection will be disconnected.
            connection_delay_failure: If auto reconnect is enabled, specify the delay time before reconnect.
        '''
        api_key = None
        secret_key = None
        if 'api_key' in kwargs:
            api_key = kwargs['api_key']
        if 'secret_key' in kwargs:
            secret_key = kwargs['secret_key']
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.websocket_request_impl = WebsocketRequestImpl(self.__api_key)
        self.connections = list()
        self.uri = WebSocketDefine.Uri
        is_auto_connect = True
        receive_limit_ms = 60000
        connection_delay_failure = 1
        if 'uri' in kwargs:
            self.uri = kwargs['uri']
        if 'is_auto_connect' in kwargs:
            is_auto_connect = kwargs['is_auto_connect']
        if 'receive_limit_ms' in kwargs:
            receive_limit_ms = kwargs['receive_limit_ms']
        if 'connection_delay_failure' in kwargs:
            connection_delay_failure = kwargs['connection_delay_failure']
        self.__watch_dog = WebSocketWatchDog(
            is_auto_connect, receive_limit_ms, connection_delay_failure)

    def __create_connection(self, request):
        connection = WebsocketConnection(
            self.__api_key, self.__secret_key, self.uri, self.__watch_dog, request)
        self.connections.append(connection)
        connection.connect()

    def unsubscribe_all(self):
        for conn in self.connections:
            conn.close()
        self.connections.clear()

    def subscribe_aggregate_trade_event(self, symbol: 'str', callback, error_handler=None):
        '''
        Aggregate Trade Streams

        The Aggregate Trade Streams push trade information that is aggregated for a single taker order every 100 milliseconds.

        Stream Name: <symbol>@aggTrade

        Update Speed: Real-time

        Payload:

        {
            "e": "aggTrade",  // Event type
            "E": 123456789,   // Event time
            "s": "BNBBTC",    // Symbol
            "a": 12345,       // Aggregate trade ID
            "p": "0.001",     // Price
            "q": "100",       // Quantity
            "f": 100,         // First trade ID
            "l": 105,         // Last trade ID
            "T": 123456785,   // Trade time
            "m": true,        // Is the buyer the market maker?
            "M": true         // Ignore
        }
        '''
        request = self.websocket_request_impl.subscribe_aggregate_trade_event(
            symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_trade_event(self, symbol: 'str', callback, error_handler=None):
        '''
        Trade Streams

        The Trade Streams push raw trade information; each trade has a unique buyer and seller.

        Stream Name: <symbol>@trade

        Update Speed: Real-time

        Payload:

        {
            "e": "trade",     // Event type
            "E": 123456789,   // Event time
            "s": "BNBBTC",    // Symbol
            "t": 12345,       // Trade ID
            "p": "0.001",     // Price
            "q": "100",       // Quantity
            "b": 88,          // Buyer order ID
            "a": 50,          // Seller order ID
            "T": 123456785,   // Trade time
            "m": true,        // Is the buyer the market maker?
            "M": true         // Ignore
        }
        '''
        request = self.websocket_request_impl.subscribe_trade_event(
            symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_candlestick_event(self, symbol: 'str', interval: 'CandlestickInterval', callback,
                                    error_handler=None):
        '''
        Kline/Candlestick Streams

        The Kline/Candlestick Stream push updates to the current klines/candlestick every 250 milliseconds (if existing).

        Stream Name: <symbol>@kline_<interval>

        Update Speed: 2000ms

        Payload:

        {
            "e": "kline",     // Event type
            "E": 123456789,   // Event time
            "s": "BNBBTC",    // Symbol
            "k": {
                "t": 123400000, // Kline start time
                "T": 123460000, // Kline close time
                "s": "BNBBTC",  // Symbol
                "i": "1m",      // Interval
                "f": 100,       // First trade ID
                "L": 200,       // Last trade ID
                "o": "0.0010",  // Open price
                "c": "0.0020",  // Close price
                "h": "0.0025",  // High price
                "l": "0.0015",  // Low price
                "v": "1000",    // Base asset volume
                "n": 100,       // Number of trades
                "x": false,     // Is this kline closed?
                "q": "1.0000",  // Quote asset volume
                "V": "500",     // Taker buy base asset volume
                "Q": "0.500",   // Taker buy quote asset volume
                "B": "123456"   // Ignore
            }
        }
        '''
        request = self.websocket_request_impl.subscribe_candlestick_event(
            symbol, interval, callback, error_handler)
        self.__create_connection(request)

    def subscribe_symbol_miniticker_event(self, symbol: 'str', callback, error_handler=None):
        '''
        Individual Symbol Mini Ticker Stream

        24hr rolling window mini-ticker statistics for a single symbol pushed every 3 seconds. These are NOT the statistics of the UTC day, 
        but a 24hr rolling window from requestTime to 24hrs before.

        Stream Name: <symbol>@miniTicker

        Update Speed: 1000ms

        Payload:

        {
            "e": "24hrMiniTicker",  // Event type
            "E": 123456789,         // Event time
            "s": "BNBBTC",          // Symbol
            "c": "0.0025",          // Close price
            "o": "0.0010",          // Open price
            "h": "0.0025",          // High price
            "l": "0.0010",          // Low price
            "v": "10000",           // Total traded base asset volume
            "q": "18"               // Total traded quote asset volume
        }
        '''
        request = self.websocket_request_impl.subscribe_symbol_miniticker_event(
            symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_all_miniticker_event(self, callback, error_handler=None):
        '''
        All Market Mini Tickers Stream

        24hr rolling window mini-ticker statistics for all symbols pushed every 3 seconds. 
        These are NOT the statistics of the UTC day, but a 24hr rolling window from requestTime to 24hrs before. 
        Note that only tickers that have changed will be present in the array.

        Stream Name: !miniTicker@arr

        Update Speed: 1000ms

        Payload:

        [
            {
                // Same as <symbol>@miniTicker payload
            }
        ]
        '''
        request = self.websocket_request_impl.subscribe_all_miniticker_event(
            callback, error_handler)
        self.__create_connection(request)

    def subscribe_symbol_ticker_event(self, symbol: 'str', callback, error_handler=None):
        '''
        Individual Symbol Ticker Streams

        24hr rollwing window ticker statistics for a single symbol pushed every 3 seconds. These are NOT the statistics of the UTC day, 
        but a 24hr rolling window from requestTime to 24hrs before.

        Stream Name: <symbol>@ticker

        Update Speed: 1000ms

        Payload:

        {
            "e": "24hrTicker",  // Event type
            "E": 123456789,     // Event time
            "s": "BNBBTC",      // Symbol
            "p": "0.0015",      // Price change
            "P": "250.00",      // Price change percent
            "w": "0.0018",      // Weighted average price
            "x": "0.0009",      // First trade(F)-1 price (first trade before the 24hr rolling window)
            "c": "0.0025",      // Last price
            "Q": "10",          // Last quantity
            "b": "0.0024",      // Best bid price
            "B": "10",          // Best bid quantity
            "a": "0.0026",      // Best ask price
            "A": "100",         // Best ask quantity
            "o": "0.0010",      // Open price
            "h": "0.0025",      // High price
            "l": "0.0010",      // Low price
            "v": "10000",       // Total traded base asset volume
            "q": "18",          // Total traded quote asset volume
            "O": 0,             // Statistics open time
            "C": 86400000,      // Statistics close time
            "F": 0,             // First trade ID
            "L": 18150,         // Last trade Id
            "n": 18151          // Total number of trades
        }
        '''
        request = self.websocket_request_impl.subscribe_symbol_ticker_event(
            symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_all_ticker_event(self, callback, error_handler=None):
        '''
        All Market Tickers Stream

        24hr rollwing window ticker statistics for all symbols pushed every 3 seconds. These are NOT the statistics of the UTC day, but a 24hr rolling window from requestTime to 24hrs before. 
        Note that only tickers that have changed will be present in the array.

        Stream Name: !ticker@arr

        Update Speed: 1000ms

        Payload:

        [
            {
                // Same as <symbol>@ticker payload
            }
        ]
        '''
        request = self.websocket_request_impl.subscribe_all_ticker_event(
            callback, error_handler)
        self.__create_connection(request)

    def subscribe_symbol_bookticker_event(self, symbol: 'str', callback, error_handler=None):
        '''
        Individual Symbol Book Ticker Streams

        Pushes any update to the best bid or ask's price or quantity in real-time for a specified symbol.

        Stream Name: <symbol>@bookTicker

        Update Speed: Real-time

        Payload:

        {
            "u":400900217,     // order book updateId
            "s":"BNBUSDT",     // symbol
            "b":"25.35190000", // best bid price
            "B":"31.21000000", // best bid qty
            "a":"25.36520000", // best ask price
            "A":"40.66000000"  // best ask qty
        }
        '''
        request = self.websocket_request_impl.subscribe_symbol_bookticker_event(
            symbol, callback, error_handler)
        self.__create_connection(request)

    def subscribe_all_bookticker_event(self, callback, error_handler=None):
        '''
        All Book Tickers Stream

        Pushes any update to the best bid or ask's price or quantity in real-time for all symbols.

        Stream Name: !bookTicker

        Update Speed: Real-time

        Payload:

        {
            // Same as <symbol>@bookTicker payload
        }
        '''
        request = self.websocket_request_impl.subscribe_all_bookticker_event(
            callback, error_handler)
        self.__create_connection(request)

    def subscribe_book_depth_event(self, symbol: 'str', limit: 'int', callback, error_handler=None, update_time: 'UpdateTime' = UpdateTime.INVALID):
        '''
        Partial Book Depth Streams

        Top bids and asks, Valid are 5, 10, or 20.

        Stream Names: <symbol>@depth<levels> OR <symbol>@depth<levels>@100ms.

        Update Speed: 1000ms or 100ms

        Payload:

        {
            "lastUpdateId": 160,  // Last update ID
            "bids": [             // Bids to be updated
                [
                "0.0024",         // Price level to be updated
                "10"              // Quantity
                ]
            ],
            "asks": [             // Asks to be updated
                [
                "0.0026",         // Price level to be updated
                "100"            // Quantity
                ]
            ]
        }
        '''
        print(update_time)
        request = self.websocket_request_impl.subscribe_book_depth_event(
            symbol, limit, update_time, callback, error_handler)
        self.__create_connection(request)

    def subscribe_diff_depth_event(self, symbol: 'str', callback, error_handler=None, update_time: 'UpdateTime' = UpdateTime.INVALID):
        '''
        Diff. Depth Stream

        Order book price and quantity depth updates used to locally manage an order book.

        Stream Name: <symbol>@depth OR <symbol>@depth@100ms

        Update Speed: 1000ms or 100ms

        Payload:

        {
            "e": "depthUpdate", // Event type
            "E": 123456789,     // Event time
            "s": "BNBBTC",      // Symbol
            "U": 157,           // First update ID in event
            "u": 160,           // Final update ID in event
            "b": [              // Bids to be updated
                [
                "0.0024",       // Price level to be updated
                "10"            // Quantity
                ]
            ],
            "a": [              // Asks to be updated
                [
                "0.0026",       // Price level to be updated
                "100"           // Quantity
                ]
            ]
        }
        '''
        request = self.websocket_request_impl.subscribe_diff_depth_event(
            symbol, update_time, callback, error_handler)
        self.__create_connection(request)

    def subscribe_user_data_event(self, listenKey: 'str', callback, error_handler=None):
        '''
        User Data Streams
        '''
        request = self.websocket_request_impl.subscribe_user_data_event(
            listenKey, callback, error_handler)
        self.__create_connection(request)
