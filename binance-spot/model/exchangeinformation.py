import json

from common.scripts.binance_spot.impl.utils import JsonWrapper


class RateLimit:

    def __init__(self):
        self.rateLimitType = ''
        self.interval = ''
        self.intervalNum = 0
        self.limit = 0


class ExchangeFilter:

    def __init__(self):
        self.filterType = ''
        self.maxOrders = 0


class Symbol:

    def __init__(self):
        self.symbol = ''
        self.status = ''
        self.baseAsset = ''
        self.baseAssetPrecision = 0
        self.quoteAsset = ''
        self.quotePrecision = 0
        self.quoteAssetPrecision = 0
        self.orderTypes = list()
        self.icebergAllowed = False
        self.ocoAllowed = False
        self.isSpotTradingAllowed = False
        self.isMarginTradingAllowed = False
        self.filters = list()
        self.permissions = list()


class ExchangeInformation:

    def __init__(self):
        self.timezone = ''
        self.serverTime = 0
        self.rateLimits = list()
        self.exchangeFilters = list()
        self.symbols = list()

    @staticmethod
    def json_parse(json_data: JsonWrapper):
        result = ExchangeInformation()
        result.timezone = json_data.get_string('timezone')
        result.serverTime = json_data.get_int('serverTime')

        data_list = json_data.get_array('rateLimits')
        element_list = list()
        for item in data_list.get_items():
            element = RateLimit()
            element.rateLimitType = item.get_string('rateLimitType')
            element.interval = item.get_string('interval')
            element.intervalNum = item.get_int('intervalNum')
            element.limit = item.get_int('limit')

            element_list.append(element)
        result.rateLimits = element_list

        data_list = json_data.get_array('exchangeFilters')
        element_list = list()
        for item in data_list.get_items():
            element = ExchangeFilter()
            element.filterType = item.get_string('filterType')
            if element.filterType == 'EXCHANGE_MAX_NUM_ORDERS':
                element.maxNumOrders = item.get_int('maxNumOrders')
            elif element.filterType == 'EXCHANGE_MAX_ALGO_ORDERS':
                element.maxNumAlgoOrders = item.get_int('maxNumAlgoOrders')

            element_list.append(element)
        result.exchangeFilters = element_list

        data_list = json_data.get_array('symbols')
        element_list = list()
        for item in data_list.get_items():
            element = Symbol()
            element.symbol = item.get_string('symbol')
            element.status = item.get_string('status')
            element.baseAsset = item.get_string('baseAsset')
            element.baseAssetPrecision = item.get_int('baseAssetPrecision')
            element.quoteAsset = item.get_string('quoteAsset')
            element.quotePrecision = item.get_int('quotePrecision')
            element.quoteAssetPrecision = item.get_int('quoteAssetPrecision')
            element.orderTypes = item.get_object('orderTypes').convert_2_list()
            element.icebergAllowed = item.get_boolean('icebergAllowed')
            element.ocoAllowed = item.get_boolean('ocoAllowed')
            element.isSpotTradingAllowed = item.get_boolean(
                'isSpotTradingAllowed')
            element.isMarginTradingAllowed = item.get_boolean(
                'isMarginTradingAllowed')

            val_list = item.get_array('filters')
            filter_list = list()
            for jtem in val_list.get_items():
                filter_list.append(jtem.convert_2_dict())
            element.filters = filter_list

            element_list.append(element)
        result.symbols = element_list

        result.permissions = json_data.get_object_or_default('permissions', JsonWrapper(json.loads('[]'))).convert_2_list()

        return result
