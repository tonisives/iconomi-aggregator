import hmac
import hashlib
import base64

from chalice import Chalice

from config import *
import requests
import time
import json

app = Chalice(app_name='iconomi-aggregator')
ICONOMI_API_URL = "https://api.iconomi.com"


@app.route('/')
def index():
    return {'hello': 'world'}


@app.route('/detail/{ticker}')
def detail(ticker):
    assets = get("/v1/strategies/" + ticker + "/structure")["values"]
    return assets

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

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
