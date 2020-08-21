class MyTrade:

    def __init__(self):
        self.symbol = ''
        self.id = 0
        self.orderId = 0
        self.orderListId = 0
        self.price = 0.0
        self.qty = 0.0
        self.quoteQty = 0.0
        self.commission = 0.0
        self.commissionAsset = ''
        self.time = 0
        self.isBuyer = False
        self.isMaker = False
        self.isBestMatch = None

    @staticmethod
    def json_parse(json_data):
        result = MyTrade()
        result.symbol = json_data.get_string('symbol')
        result.id = json_data.get_int('id')
        result.orderId = json_data.get_int('orderId')
        result.orderListId = json_data.get_int('orderListId')
        result.price = json_data.get_float('price')
        result.qty = json_data.get_float('qty')
        result.quoteQty = json_data.get_float('quoteQty')
        result.commission = json_data.get_float('commission')
        result.commissionAsset = json_data.get_string('commissionAsset')
        result.time = json_data.get_int('time')
        result.isBuyer = json_data.get_boolean('buyer')
        result.isMaker = json_data.get_boolean('maker')
        result.isBestMatch = json_data.get_boolean('isBestMatch')

        return result
