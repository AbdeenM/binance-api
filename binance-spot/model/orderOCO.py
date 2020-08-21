from common.scripts.binance_spot.impl.utils import JsonWrapper
from common.scripts.binance_spot.model import Order

class Orders:

    def __init__(self):
        self.symbol = ''
        self.orderId = 0
        self.clientOrderId = ''


class OrderReports:

    def __init__(self):
        self.symbol = ''
        self.orderId = 0
        self.orderListId = 0
        self.clientOrderId = ''
        self.transactionTime = 0
        self.price = 0.0
        self.origQty = 0.0
        self.executedQty = 0.0
        self.cummulativeQuoteQty = 0.0
        self.status = ''
        self.timeInForce = ''
        self.type = ''
        self.side = ''
        self.stopPrice = 0.0


class OrderOCO:

    def __init__(self):
        self.orderListId = 0
        self.contingencyType = ''
        self.listStatusType = ''
        self.listOrderStatus = ''
        self.listClientOrderId = ''
        self.transactionTime = 0
        self.symbol = ''
        self.orders = list()
        self.orderRexports = list()

    @staticmethod
    def json_parse(json_data: JsonWrapper):
        result = Order()
        result.orderListId = json_data.get_int_or_default('orderListId', 0)
        result.contingencyType = json_data.get_string_or_default('contingencyType', '')
        result.listStatusType = json_data.get_string_or_default('listStatusType', '')
        result.listOrderStatus = json_data.get_string_or_default('listOrderStatus', '')
        result.listClientOrderId = json_data.get_string_or_default('listClientOrderId', '')
        result.transactionTime = json_data.get_int_or_default('transactionTime', 0)
        result.symbol = json_data.get_string_or_default('symbol', '')

        data_list = json_data.get_array('orders')
        element_list = list()
        for item in data_list.get_items():
            element = Orders()
            element.symbol = item.get_string_or_default('symbol', '')
            element.orderId = item.get_int_or_default('orderId', 0)
            element.clientOrderId = item.get_string_or_default('clientOrderId', '')
            element_list.append(element)
        result.orders = element_list

        data_list = json_data.get_array('orderReports')
        element_list = list()
        for item in data_list.get_items():
            element = Orders()
            element.symbol = item.get_string_or_default('symbol', '')
            element.orderId = item.get_int_or_default('orderId', 0)
            element.orderListId = item.get_int_or_default('orderListId', 0)
            element.clientOrderId = item.get_string_or_default('clientOrderId', '')
            element.transactionTime = item.get_int_or_default('transactionTime', 0)
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
        result.orders = element_list

        return result
