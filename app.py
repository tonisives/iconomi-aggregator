import hmac
import hashlib
import base64

from chalice import Chalice

from config import *
import requests
import time
import json

from weigher import Weigher

app = Chalice(app_name='iconomi-aggregator')
ICONOMI_API_URL = "https://api.iconomi.com"


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/strategies/{ticker}')
def detail(ticker):
    assets = get("/v1/strategies/" + ticker + "/structure")["values"]
    return assets


@app.route('/strategies')
def strategies():
    strategies_list = get("/v1/strategies/")
    return strategies_list


@app.route('/top-ten')
def top_ten():
    tickers = ["BLX", "CAR", "ECA", "CCC", "ADVERTO", "MAV", "LONGTERMFUNDAMENTALS", "RISKYBISCUITS", "KNEPALA",
               "JUMPSTART", "INCGROWTH"]
    combined_assets = []

    for ticker in tickers:
        assets = get("/v1/strategies/" + ticker + "/structure")
        combined_assets.append(assets)

    weigher = Weigher(combined_assets)

    return weigher.get_weighed()


def generate_signature(payload, request_type, request_path, timestamp):
    data = ''.join([timestamp, request_type.upper(),
                    request_path, payload]).encode()
    signed_data = hmac.new(ICONOMI_API_SECRET.encode(), data, hashlib.sha512)
    return base64.b64encode(signed_data.digest())


def get(api):
    return call('GET', api, '')


def post(api, payload):
    return call('POST', api, payload)


def call(method, api, payload):
    timestamp = str(int(time.time() * 1000.0))

    jsonPayload = payload
    if method == 'POST':
        jsonPayload = json.dumps(payload)

    requestHeaders = {
        'ICN-API-KEY': ICONOMI_API_KEY,
        'ICN-SIGN': generate_signature(jsonPayload, method, api, timestamp),
        'ICN-TIMESTAMP': timestamp
    }

    if method == 'GET':
        response = requests.get(ICONOMI_API_URL + api, headers=requestHeaders)
        if response.status_code == 200:
            return json.loads(response._content)
        else:
            return ('Request did not succeed: ' + response.reason)
    elif method == 'POST':
        response = requests.post(
            ICONOMI_API_URL + api, json=payload, headers=requestHeaders)
        if response.status_code == 200:
            return json.loads(response._content)
        else:
            return ('Request did not succeed: ' + response.reason)
