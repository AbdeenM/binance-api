from typing import List
from common.scripts.binance_spot.constant.system import RestApiDefine
from common.scripts.binance_spot.impl.restapirequestimpl import RestApiRequestImpl
from common.scripts.binance_spot.impl.restapiinvoker import call_sync
from common.scripts.binance_spot.model import AccountInformation, Candlestick, Order, OrderOCO, ExchangeInformation
from common.scripts.binance_spot.model.constant import *


class RequestClient(object):

    def __init__(self, **kwargs):
        '''
        Create the request client instance.
        :param kwargs: The option of request connection.
            api_key: The public key applied from common.scripts.binance_spot.
            secret_key: The private key applied from common.scripts.binance_spot.
            server_url: The URL name like 'https://api.binance.com'.
            debug: If request logs to print or not (True or False).
        '''
        api_key = None
        secret_key = None
        url = RestApiDefine.Url
        self.__debug = None
        if 'api_key' in kwargs:
            api_key = kwargs['api_key']
        if 'secret_key' in kwargs:
            secret_key = kwargs['secret_key']
        if 'url' in kwargs:
            url = kwargs['url']
        if 'debug' in kwargs:
            self.__debug = kwargs['debug']
        try:
            self.request_impl = RestApiRequestImpl(
                api_key, secret_key, url, self.__debug)
        except Exception:
            pass
        self.limits = {}

    def __call_sync(self, request):
        return call_sync(request, self.__debug)

    def refresh_limits(self, limits):
        for k, v in limits.items():
            self.limits[k] = v

    def test_connectivity(self) -> any:
        '''
        Test Connectivity

        GET /api/v3/ping

        Test connectivity to the Rest API.

        Payload:

        {}
        '''
        response = self.__call_sync(self.request_impl.test_connectivity())
        self.refresh_limits(response[1])
        return response[0]

    def get_servertime(self) -> any:
        '''
        Check Server Time

        GET /api/v3/time

        Test connectivity to the Rest API and get the current server time.

        Payload:

        {
            "serverTime": 1499827319559
        }
        '''
        response = self.__call_sync(self.request_impl.get_servertime())
        self.refresh_limits(response[1])
        return response[0]

    def get_exchange_information(self) -> ExchangeInformation:
        '''
        Exchange Information (MARKET_DATA)

        GET /api/v3/exchangeInfo

        Current exchange trading rules and symbol information.

        Payload:

        {
            "timezone": "UTC",
            "serverTime": 1565246363776,
            "rateLimits": [
                {
                //These are defined in the `ENUM definitions` section under `Rate Limiters (rateLimitType)`.
                //All limits are optional
                }
            ],
            "exchangeFilters": [
                //These are the defined filters in the `Filters` section.
                //All filters are optional.
            ],
            "symbols": [
                {
                "symbol": "ETHBTC",
                "status": "TRADING",
                "baseAsset": "ETH",
                "baseAssetPrecision": 8,
                "quoteAsset": "BTC",
                "quotePrecision": 8,
                "quoteAssetPrecision": 8,
                "orderTypes": [
                    "LIMIT",
                    "LIMIT_MAKER",
                    "MARKET",
                    "STOP_LOSS",
                    "STOP_LOSS_LIMIT",
                    "TAKE_PROFIT",
                    "TAKE_PROFIT_LIMIT"
                ],
                "icebergAllowed": true,
                "ocoAllowed": true,
                "isSpotTradingAllowed": true,
                "isMarginTradingAllowed": true,
                "filters": [
                    //These are defined in the Filters section.
                    //All filters are optional
                ],
                "permissions": [
                    "SPOT",
                    "MARGIN"
                ]
                }
            ]
        }
        '''
        response = self.__call_sync(
            self.request_impl.get_exchange_information())
        self.refresh_limits(response[1])
        return response[0]

    def get_order_book(self, symbol: 'str', limit: 'int' = None) -> any:
        '''
        Order Book (MARKET_DATA)

        GET /api/v3/depth

        Adjusted based on the limit.

        Payload:

        {
            "lastUpdateId": 1027024,
            "bids": [
                [
                "4.00000000",     // PRICE
                "431.00000000"    // QTY
                ]
            ],
            "asks": [
                [
                "4.00000200",
                "12.00000000"
                ]
            ]
        }
        '''
        response = self.__call_sync(
            self.request_impl.get_order_book(symbol, limit))
        self.refresh_limits(response[1])
        return response[0]

    def get_recent_trades_list(self, symbol: 'str', limit: 'int' = None) -> any:
        '''
        Recent Trades List (MARKET_DATA)

        GET /api/v3/trades 

        Get recent trades (up to last 500).

        Payload:

        [
            {
                "id": 28457,
                "price": "4.00000100",
                "qty": "12.00000000",
                "quoteQty": "48.000012",
                "time": 1499865549590,
                "isBuyerMaker": true,
                "isBestMatch": true
            }
        ]
        '''
        response = self.__call_sync(
            self.request_impl.get_recent_trades_list(symbol, limit))
        self.refresh_limits(response[1])
        return response[0]

    def get_old_trade_lookup(self, symbol: 'str', limit: 'int' = None, fromId: 'long' = None) -> any:
        '''
        Old Trades Lookup (MARKET_DATA)

        GET /api/v3/historicalTrades

        Get older market historical trades.

        Payload:

        [
            {
                "id": 28457,
                "price": "4.00000100",
                "qty": "12.00000000",
                "quoteQty": "48.000012",
                "time": 1499865549590, // Trade executed timestamp, as same as `T` in the stream
                "isBuyerMaker": true,
                "isBestMatch": true
            }
        ]
        '''
        response = self.__call_sync(
            self.request_impl.get_old_trade_lookup(symbol, limit, fromId))
        self.refresh_limits(response[1])
        return response[0]

    def get_aggregate_trades_list(self, symbol: 'str', fromId: 'long' = None,
                                  startTime: 'long' = None, endTime: 'long' = None, limit: 'int' = None) -> any:
        '''
        Compressed/Aggregate Trades List (MARKET_DATA)

        GET /api/v3/aggTrades

        Get compressed, aggregate trades. Trades that fill at the time, from the same order, 
        with the same price will have the quantity aggregated.

        Notes:
            1. If startTime and endTime are sent, time between startTime and endTime must be less than 1 hour.
            2. If fromId, startTime, and endTime are not sent, the most recent aggregate trades will be returned.

        Payload:

        [
            {
                "a": 26129,         // Aggregate tradeId
                "p": "0.01633102",  // Price
                "q": "4.70443515",  // Quantity
                "f": 27781,         // First tradeId
                "l": 27781,         // Last tradeId
                "T": 1498793709153, // Timestamp
                "m": true,          // Was the buyer the maker?
                "M": true           // Was the trade the best price match?
            }
        ]
        '''
        response = self.__call_sync(self.request_impl.get_aggregate_trades_list(
            symbol, fromId, startTime, endTime, limit))
        self.refresh_limits(response[1])
        return response[0]

    def get_candlestick_data(self, symbol: 'str', interval: 'CandlestickInterval',
                             startTime: 'long' = None, endTime: 'long' = None, limit: 'int' = None) -> List[Candlestick]:
        '''
        Kline/Candlestick Data (MARKET_DATA)

        GET /api/v3/klines

        Kline/candlestick bars for a symbol. Klines are uniquely identified by their open time.

        Payload:

        [
            [
                1499040000000,      // Open time
                "0.01634790",       // Open
                "0.80000000",       // High
                "0.01575800",       // Low
                "0.01577100",       // Close
                "148976.11427815",  // Volume
                1499644799999,      // Close time
                "2434.19055334",    // Quote asset volume
                308,                // Number of trades
                "1756.87402397",    // Taker buy base asset volume
                "28.46694368",      // Taker buy quote asset volume
                "17928899.62484339" // Ignore
            ]
        ]
        '''
        response = self.__call_sync(self.request_impl.get_candlestick_data(
            symbol, interval, startTime, endTime, limit))
        self.refresh_limits(response[1])
        return response[0]

    def get_current_average_price(self, symbol: 'str') -> any:
        '''
        Current Average Price (MARKET_DATA)

        GET /api/v3/avgPrice 

        Current average price for a symbol.

        Payload:

        {
            "mins": 5,
            "price": "9.35751834"
        }
        '''
        response = self.__call_sync(
            self.request_impl.get_current_average_price(symbol))
        self.refresh_limits(response[1])
        return response[0]

    def get_ticker_price_change_statistics(self, symbol: 'str' = None) -> any:
        '''
        24hr Ticker Price Change Statistics (MARKET_DATA)

        GET /api/v3/ticker/24hr

        24 hour rolling window price change statistics.
        Careful when accessing this with no symbol.

        Note: If the symbol is not sent, tickers for all symbols will be returned in an array.

        Payload:

        {
            "symbol": "BNBBTC",
            "priceChange": "-94.99999800",
            "priceChangePercent": "-95.960",
            "weightedAvgPrice": "0.29628482",
            "prevClosePrice": "0.10002000",
            "lastPrice": "4.00000200",
            "lastQty": "200.00000000",
            "bidPrice": "4.00000000",
            "askPrice": "4.00000200",
            "openPrice": "99.00000000",
            "highPrice": "100.00000000",
            "lowPrice": "0.10000000",
            "volume": "8913.30000000",
            "quoteVolume": "15.30000000",
            "openTime": 1499783499040,
            "closeTime": 1499869899040,
            "firstId": 28385,   // First tradeId
            "lastId": 28460,    // Last tradeId
            "count": 76         // Trade count
        }

        OR

        [
            {
                "symbol": "BNBBTC",
                "priceChange": "-94.99999800",
                "priceChangePercent": "-95.960",
                "weightedAvgPrice": "0.29628482",
                "prevClosePrice": "0.10002000",
                "lastPrice": "4.00000200",
                "lastQty": "200.00000000",
                "bidPrice": "4.00000000",
                "askPrice": "4.00000200",
                "openPrice": "99.00000000",
                "highPrice": "100.00000000",
                "lowPrice": "0.10000000",
                "volume": "8913.30000000",
                "quoteVolume": "15.30000000",
                "openTime": 1499783499040,
                "closeTime": 1499869899040,
                "firstId": 28385,   // First tradeId
                "lastId": 28460,    // Last tradeId
                "count": 76         // Trade count
            }
        ]
        '''
        response = self.__call_sync(
            self.request_impl.get_ticker_price_change_statistics(symbol))
        self.refresh_limits(response[1])
        return response[0]

    def get_symbol_price_ticker(self, symbol: 'str' = None) -> any:
        '''
        Symbol Price Ticker (MARKET_DATA)

        GET /api/v3/ticker/price

        Latest price for a symbol or symbols.

        Note: If the symbol is not sent, prices for all symbols will be returned in an array.

        Payload:

        {
            "symbol": "LTCBTC",
            "price": "4.00000200"
        }

        OR

        [
            {
                "symbol": "LTCBTC",
                "price": "4.00000200"
            },
            {
                "symbol": "ETHBTC",
                "price": "0.07946600"
            }
        ]
        '''
        response = self.__call_sync(
            self.request_impl.get_symbol_price_ticker(symbol))
        self.refresh_limits(response[1])
        return response[0]

    def get_symbol_orderbook_ticker(self, symbol: 'str' = None) -> any:
        '''
        Symbol Order Book Ticker (MARKET_DATA)

        GET /api/v3/ticker/bookTicker

        Best price/qty on the order book for a symbol or symbols.

        Note: If the symbol is not sent, bookTickers for all symbols will be returned in an array.

        Payload:

        {
            "symbol": "LTCBTC",
            "bidPrice": "4.00000000",
            "bidQty": "431.00000000",
            "askPrice": "4.00000200",
            "askQty": "9.00000000"
        }

        OR

        [
            {
                "symbol": "LTCBTC",
                "bidPrice": "4.00000000",
                "bidQty": "431.00000000",
                "askPrice": "4.00000200",
                "askQty": "9.00000000"
            },
            {
                "symbol": "ETHBTC",
                "bidPrice": "0.07946700",
                "bidQty": "9.00000000",
                "askPrice": "100000.00000000",
                "askQty": "1000.00000000"
            }
        ]
        '''
        response = self.__call_sync(
            self.request_impl.get_symbol_orderbook_ticker(symbol))
        self.refresh_limits(response[1])
        return response[0]

    def post_test_order(self, symbol: 'str', side: 'OrderSide', ordertype: 'OrderType',
                        timeInForce: 'TimeInForce' = TimeInForce.INVALID, quantity: 'float' = None,
                        quoteOrderQty: 'float' = None, price: 'float' = None,
                        newClientOrderId: 'str' = None, stopPrice: 'float' = None,
                        icebergQty: 'float' = None, newOrderRespType: 'OrderRespType' = OrderRespType.INVALID) -> any:
        '''
        Test New Order (TRADE)

        POST /api/v3/order/test (HMAC SHA256)

        Test new order creation and signature/recvWindow long. Creates and validates a new order 
        but does not send it into the matching engine.

        Payload:

        {}
        '''
        response = self.__call_sync(self.request_impl.post_test_order(symbol, side, ordertype,
                                                                      timeInForce, quantity, quoteOrderQty,
                                                                      price, newClientOrderId, stopPrice,
                                                                      icebergQty, newOrderRespType))
        self.refresh_limits(response[1])
        return response[0]

    def post_order(self, symbol: 'str', side: 'OrderSide', ordertype: 'OrderType',
                   timeInForce: 'TimeInForce' = TimeInForce.INVALID, quantity: 'float' or str = None,
                   quoteOrderQty: 'float' = None, price: 'float' or str = None,
                   newClientOrderId: 'str' = None, stopPrice: 'float' or str = None,
                   icebergQty: 'float' = None, newOrderRespType: 'OrderRespType' = OrderRespType.INVALID) -> Order:
        '''
        New Order (TRADE)

        POST /api/v3/order (HMAC SHA256)

        Send in a new order.

        Notes:
            1. LIMIT_MAKER are LIMIT orders that will be rejected if they would immediately match and trade as a taker.
            2. STOP_LOSS and TAKE_PROFIT will execute a MARKET order when the stopPrice is reached.
            3. Any LIMIT or LIMIT_MAKER type order can be made an iceberg order by sending an icebergQty.
            4. Any order with an icebergQty MUST have timeInForce set to GTC.
            5. MARKET orders using the quantity field specifies the amount of the base asset the user wants to buy or 
            sell at the market price.
                * For example, sending a MARKET order on BTCUSDT will specify how much BTC the user is buying or selling.
            6. MARKET orders using quoteOrderQty specifies the amount the user wants to spend (when buying) or receive 
            (when selling) the quote asset; the correct quantity will be determined based on the market liquidity and quoteOrderQty.
                * Using BTCUSDT as an example:
                    - On the BUY side, the order will buy as many BTC as quoteOrderQty USDT can.
                    - On the SELL side, the order will sell as much BTC needed to receive quoteOrderQty USDT.
            7. MARKET orders using quoteOrderQty will not break LOT_SIZE filter rules; the order will execute a quantity that 
            will have the notional value as close as possible to quoteOrderQty.
            8. same newClientOrderId can be accepted only when the previous one is filled, otherwise the order will be rejected.
            9. Trigger order price rules against market price for both MARKET and LIMIT versions:
                * Price above market price: STOP_LOSS BUY, TAKE_PROFIT SELL
                * Price below market price: STOP_LOSS SELL, TAKE_PROFIT BUY

        Payload ACK:

        {
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1, //Unless OCO, value will be -1
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595
        }

        Payload RESULT:

        {
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1, //Unless OCO, value will be -1
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595,
            "price": "0.00000000",
            "origQty": "10.00000000",
            "executedQty": "10.00000000",
            "cummulativeQuoteQty": "10.00000000",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "SELL"
        }

        Payload FULL:

        {
            "symbol": "BTCUSDT",
            "orderId": 28,
            "orderListId": -1, //Unless OCO, value will be -1
            "clientOrderId": "6gCrw2kRUAF9CvJDGP16IP",
            "transactTime": 1507725176595,
            "price": "0.00000000",
            "origQty": "10.00000000",
            "executedQty": "10.00000000",
            "cummulativeQuoteQty": "10.00000000",
            "status": "FILLED",
            "timeInForce": "GTC",
            "type": "MARKET",
            "side": "SELL",
            "fills": [
                {
                "price": "4000.00000000",
                "qty": "1.00000000",
                "commission": "4.00000000",
                "commissionAsset": "USDT"
                },
                {
                "price": "3999.00000000",
                "qty": "5.00000000",
                "commission": "19.99500000",
                "commissionAsset": "USDT"
                },
                {
                "price": "3998.00000000",
                "qty": "2.00000000",
                "commission": "7.99600000",
                "commissionAsset": "USDT"
                },
                {
                "price": "3997.00000000",
                "qty": "1.00000000",
                "commission": "3.99700000",
                "commissionAsset": "USDT"
                },
                {
                "price": "3995.00000000",
                "qty": "1.00000000",
                "commission": "3.99500000",
                "commissionAsset": "USDT"
                }
            ]
        }
        '''
        response = self.__call_sync(self.request_impl.post_order(symbol, side, ordertype,
                                                                 timeInForce, quantity, quoteOrderQty,
                                                                 price, newClientOrderId, stopPrice,
                                                                 icebergQty, newOrderRespType))
        self.refresh_limits(response[1])
        return response[0]

    def cancel_order(self, symbol: 'str', orderId: 'long' = None, newClientOrderId: 'str' = None) -> any:
        '''
        Cancel Order (TRADE)

        DELETE /api/v3/order (HMAC SHA256)

        Cancel an active order.

        Note: Not sure how to handle "newClientOrderId", try setting it to a unique id 
        maybe time based. i think it should work.

        Payload:

        {
            "symbol": "LTCBTC",
            "origClientOrderId": "myOrder1",
            "orderId": 4,
            "orderListId": -1, //Unless part of an OCO, the value will always be -1.
            "clientOrderId": "cancelMyOrder1",
            "price": "2.00000000",
            "origQty": "1.00000000",
            "executedQty": "0.00000000",
            "cummulativeQuoteQty": "0.00000000",
            "status": "CANCELED",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY"
        }
        '''
        response = self.__call_sync(self.request_impl.cancel_order(
            symbol, orderId, newClientOrderId))
        self.refresh_limits(response[1])
        return response[0]

    def cancel_all_orders(self, symbol: 'str') -> any:
        '''
        Cancel All Open Orders (TRADE)

        DELETE api/v3/openOrders

        Cancels all active orders on a symbol.
        This includes OCO orders.

        Note: Weird enough canceling all orders based on symbol does not require a signature based on 
        docs however requires the recvWindow and timestamp where are parameters needed with signature. 
        signature is added but not tested so we will see.

        Payload:

        [
            {
                "symbol": "BTCUSDT",
                "origClientOrderId": "E6APeyTJvkMvLMYMqu1KQ4",
                "orderId": 11,
                "orderListId": -1,
                "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
                "price": "0.089853",
                "origQty": "0.178622",
                "executedQty": "0.000000",
                "cummulativeQuoteQty": "0.000000",
                "status": "CANCELED",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY"
            },
            {
                "symbol": "BTCUSDT",
                "origClientOrderId": "A3EF2HCwxgZPFMrfwbgrhv",
                "orderId": 13,
                "orderListId": -1,
                "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
                "price": "0.090430",
                "origQty": "0.178622",
                "executedQty": "0.000000",
                "cummulativeQuoteQty": "0.000000",
                "status": "CANCELED",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY"
            },
            {
                "orderListId": 1929,
                "contingencyType": "OCO",
                "listStatusType": "ALL_DONE",
                "listOrderStatus": "ALL_DONE",
                "listClientOrderId": "2inzWQdDvZLHbbAmAozX2N",
                "transactionTime": 1585230948299,
                "symbol": "BTCUSDT",
                "orders": [
                {
                    "symbol": "BTCUSDT",
                    "orderId": 20,
                    "clientOrderId": "CwOOIPHSmYywx6jZX77TdL"
                },
                {
                    "symbol": "BTCUSDT",
                    "orderId": 21,
                    "clientOrderId": "461cPg51vQjV3zIMOXNz39"
                }
                ],
                "orderReports": [
                {
                    "symbol": "BTCUSDT",
                    "origClientOrderId": "CwOOIPHSmYywx6jZX77TdL",
                    "orderId": 20,
                    "orderListId": 1929,
                    "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
                    "price": "0.668611",
                    "origQty": "0.690354",
                    "executedQty": "0.000000",
                    "cummulativeQuoteQty": "0.000000",
                    "status": "CANCELED",
                    "timeInForce": "GTC",
                    "type": "STOP_LOSS_LIMIT",
                    "side": "BUY",
                    "stopPrice": "0.378131",
                    "icebergQty": "0.017083"
                },
                {
                    "symbol": "BTCUSDT",
                    "origClientOrderId": "461cPg51vQjV3zIMOXNz39",
                    "orderId": 21,
                    "orderListId": 1929,
                    "clientOrderId": "pXLV6Hz6mprAcVYpVMTGgx",
                    "price": "0.008791",
                    "origQty": "0.690354",
                    "executedQty": "0.000000",
                    "cummulativeQuoteQty": "0.000000",
                    "status": "CANCELED",
                    "timeInForce": "GTC",
                    "type": "LIMIT_MAKER",
                    "side": "BUY",
                    "icebergQty": "0.639962"
                }
                ]
            }
        ]
        '''
        response = self.__call_sync(
            self.request_impl.cancel_all_orders(symbol))
        self.refresh_limits(response[1])
        return response[0]

    def get_order(self, symbol: 'str', orderId: 'long' = None) -> any:
        '''
        Query Order (USER_DATA)

        GET /api/v3/order (HMAC SHA256)

        Check an order's status.

        Notes: For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        Payload:

        {
            "symbol": "LTCBTC",
            "orderId": 1,
            "orderListId": -1, //Unless OCO, value will be -1
            "clientOrderId": "myOrder1",
            "price": "0.1",
            "origQty": "1.0",
            "executedQty": "0.0",
            "cummulativeQuoteQty": "0.0",
            "status": "NEW",
            "timeInForce": "GTC",
            "type": "LIMIT",
            "side": "BUY",
            "stopPrice": "0.0",
            "icebergQty": "0.0",
            "time": 1499827319559,
            "updateTime": 1499827319559,
            "isWorking": true,
            "origQuoteOrderQty": "0.000000"
        }
        '''
        response = self.__call_sync(self.request_impl.get_order(
            symbol, orderId))
        self.refresh_limits(response[1])
        return response[0]

    def get_open_orders(self, symbol: 'str' = None) -> any:
        '''
        Current Open Orders (USER_DATA)

        GET /api/v3/openOrders (HMAC SHA256)

        Get all open orders on a symbol. Careful when accessing this with no symbol.

        Notes: If the symbol is not sent, orders for all symbols will be returned in an array.

        Payload:

        [
            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "orderListId": -1, //Unless OCO, the value will always be -1
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "cummulativeQuoteQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559,
                "updateTime": 1499827319559,
                "isWorking": true,
                "origQuoteOrderQty": "0.000000"
            }
        ]
        '''
        response = self.__call_sync(self.request_impl.get_open_orders(symbol))
        self.refresh_limits(response[1])
        return response[0]

    def get_all_orders(self, symbol: 'str', orderId: 'long' = None, startTime: 'long' = None,
                       endTime: 'long' = None, limit: 'int' = None) -> any:
        '''
        All Orders (USER_DATA)

        GET /api/v3/allOrders (HMAC SHA256)

        Get all account orders; active, canceled, or filled.

        Notes:
        1. If orderId is set, it will get orders >= that orderId. Otherwise most recent orders are returned.
        2. For some historical orders cummulativeQuoteQty will be < 0, meaning the data is not available at this time.

        Payload:

        [
            {
                "symbol": "LTCBTC",
                "orderId": 1,
                "orderListId": -1, //Unless OCO, the value will always be -1
                "clientOrderId": "myOrder1",
                "price": "0.1",
                "origQty": "1.0",
                "executedQty": "0.0",
                "cummulativeQuoteQty": "0.0",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT",
                "side": "BUY",
                "stopPrice": "0.0",
                "icebergQty": "0.0",
                "time": 1499827319559,
                "updateTime": 1499827319559,
                "isWorking": true,
                "origQuoteOrderQty": "0.000000"
            }
        ]
        '''
        response = self.__call_sync(self.request_impl.get_all_orders(
            symbol, orderId, startTime, endTime, limit))
        self.refresh_limits(response[1])
        return response[0]

    def post_oco_order(self, symbol: 'str', side: 'OrderSide', quantity: 'float' or str, price: 'float' or str,
                       stopPrice: 'float' or str, listClientOrderId: 'str' = None, limitClientOrderId: 'str' = None,
                       limitIcebergQty: 'float' = None, stopClientOrderId: 'str' = None,
                       stopLimitPrice: 'float' or str = None, stopIcebergQty: 'float' = None,
                       stopLimitTimeInForce: 'StopLimitTimeType' = StopLimitTimeType.INVALID,
                       newOrderRespType: 'OrderRespType' = OrderRespType.INVALID) -> OrderOCO:
        '''
        New OCO (TRADE)

        POST /api/v3/order/oco (HMAC SHA256)

        Send in a new OCO.

        Notes:
        1.Price Restrictions:
            * SELL: Limit Price > Last Price > Stop Price
            * BUY: Limit Price < Last Price < Stop Price
        2. Quantity Restrictions:
            * Both legs must have the same quantity
            * ICEBERG quantities however do not have to be the same.
        3. Order Rate Limit:
            * OCO counts as 2 orders against the order rate limit.

        Payload:

        {
            "orderListId": 0,
            "contingencyType": "OCO",
            "listStatusType": "EXEC_STARTED",
            "listOrderStatus": "EXECUTING",
            "listClientOrderId": "JYVpp3F0f5CAG15DhtrqLp",
            "transactionTime": 1563417480525,
            "symbol": "LTCBTC",
            "orders": [
                {
                "symbol": "LTCBTC",
                "orderId": 2,
                "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos"
                },
                {
                "symbol": "LTCBTC",
                "orderId": 3,
                "clientOrderId": "xTXKaGYd4bluPVp78IVRvl"
                }
            ],
            "orderReports": [
                {
                "symbol": "LTCBTC",
                "orderId": 2,
                "orderListId": 0,
                "clientOrderId": "Kk7sqHb9J6mJWTMDVW7Vos",
                "transactTime": 1563417480525,
                "price": "0.000000",
                "origQty": "0.624363",
                "executedQty": "0.000000",
                "cummulativeQuoteQty": "0.000000",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "STOP_LOSS",
                "side": "BUY",
                "stopPrice": "0.960664"
                },
                {
                "symbol": "LTCBTC",
                "orderId": 3,
                "orderListId": 0,
                "clientOrderId": "xTXKaGYd4bluPVp78IVRvl",
                "transactTime": 1563417480525,
                "price": "0.036435",
                "origQty": "0.624363",
                "executedQty": "0.000000",
                "cummulativeQuoteQty": "0.000000",
                "status": "NEW",
                "timeInForce": "GTC",
                "type": "LIMIT_MAKER",
                "side": "BUY"
                }
            ]
        }
        '''
        response = self.__call_sync(self.request_impl.post_oco_order(symbol, listClientOrderId, side,
                                                                     quantity, limitClientOrderId, price,
                                                                     limitIcebergQty, stopClientOrderId,
                                                                     stopPrice, stopLimitPrice, stopIcebergQty,
                                                                     stopLimitTimeInForce, newOrderRespType))
        self.refresh_limits(response[1])
        return response[0]

    def cancel_oco_order(self, symbol: 'str', orderListId: 'long' = None, listClientOrderId: 'str' = None, newClientOrderId: 'str' = None) -> any:
        '''
        Cancel OCO (TRADE)

        DELETE /api/v3/orderList (HMAC SHA256)

        Cancel an entire Order List

        Note: Canceling an individual leg will cancel the entire OCO.

        Payload:

        {
            "orderListId": 0,
            "contingencyType": "OCO",
            "listStatusType": "ALL_DONE",
            "listOrderStatus": "ALL_DONE",
            "listClientOrderId": "C3wyj4WVEktd7u9aVBRXcN",
            "transactionTime": 1574040868128,
            "symbol": "LTCBTC",
            "orders": [
                {
                "symbol": "LTCBTC",
                "orderId": 2,
                "clientOrderId": "pO9ufTiFGg3nw2fOdgeOXa"
                },
                {
                "symbol": "LTCBTC",
                "orderId": 3,
                "clientOrderId": "TXOvglzXuaubXAaENpaRCB"
                }
            ],
            "orderReports": [
                {
                "symbol": "LTCBTC",
                "origClientOrderId": "pO9ufTiFGg3nw2fOdgeOXa",
                "orderId": 2,
                "orderListId": 0,
                "clientOrderId": "unfWT8ig8i0uj6lPuYLez6",
                "price": "1.00000000",
                "origQty": "10.00000000",
                "executedQty": "0.00000000",
                "cummulativeQuoteQty": "0.00000000",
                "status": "CANCELED",
                "timeInForce": "GTC",
                "type": "STOP_LOSS_LIMIT",
                "side": "SELL",
                "stopPrice": "1.00000000"
                },
                {
                "symbol": "LTCBTC",
                "origClientOrderId": "TXOvglzXuaubXAaENpaRCB",
                "orderId": 3,
                "orderListId": 0,
                "clientOrderId": "unfWT8ig8i0uj6lPuYLez6",
                "price": "3.00000000",
                "origQty": "10.00000000",
                "executedQty": "0.00000000",
                "cummulativeQuoteQty": "0.00000000",
                "status": "CANCELED",
                "timeInForce": "GTC",
                "type": "LIMIT_MAKER",
                "side": "SELL"
                }
            ]
        }
        '''
        response = self.__call_sync(self.request_impl.cancel_oco_order(
            symbol, orderListId, listClientOrderId, newClientOrderId))
        self.refresh_limits(response[1])
        return response[0]

    def get_oco_order(self, orderListId: 'long' = None, origClientOrderId: 'str' = None) -> any:
        '''
        Query OCO (USER_DATA)

        GET /api/v3/orderList (HMAC SHA256)

        Retrieves a specific OCO based on provided optional parameters.

        Note: Either orderListId or listClientOrderId must be provided.

        Payload:

        {
            "orderListId": 27,
            "contingencyType": "OCO",
            "listStatusType": "EXEC_STARTED",
            "listOrderStatus": "EXECUTING",
            "listClientOrderId": "h2USkA5YQpaXHPIrkd96xE",
            "transactionTime": 1565245656253,
            "symbol": "LTCBTC",
            "orders": [
                {
                "symbol": "LTCBTC",
                "orderId": 4,
                "clientOrderId": "qD1gy3kc3Gx0rihm9Y3xwS"
                },
                {
                "symbol": "LTCBTC",
                "orderId": 5,
                "clientOrderId": "ARzZ9I00CPM8i3NhmU9Ega"
                }
            ]
        }
        '''
        response = self.__call_sync(self.request_impl.get_oco_order(
            orderListId, origClientOrderId))
        self.refresh_limits(response[1])
        return response[0]

    def get_all_oco_orders(self, fromId: 'long' = None, startTime: 'long' = None,
                           endTime: 'long' = None, limit: 'int' = None) -> any:
        '''
        Query all OCO (USER_DATA)

        GET /api/v3/allOrderList (HMAC SHA256)

        Retrieves all OCO based on provided optional parameters.

        Payload:

        [
            {
                "orderListId": 29,
                "contingencyType": "OCO",
                "listStatusType": "EXEC_STARTED",
                "listOrderStatus": "EXECUTING",
                "listClientOrderId": "amEEAXryFzFwYF1FeRpUoZ",
                "transactionTime": 1565245913483,
                "symbol": "LTCBTC",
                "orders": [
                {
                    "symbol": "LTCBTC",
                    "orderId": 4,
                    "clientOrderId": "oD7aesZqjEGlZrbtRpy5zB"
                },
                {
                    "symbol": "LTCBTC",
                    "orderId": 5,
                    "clientOrderId": "Jr1h6xirOxgeJOUuYQS7V3"
                }
                ]
            },
            {
                "orderListId": 28,
                "contingencyType": "OCO",
                "listStatusType": "EXEC_STARTED",
                "listOrderStatus": "EXECUTING",
                "listClientOrderId": "hG7hFNxJV6cZy3Ze4AUT4d",
                "transactionTime": 1565245913407,
                "symbol": "LTCBTC",
                "orders": [
                {
                    "symbol": "LTCBTC",
                    "orderId": 2,
                    "clientOrderId": "j6lFOfbmFMRjTYA7rRJ0LP"
                },
                {
                    "symbol": "LTCBTC",
                    "orderId": 3,
                    "clientOrderId": "z0KCjOdditiLS5ekAFtK81"
                }
                ]
            }
        ]
        '''
        response = self.__call_sync(self.request_impl.get_all_oco_orders(
            fromId, startTime, endTime, limit))
        self.refresh_limits(response[1])
        return response[0]

    def get_open_oco_orders(self) -> any:
        '''
        Query Open OCO (USER_DATA)

        GET /api/v3/openOrderList (HMAC SHA256)

        Payload:

        [
            {
                "orderListId": 31,
                "contingencyType": "OCO",
                "listStatusType": "EXEC_STARTED",
                "listOrderStatus": "EXECUTING",
                "listClientOrderId": "wuB13fmulKj3YjdqWEcsnp",
                "transactionTime": 1565246080644,
                "symbol": "1565246079109",
                "orders": [
                {
                    "symbol": "LTCBTC",
                    "orderId": 4,
                    "clientOrderId": "r3EH2N76dHfLoSZWIUw1bT"
                },
                {
                    "symbol": "LTCBTC",
                    "orderId": 5,
                    "clientOrderId": "Cv1SnyPD3qhqpbjpYEHbd2"
                }
                ]
            }
        ]
        '''
        response = self.__call_sync(self.request_impl.get_open_oco_orders())
        self.refresh_limits(response[1])
        return response[0]

    def get_account_information(self) -> AccountInformation:
        '''
        Account Information (USER_DATA)

        GET /api/v3/account (HMAC SHA256)

        Get current account information.

        Payload:

        {
            "makerCommission": 15,
            "takerCommission": 15,
            "buyerCommission": 0,
            "sellerCommission": 0,
            "canTrade": true,
            "canWithdraw": true,
            "canDeposit": true,
            "updateTime": 123456789,
            "accountType": "SPOT",
            "balances": [
                {
                "asset": "BTC",
                "free": "4723846.89208129",
                "locked": "0.00000000"
                },
                {
                "asset": "LTC",
                "free": "4763368.68006011",
                "locked": "0.00000000"
                }
            ],
            "permissions": [
                "SPOT"
            ]
        }
        '''
        response = self.__call_sync(
            self.request_impl.get_account_information())
        self.refresh_limits(response[1])
        return response[0]

    def get_account_trades(self, symbol: 'str', startTime: 'long' = None, endTime: 'long' = None, fromId: 'long' = None, limit: 'int' = None) -> any:
        '''
        Account Trade List (USER_DATA)

        GET /api/v3/myTrades (HMAC SHA256)

        Get trades for a specific account and symbol.

        Note: If fromId is set, it will get id >= that fromId. Otherwise most recent orders are returned.

        Payload:

       [
            {
                "symbol": "BNBBTC",
                "id": 28457,
                "orderId": 100234,
                "orderListId": -1, //Unless OCO, the value will always be -1
                "price": "4.00000100",
                "qty": "12.00000000",
                "quoteQty": "48.000012",
                "commission": "10.10000000",
                "commissionAsset": "BNB",
                "time": 1499865549590,
                "isBuyer": true,
                "isMaker": false,
                "isBestMatch": true
            }
        ]
        '''
        response = self.__call_sync(self.request_impl.get_account_trades(
            symbol, startTime, endTime, fromId, limit))
        self.refresh_limits(response[1])
        return response[0]

    def start_user_data_stream(self) -> any:
        '''
        Create a ListenKey (USER_STREAM)

        POST /api/v3/userDataStream

        Start a new user data stream. The stream will close after 60 minutes unless a keepalive is sent. 
        If the account has an active listenKey, that listenKey will be returned and its validity will 
        be extended for 60 minutes.

        Payload;

        {
            "listenKey": "pqia91ma19a5s61cv6a81va65sdf19v8a65a1a5s61cv6a81va65sdf19v8a65a1"
        }
        '''
        response = self.__call_sync(self.request_impl.start_user_data_stream())
        self.refresh_limits(response[1])
        return response[0]

    def keep_user_data_stream(self, listenKey: 'str') -> any:
        '''
        Ping/Keep-alive a ListenKey (USER_STREAM)

        PUT /api/v3/userDataStream

        Keepalive a user data stream to prevent a time out. User data streams will close after 60 minutes.
        It's recommended to send a ping about every 30 minutes.

        Payload:

        {}
        '''
        response = self.__call_sync(
            self.request_impl.keep_user_data_stream(listenKey))
        self.refresh_limits(response[1])
        return response[0]

    def close_user_data_stream(self, listenKey: 'str') -> any:
        '''
        Close a ListenKey (USER_STREAM)

        DELETE /api/v3/userDataStream

        Close out a user data stream.

        Payload:

        {}
        '''
        response = self.__call_sync(
            self.request_impl.close_user_data_stream(listenKey))
        self.refresh_limits(response[1])
        return response[0]
