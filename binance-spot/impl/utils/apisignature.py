import base64
import hashlib
import hmac
import datetime
from urllib import parse
import urllib.parse
from common.scripts.binance_spot.exception.binanceapiexception import BinanceApiException


def create_signature(secret_key, builder):
    if secret_key is None or secret_key == '':
        raise BinanceApiException(
            BinanceApiException.KEY_MISSING,  'Secret key are required')

#    keys = builder.param_map.keys()
#    query_string = '&'.join(['%s=%s' % (key, parse.quote(builder.param_map[key], safe='')) for key in keys])
    query_string = builder.build_url()
    signature = hmac.new(secret_key.encode(), msg=query_string.encode(
    ), digestmod=hashlib.sha256).hexdigest()
    builder.put_url('signature', signature)


def create_signature_with_query(secret_key, query):
    if secret_key is None or secret_key == '':
        raise BinanceApiException(
            BinanceApiException.KEY_MISSING,  'Secret key are required')

    signature = hmac.new(secret_key.encode(), msg=query.encode(),
                         digestmod=hashlib.sha256).hexdigest()

    return signature


def utc_now():
    return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
