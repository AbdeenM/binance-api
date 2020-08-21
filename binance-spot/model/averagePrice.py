class AveragePrice:

    def __init__(self):
        self.mins = 0
        self.price = 0.0

    @staticmethod
    def json_parse(json_wrapper):
        result = AveragePrice()
        result.mins = json_wrapper.get_int('mins')
        result.price = json_wrapper.get_float('price')
        return result
