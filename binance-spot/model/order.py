from common.scripts.binance_spot.impl.utils import JsonWrapper
from common.scripts.binance_spot.model.exchangeinformation import Symbol


class Fills:

    def __init__(self):
        self.price = 0.0
        self.qty = 0.0
        self.commission = 0.0
        self.commissionAsset = ''


class Orders:

    def __init__(self):
        self.symbol = ''
        self.orderId = 0
        self.clientOrderId = ''


class OrderReports:

    def __init__(self):
        self.symbol = ''
        self.origClientOrderId = ''
        self.orderId = 0
        self.orderListId = 0
        self.clientOrderId = ''
        self.price = 0.0
        self.origQty = 0.0
        self.executedQty = 0.0
        self.cummulativeQuoteQty = 0.0
        self.status = ''
        self.timeInForce = ''
        self.type = ''
        self.side = ''
        self.stopPrice = 0.0
        self.icebergQty = 0.0


class Order:

    def __init__(self):
        self.symbol = ''
        self.origClientOrderId = ''
        self.orderId = 0
        self.orderListId = 0
        self.contingencyType = ''
        self.listStatusType = ''
        self.listOrderStatus = ''
        self.listClientOrderId = ''
        self.transactionTime = 0
        self.clientOrderId = ''
        self.transactTime = 0
        self.price = 0.0
        self.origQty = 0.0
        self.executedQty = 0.0
        self.cummulativeQuoteQty = 0.0
        self.status = ''
        self.timeInForce = ''
        self.type = ''
        self.side = ''
        self.stopPrice = 0.0
        self.icebergQty = 0.0
        self.time = 0
        self.updateTime = 0
        self.isWorking = False
        self.origQuoteOrderQty = 0.0
        self.fills = list()
        self.orders = list()
        self.orderReports = list()

    @staticmethod
    def json_parse(json_data: JsonWrapper):
        result = Order()
        result.symbol = json_data.get_string_or_default('symbol', '')
        result.origClientOrderId = json_data.get_string_or_default('origClientOrderId', '')
        result.orderId = json_data.get_int_or_default('orderId', 0)
        result.orderListId = json_data.get_int_or_default('orderListId', 0)
        result.contingencyType = json_data.get_string_or_default('contingencyType', '')
        result.listStatusType = json_data.get_string_or_default('listStatusType', '')
        result.listOrderStatus = json_data.get_string_or_default('listOrderStatus', '')
        result.listClientOrderId = json_data.get_string_or_default('listClientOrderId', '')
        result.transactionTime = json_data.get_int_or_default('transactionTime', 0)
        result.clientOrderId = json_data.get_string_or_default('clientOrderId', '')
        result.transactTime = json_data.get_int_or_default('transactTime', 0)
        result.price = json_data.get_float_or_default('price', 0.0)
        result.origQty = json_data.get_float_or_default('origQty', 0.0)
        result.executedQty = json_data.get_float_or_default('executedQty', 0.0)
        result.cummulativeQuoteQty = json_data.get_float_or_default('cummulativeQuoteQty', 0.0)
        result.status = json_data.get_string_or_default('status', '')
        result.timeInForce = json_data.get_string_or_default('timeInForce', '')
        result.type = json_data.get_string_or_default('type', '')
        result.side = json_data.get_string_or_default('side', '')
        result.stopPrice = json_data.get_float_or_default('stopPrice', 0.0)
        result.icebergQty = json_data.get_float_or_default('icebergQty', 0.0)
        result.time = json_data.get_int_or_default('time', 0)
        result.updateTime = json_data.get_int_or_default('updateTime', 0)
        result.isWorking = json_data.get_boolean_or_default('isWorking', False)
        result.origQuoteOrderQty = json_data.get_float_or_default('origQuoteOrderQty', 0.0)

        data_list = json_data.get_array_or_default('fills')
        element_list = list()
        for item in data_list.get_items():
            element = Symbol()
            element.price = item.get_float_or_default('price', 0.0)
            element.qty = item.get_float_or_default('qty', 0.0)
            element.commission = item.get_float_or_default('commission', 0.0)
            element.commissionAsset = item.get_string_or_default('commissionAsset', '')

            element_list.append(element)
        result.fills = element_list

        data_list = json_data.get_array_or_default('orders')
        element_list = list()
        for item in data_list.get_items():
            element = Orders()
            element.symbol = item.get_string_or_default('symbol', '')
            element.orderId = item.get_int_or_default('orderId', 0)
            element.clientOrderId = item.get_string_or_default('clientOrderId', '')

            element_list.append(element)
        result.orders = element_list

        data_list = json_data.get_array_or_default('orderReports')
        element_list = list()
        for item in data_list.get_items():
            element = Orders()
            element.symbol = item.get_string_or_default('symbol', '')
            element.origClientOrderId = item.get_string_or_default('origClientOrderId', '')
            element.orderId = item.get_int_or_default('orderId', 0)
            element.orderListId = item.get_int_or_default('orderListId', 0)
            element.clientOrderId = item.get_string_or_default('clientOrderId', '')
            element.price = item.get_float_or_default('price', 0.0)
            element.origQty = item.get_float_or_default('origQty', 0.0)
            element.executedQty = item.get_float_or_default('executedQty', 0.0)
            element.cummulativeQuoteQty = item.get_float_or_default('cummulativeQuoteQty', 0.0)
            element.status = item.get_string_or_default('status', '')
            element.timeInForce = item.get_string_or_default('timeInForce', '')
            element.type = item.get_string_or_default('type', '')
            element.side = item.get_string_or_default('side', '')
            element.stopPrice = item.get_string_or_default('stopPrice', '')
            element.icebergQty = item.get_float_or_default('icebergQty', 0.0)

            element_list.append(element)
        result.orderReports = element_list

        return result
