class AggregateTradeEvent:

    def __init__(self):
        self.eventType = ''
        self.eventTime = 0
        self.symbol = ''
        self.id = 0
        self.price = 0.0
        self.qty = 0
        self.firstId = 0
        self.lastId = 0
        self.time = 0
        self.isBuyerMaker = False
        self.ignore = False

    @staticmethod
    def json_parse(json_wrapper):
        result = AggregateTradeEvent()
        result.eventType = json_wrapper.get_string('e')
        result.eventTime = json_wrapper.get_int('E')
        result.symbol = json_wrapper.get_string('s')
        result.id = json_wrapper.get_int('a')
        result.price = json_wrapper.get_float('p')
        result.qty = json_wrapper.get_float('q')
        result.firstId = json_wrapper.get_int('f')
        result.lastId = json_wrapper.get_int('l')
        result.time = json_wrapper.get_int('T')
        result.isBuyerMaker = json_wrapper.get_boolean('m')
        result.ignore = json_wrapper.get_boolean('M')
        return result
