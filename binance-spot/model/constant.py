class CandlestickInterval:

    MIN1 = '1m'
    MIN3 = '3m'
    MIN5 = '5m'
    MIN15 = '15m'
    MIN30 = '30m'
    HOUR1 = '1h'
    HOUR2 = '2h'
    HOUR4 = '4h'
    HOUR6 = '6h'
    HOUR8 = '8h'
    HOUR12 = '12h'
    DAY1 = '1d'
    DAY3 = '3d'
    WEEK1 = '1w'
    MON1 = '1m'
    INVALID = None


class OrderSide:

    BUY = 'BUY'
    SELL = 'SELL'
    INVALID = None


class TimeInForce:

    GTC = 'GTC'
    IOC = 'IOC'
    FOK = 'FOK'
    GTX = 'GTX'
    INVALID = None


class OrderType:

    LIMIT = 'LIMIT'
    MARKET = 'MARKET'
    STOP = 'STOP'
    STOP_MARKET = 'STOP_MARKET'
    TAKE_PROFIT = 'TAKE_PROFIT'
    TAKE_PROFIT_MARKET = 'TAKE_PROFIT_MARKET'
    TRAILING_STOP_MARKET = 'TRAILING_STOP_MARKET'
    INVALID = None


class OrderRespType:

    ACK = 'ACK'
    RESULT = 'RESULT'
    FULL = 'FULL'
    INVALID = None


class StopLimitTimeType:

    GTC = 'GTC'
    FOK = 'FOK'
    IOC = 'IOC'
    INVALID = None


class SubscribeMessageType:

    RESPONSE = 'response'
    PAYLOAD = 'payload'


class UpdateTime:

    NORMAL = ''
    FAST = '@100ms'
    REALTIME = '@0ms'
    INVALID = ''
