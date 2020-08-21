class Trade:

    def __init__(self):
        self.id = 0
        self.price = 0.0
        self.qty = 0.0
        self.quoteQty = 0.0
        self.time = 0
        self.isBuyerMaker = False
        self.isBestMatch = False

    @staticmethod
    def json_parse(json_data):
        result = Trade()
        result.id = json_data.get_int('id')
        result.price = json_data.get_float('price')
        result.qty = json_data.get_float('qty')
        result.quoteQty = json_data.get_float('quoteQty')
        result.time = json_data.get_int('time')
        result.isBuyerMaker = json_data.get_boolean('isBuyerMaker')
        result.isBestMatch = json_data.get_boolean('isBestMatch')

        return result
