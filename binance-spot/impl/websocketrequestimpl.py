import time
from common.scripts.binance_spot.impl.websocketrequest import WebsocketRequest
from common.scripts.binance_spot.impl.utils.channels import *
from common.scripts.binance_spot.impl.utils.timeservice import *
from common.scripts.binance_spot.impl.utils.inputchecker import *
from common.scripts.binance_spot.model import *
# For develop
from common.scripts.binance_spot.base.printobject import *


class WebsocketRequestImpl(object):

    def __init__(self, api_key):
        self.__api_key = api_key

    def subscribe_aggregate_trade_event(self, symbol, callback, error_handler=None):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(aggregate_trade_channel(symbol))
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = AggregateTradeEvent.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_trade_event(self, symbol, callback, error_handler=None):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(rade_channel(symbol))
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = TradeEvent.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_candlestick_event(self, symbol, interval, callback, error_handler=None):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(interval, 'interval')
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(kline_channel(symbol, interval))
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = CandlestickEvent.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_symbol_miniticker_event(self, symbol, callback, error_handler=None):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(symbol_miniticker_channel(symbol))
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = SymbolMiniTickerEvent.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_all_miniticker_event(self, callback, error_handler=None):
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(all_miniticker_channel())
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                element = SymbolMiniTickerEvent.json_parse(item)
            result.append(element)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_symbol_ticker_event(self, symbol, callback, error_handler=None):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(symbol_ticker_channel(symbol))
            time.sleep(0.02)

        def json_parse(json_wrapper):
            result = SymbolTickerEvent.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_all_ticker_event(self, callback, error_handler=None):
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(all_ticker_channel())
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = list()
            data_list = json_wrapper.convert_2_array()
            for item in data_list.get_items():
                ticker_event_obj = SymbolTickerEvent.json_parse(item)
            result.append(ticker_event_obj)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_symbol_bookticker_event(self, symbol, callback, error_handler=None):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(symbol_bookticker_channel(symbol))
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = SymbolBookTickerEvent.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_all_bookticker_event(self, callback, error_handler=None):
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(all_bookticker_channel())
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = SymbolBookTickerEvent.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_book_depth_event(self, symbol, limit, update_time, callback, error_handler=None):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(limit, 'limit')
        check_should_not_none(callback, 'callback')
        # print(update_time)

        def subscription_handler(connection):
            connection.send(book_depth_channel(symbol, limit, update_time))
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = OrderBookEvent.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_diff_depth_event(self, symbol, update_time, callback, error_handler=None):
        check_should_not_none(symbol, 'symbol')
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(diff_depth_channel(symbol, update_time))
            time.sleep(0.01)

        def json_parse(json_wrapper):
            result = DiffDepthEvent.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request

    def subscribe_user_data_event(self, listenKey, callback, error_handler=None):
        check_should_not_none(listenKey, 'listenKey')
        check_should_not_none(callback, 'callback')

        def subscription_handler(connection):
            connection.send(user_data_channel(listenKey))
            time.sleep(0.01)

        def json_parse(json_wrapper):
            print('event type: ', json_wrapper.get_string('e'))
            print(json_wrapper)
            if(json_wrapper.get_string('e') == 'ACCOUNT_UPDATE'):
                result = AccountUpdate.json_parse(json_wrapper)
            elif(json_wrapper.get_string('e') == 'ORDER_TRADE_UPDATE'):
                result = OrderUpdate.json_parse(json_wrapper)
            elif(json_wrapper.get_string('e') == 'listenKeyExpired'):
                result = ListenKeyExpired.json_parse(json_wrapper)
            return result

        request = WebsocketRequest()
        request.subscription_handler = subscription_handler
        request.json_parser = json_parse
        request.update_callback = callback
        request.error_handler = error_handler

        return request
