from common.scripts.binance_spot.impl import RestApiRequest
from common.scripts.binance_spot.impl.utils.urlparamsbuilder import UrlParamsBuilder
from common.scripts.binance_spot.impl.utils.apisignature import create_signature
from common.scripts.binance_spot.impl.utils.inputchecker import *
from common.scripts.binance_spot.impl.utils.timeservice import *
from common.scripts.binance_spot.model import *
# For develop
from common.scripts.binance_spot.base.printobject import *


class RestApiRequestImpl(object):

    def __init__(self, api_key, secret_key, server_url='https://api.binance.com', debug=False):
        self.__api_key = api_key
        self.__secret_key = secret_key
        self.__server_url = server_url
        self.__debug = debug

    def __create_request_by_get(self, url, builder):
        request = RestApiRequest()
        request.method = 'GET'
        request.host = self.__server_url
        request.header.update({'Content-Type': 'application/json'})
        request.url = url + '?' + builder.build_url()

        if self.__debug == True:
            print('====== Request ======')
            print(request)
            PrintMix.print_data(request)
            print('=====================')
        return request

    def __create_request_by_get_with_apikey(self, url, builder):
        request = RestApiRequest()
        request.method = 'GET'
        request.host = self.__server_url
        request.header.update({'Content-Type': 'application/json'})
        request.header.update({'X-MBX-APIKEY': self.__api_key})
        request.url = url + '?' + builder.build_url()

        if self.__debug == True:
            print('====== Request ======')
            print(request)
            PrintMix.print_data(request)
            print('=====================')
        return request

    def __create_request_by_post_with_signature(self, url, builder):
        request = RestApiRequest()
        request.method = 'POST'
        request.host = self.__server_url
        builder.put_url('recvWindow', 60000)
        builder.put_url('timestamp', str(get_current_timestamp() - 1000))
        create_signature(self.__secret_key, builder)
        request.header.update({'Content-Type': 'application/json'})
        request.header.update({'X-MBX-APIKEY': self.__api_key})
        request.post_body = builder.post_map
        request.url = url + '?' + builder.build_url()

        if self.__debug == True:
            print('====== Request ======')
            print(request)
            PrintMix.print_data(request)
            print('=====================')
        return request

    def __create_request_by_delete_with_signature(self, url, builder):
        request = RestApiRequest()
        request.method = 'DELETE'
        request.host = self.__server_url
        builder.put_url('recvWindow', 60000)
        builder.put_url('timestamp', str(get_current_timestamp() - 1000))
        create_signature(self.__secret_key, builder)
        request.header.update({'Content-Type': 'application/json'})
        request.header.update({'X-MBX-APIKEY': self.__api_key})
        request.url = url + '?' + builder.build_url()

        if self.__debug == True:
            print('====== Request ======')
            print(request)
            PrintMix.print_data(request)
            print('=====================')
        return request

    def __create_request_by_get_with_signature(self, url, builder):
        request = RestApiRequest()
        request.method = 'GET'
        request.host = self.__server_url
        builder.put_url('recvWindow', 60000)
        builder.put_url('timestamp', str(get_current_timestamp() - 1000))
        create_signature(self.__secret_key, builder)
        request.header.update(
            {'Content-Type': 'application/x-www-form-urlencoded'})
        request.header.update({'X-MBX-APIKEY': self.__api_key})
        request.url = url + '?' + builder.build_url()

        if self.__debug == True:
            print('====== Request ======')
            print(request)
            PrintMix.print_data(request)
            print('=====================')
        return request

    def __create_request_by_put_with_signature(self, url, builder):
        request = RestApiRequest()
        request.method = 'PUT'
        request.host = self.__server_url
        builder.put_url('recvWindow', 60000)
        builder.put_url('timestamp', str(get_current_timestamp() - 1000))
        create_signature(self.__secret_key, builder)
        request.header.update({'Content-Type': 'application/json'})
        request.header.update({'X-MBX-APIKEY': self.__api_key})
        request.url = url + '?' + builder.build_url()

        if self.__debug == True:
            print('====== Request ======')
            print(request)
            PrintMix.print_data(request)
            print('=====================')
        return request

    def test_connectivity(self):
        builder = UrlParamsBuilder()
        request = self.__create_request_by_get('/api/v3/ping', builder)

        def parse(json_wrapper):
            result = 'OK'
            return result

        request.json_parser = parse
        return request

    def get_servertime(self):
        builder = UrlParamsBuilder()
        request = self.__create_request_by_get('/api/v3/time', builder)

        def parse(json_wrapper):
            result = json_wrapper.get_int('serverTime')
            return result

        request.json_parser = parse
        return request

    def get_exchange_information(self):
        builder = UrlParamsBuilder()
        request = self.__create_request_by_get(
            '/api/v3/exchangeInfo', builder)

        def parse(json_wrapper):
            result = ExchangeInformation.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_order_book(self, symbol, limit):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('limit', limit)

        request = self.__create_request_by_get('/api/v3/depth', builder)

        def parse(json_wrapper):
            result = OrderBook.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_recent_trades_list(self, symbol, limit):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('limit', limit)

        request = self.__create_request_by_get('/api/v3/trades', builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Trade.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_old_trade_lookup(self, symbol, limit, fromId):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('limit', limit)
        builder.put_url('fromId', fromId)

        request = self.__create_request_by_get_with_apikey(
            '/api/v3/historicalTrades', builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Trade.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_aggregate_trades_list(self, symbol, fromId, startTime, endTime, limit):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('fromId', fromId)
        builder.put_url('startTime', startTime)
        builder.put_url('endTime', endTime)
        builder.put_url('limit', limit)

        request = self.__create_request_by_get('/api/v3/aggTrades', builder)

        def parse(json_wrapper):
            aggregate_trades_list = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                trade = AggregateTrade.json_parse(item)
                aggregate_trades_list.append(trade)
            return aggregate_trades_list

        request.json_parser = parse
        return request

    def get_candlestick_data(self, symbol, interval, startTime, endTime, limit):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(symbol, 'interval')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('interval', interval)
        builder.put_url('startTime', startTime)
        builder.put_url('endTime', endTime)
        builder.put_url('limit', limit)

        request = self.__create_request_by_get('/api/v3/klines', builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Candlestick.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_current_average_price(self, symbol):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)

        request = self.__create_request_by_get(
            '/api/v3/avgPrice', builder)

        def parse(json_wrapper):
            result = AveragePrice.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_ticker_price_change_statistics(self, symbol):
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)

        request = self.__create_request_by_get('/api/v3/ticker/24hr', builder)

        def parse(json_wrapper):
            result = list()

            if symbol:
                element = TickerPriceChangeStatistics.json_parse(json_wrapper)
                result.append(element)
            else:
                data_list = json_wrapper.convert_2_array()
                for item in data_list.get_items():
                    element = TickerPriceChangeStatistics.json_parse(item)
                    result.append(element)

            return result

        request.json_parser = parse
        return request

    def get_symbol_price_ticker(self, symbol):
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)

        request = self.__create_request_by_get(
            '/api/v3/ticker/price', builder)

        def parse(json_wrapper):
            result = list()

            if symbol:
                element = SymbolPrice.json_parse(json_wrapper)
                result.append(element)
            else:
                data_list = json_wrapper.convert_2_array()
                for item in data_list.get_items():
                    element = SymbolPrice.json_parse(item)
                    result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_symbol_orderbook_ticker(self, symbol):
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)

        request = self.__create_request_by_get(
            '/api/v3/ticker/bookTicker', builder)

        def parse(json_wrapper):
            result = list()

            if symbol:
                element = SymbolOrderBook.json_parse(json_wrapper)
                result.append(element)
            else:
                data_list = json_wrapper.convert_2_array()
                for item in data_list.get_items():
                    element = SymbolOrderBook.json_parse(item)
                    result.append(element)
            return result

        request.json_parser = parse
        return request

    def post_test_order(self, symbol, side, ordertype,
                        timeInForce, quantity, quoteOrderQty, price,
                        newClientOrderId, stopPrice, icebergQty, newOrderRespType):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(side, 'side')
        check_should_not_none(ordertype, 'ordertype')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('side', side)
        builder.put_url('type', ordertype)
        builder.put_url('timeInForce', timeInForce)
        builder.put_url('quantity', quantity)
        builder.put_url('quoteOrderQty', quoteOrderQty)
        builder.put_url('price', price)
        builder.put_url('newClientOrderId', newClientOrderId)
        builder.put_url('stopPrice', stopPrice)
        builder.put_url('icebergQty', icebergQty)
        builder.put_url('newOrderRespType', newOrderRespType)

        request = self.__create_request_by_post_with_signature(
            '/api/v3/order/test', builder)

        def parse(json_wrapper):
            result = 'OK'
            return result

        request.json_parser = parse
        return request

    def post_order(self, symbol, side, ordertype,
                   timeInForce, quantity, quoteOrderQty, price,
                   newClientOrderId, stopPrice, icebergQty, newOrderRespType):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(side, 'side')
        check_should_not_none(ordertype, 'ordertype')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('side', side)
        builder.put_url('type', ordertype)
        builder.put_url('timeInForce', timeInForce)
        builder.put_url('quantity', quantity)
        builder.put_url('quoteOrderQty', quoteOrderQty)
        builder.put_url('price', price)
        builder.put_url('newClientOrderId', newClientOrderId)
        builder.put_url('stopPrice', stopPrice)
        builder.put_url('icebergQty', icebergQty)
        builder.put_url('newOrderRespType', newOrderRespType)

        request = self.__create_request_by_post_with_signature(
            '/api/v3/order', builder)

        def parse(json_wrapper):
            result = Order.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def cancel_order(self, symbol, orderId, newClientOrderId):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('orderId', orderId)
        builder.put_url('newClientOrderId', newClientOrderId)

        request = self.__create_request_by_delete_with_signature(
            '/api/v3/order', builder)

        def parse(json_wrapper):
            result = Order.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def cancel_all_orders(self, symbol):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)

        request = self.__create_request_by_delete_with_signature(
            'api/v3/openOrders', builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Order.json_parse(item)
                result.append(element)

            return result

        request.json_parser = parse
        return request

    def get_order(self, symbol, orderId):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('orderId', orderId)

        request = self.__create_request_by_get_with_signature(
            '/api/v3/order', builder)

        def parse(json_wrapper):
            result = Order.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_open_orders(self, symbol):
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)

        request = self.__create_request_by_get_with_signature(
            '/api/v3/openOrders', builder)

        def parse(json_wrapper):
            result = list()

            if symbol:
                element = Order.json_parse(json_wrapper)
                result.append(element)
            else:
                data_list = json_wrapper.convert_2_array()
                for item in data_list.get_items():
                    element = Order.json_parse(item)
                    result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_all_orders(self, symbol, orderId, startTime, endTime, limit):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('orderId', orderId)
        builder.put_url('startTime', startTime)
        builder.put_url('endTime', endTime)
        builder.put_url('limit', limit)

        request = self.__create_request_by_get_with_signature(
            '/api/v3/allOrders', builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = Order.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def post_oco_order(self, symbol, listClientOrderId, side,
                       quantity, limitClientOrderId, price,
                       limitIcebergQty, stopClientOrderId,
                       stopPrice, stopLimitPrice, stopIcebergQty,
                       stopLimitTimeInForce, newOrderRespType):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(side, 'side')
        check_should_not_none(quantity, 'quantity')
        check_should_not_none(price, 'price')
        check_should_not_none(stopPrice, 'stopPrice')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('listClientOrderId', listClientOrderId)
        builder.put_url('side', side)
        builder.put_url('quantity', quantity)
        builder.put_url('limitClientOrderId', limitClientOrderId)
        builder.put_url('price', price)
        builder.put_url('limitIcebergQty', limitIcebergQty)
        builder.put_url('stopClientOrderId', stopClientOrderId)
        builder.put_url('stopPrice', stopPrice)
        builder.put_url('stopLimitPrice', stopLimitPrice)
        builder.put_url('stopIcebergQty', stopIcebergQty)
        builder.put_url('stopLimitTimeInForce', stopLimitTimeInForce)
        builder.put_url('newOrderRespType', newOrderRespType)

        request = self.__create_request_by_post_with_signature(
            '/api/v3/order/oco', builder)

        def parse(json_wrapper):
            result = OrderOCO.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def cancel_oco_order(self, symbol, orderListId, listClientOrderId, newClientOrderId):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('orderListId', orderListId)
        builder.put_url('listClientOrderId', listClientOrderId)
        builder.put_url('newClientOrderId', newClientOrderId)

        request = self.__create_request_by_delete_with_signature(
            '/api/v3/order', builder)

        def parse(json_wrapper):
            result = OrderOCO.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_oco_order(self, orderListId, origClientOrderId):
        builder = UrlParamsBuilder()
        builder.put_url('orderListId', symbol)
        builder.put_url('origClientOrderId', orderId)

        request = self.__create_request_by_get_with_signature(
            '/api/v3/orderList', builder)

        def parse(json_wrapper):
            result = OrderOCO.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_all_oco_orders(self, fromId, startTime, endTime, limit):
        builder = UrlParamsBuilder()
        builder.put_url('fromId', fromId)
        builder.put_url('startTime', startTime)
        builder.put_url('endTime', endTime)
        builder.put_url('limit', limit)

        request = self.__create_request_by_get_with_signature(
            '/api/v3/allOrderList', builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = OrderOCO.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_open_oco_orders(self):
        builder = UrlParamsBuilder()

        request = self.__create_request_by_get_with_signature(
            '/api/v3/openOrderList', builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = OrderOCO.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def get_account_information(self):
        builder = UrlParamsBuilder()

        request = self.__create_request_by_get_with_signature(
            '/api/v3/account', builder)

        def parse(json_wrapper):
            result = AccountInformation.json_parse(json_wrapper)
            return result

        request.json_parser = parse
        return request

    def get_account_trades(self, symbol, startTime, endTime, fromId, limit):
        check_should_not_none(symbol, 'symbol')
        builder = UrlParamsBuilder()
        builder.put_url('symbol', symbol)
        builder.put_url('startTime', startTime)
        builder.put_url('endTime', endTime)
        builder.put_url('fromId', fromId)
        builder.put_url('limit', limit)

        request = self.__create_request_by_get_with_signature(
            '/api/v3/myTrades', builder)

        def parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = MyTrade.json_parse(item)
                result.append(element)
            return result

        request.json_parser = parse
        return request

    def start_user_data_stream(self):
        builder = UrlParamsBuilder()

        request = self.__create_request_by_post_with_signature(
            '/api/v3/userDataStream', builder)

        def parse(json_wrapper):
            result = json_wrapper.get_string('listenKey')
            return result

        request.json_parser = parse
        return request

    def keep_user_data_stream(self, listenKey):
        check_should_not_none(listenKey, 'listenKey')
        builder = UrlParamsBuilder()
        builder.put_url('listenKey', listenKey)

        request = self.__create_request_by_put_with_signature(
            '/api/v3/userDataStream', builder)

        def parse(json_wrapper):
            result = 'OK'
            return result

        request.json_parser = parse
        return request

    def close_user_data_stream(self, listenKey):
        check_should_not_none(listenKey, 'listenKey')
        builder = UrlParamsBuilder()
        builder.put_url('listenKey', listenKey)

        request = self.__create_request_by_delete_with_signature(
            '/api/v3/userDataStream', builder)

        def parse(json_wrapper):
            result = 'OK'
            return result

        request.json_parser = parse
        return request
