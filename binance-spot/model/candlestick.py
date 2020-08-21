class Candlestick:

    def __init__(self):
        self.openTime = 0
        self.open = 0.0
        self.high = 0.0
        self.low = 0.0
        self.close = 0.0
        self.volume = 0.0
        self.closeTime = 0
        self.quoteAssetVolume = 0.0
        self.numTrades = 0
        self.takerBuyBaseAssetVolume = 0.0
        self.takerBuyQuoteAssetVolume = 0.0
        self.ignore = 0.0

    def to_list(self):
        return [
            self.openTime,
            self.open,
            self.high,
            self.low,
            self.close,
            self.volume,
            self.closeTime,
            self.quoteAssetVolume,
            self.numTrades,
            self.takerBuyBaseAssetVolume,
            self.takerBuyQuoteAssetVolume,
            self.ignore,
        ]

    @staticmethod
    def json_parse_dict(val):
        result = Candlestick()
        result.openTime = val['t']
        result.open = val['o']
        result.high = val['h']
        result.low = val['l']
        result.close = val['c']
        result.volume = val['v']
        result.closeTime = val['T']
        result.quoteAssetVolume = val['q']
        result.numTrades = val['n']
        result.takerBuyBaseAssetVolume = val['V']
        result.takerBuyQuoteAssetVolume = val['Q']
        result.ignore = val['B']

        return result

    @staticmethod
    def json_parse(json_data):
        result = Candlestick()
        val = json_data.convert_2_list()
        result.openTime = val[0]
        result.open = val[1]
        result.high = val[2]
        result.low = val[3]
        result.close = val[4]
        result.volume = val[5]
        result.closeTime = val[6]
        result.quoteAssetVolume = val[7]
        result.numTrades = val[8]
        result.takerBuyBaseAssetVolume = val[9]
        result.takerBuyQuoteAssetVolume = val[10]
        result.ignore = val[11]

        return result
