#!/usr/bin/env python3

import base64
import hashlib
import hmac
import json

from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen

from .constants import *
from .helpers import *


class Client(object):
    def __init__(self, account, key, secret, timeout=5):
        self._api_account = account
        self._api_key = key
        self._api_secret = secret

        self._api_timeout = int(timeout)

    def _build_headers(self, scope, method, params={}):
        headers = {
            'Accept': 'application/json',
            'User-Agent': 'pyCryptoTrader/1.0.0',
        }

        if scope.lower() == 'private':
            if method.upper() in ['GET', 'DELETE']:
                params = {'identity': self._api_account, 'nonce': get_current_timestamp()}

            payload = self._build_payload(params)
            signature = hmac.new(bytes(self._api_secret, 'utf-8'), bytes(payload, 'utf-8'), hashlib.sha384).hexdigest()

            headers.update({
                'X-BITOPRO-APIKEY': self._api_key,
                'X-BITOPRO-PAYLOAD': payload,
                'X-BITOPRO-SIGNATURE': signature
            })

        return headers

    def _build_payload(self, params={}):
        return base64.urlsafe_b64encode(json.dumps(params).encode('utf-8')).decode('utf-8')

    def _build_url(self, endpoint):
        return f"{PRIVATE_API_URL}/{PRIVATE_API_VERSION}/{endpoint}"

    def _send_request(self, scope, method, endpoint, params={}):
        # Build required url, headers and signature
        url = self._build_url(endpoint)
        headers = self._build_headers(scope, method, params)

        # Build body for POST request only
        data = None

        if len(params) > 0:
            if method.upper() == 'GET':
                url = f"{self._build_url(endpoint)}?{urlencode(params)}"
            elif method.upper() == 'POST':
                data = json.dumps(params).encode('utf-8')

        request = Request(headers=headers, method=method.upper(), url=url)
        response = urlopen(request, data=data, timeout=self._api_timeout)

        return json.loads(response.read())

    # Public API
    def get_public_all_tickers(self, pair=None):
        """
        https://developer.bitopro.com/docs#operation/getTickers

        :param pair: the trading pair to query
        :return: a data list contains all pair tickers
        """

        if pair is not None and len(pair) > 0:
            return self._send_request('public', 'GET', f"tickers/{pair.lower()}")
        else:
            return self._send_request('public', 'GET', 'tickers')

    def get_public_available_currencies(self):
        """
        https://developer.bitopro.com/docs#operation/getCurrencies

        :return: a data list contains all information for each currency
        """

        return self._send_request('public', 'GET', 'provisioning/currencies')

    def get_public_available_pairs(self):
        """
        https://developer.bitopro.com/docs#operation/getTradingPairs

        :return: a data list contains all information for each pair
        """

        return self._send_request('public', 'GET', 'provisioning/trading-pairs')

    def get_public_order_book(self, pair, limit=5):
        """
        https://developer.bitopro.com/docs#operation/getOrderBookByPair

        :param pair: the trading pair to query
        :param limit: the limit for the response
        :return: a dict contains ask and bid data
        """

        params = {
            'limit': limit,
        }

        return self._send_request('public', 'GET', f"order-book/{pair.lower()}", params)

    def get_public_recent_trades(self, pair):
        """
        https://developer.bitopro.com/docs#operation/getPairTrades

        :param pair: the trading pair to query
        :return: a data list contains all completed orders in exchange
        """

        return self._send_request('public', 'GET', f"trades/{pair.lower()}")

    # Private API (Read)
    def get_private_account_balance(self):
        """
        https://developer.bitopro.com/docs#operation/getAccountBalance

        :return: a data list contains all coins balance
        """

        return self._send_request('private', 'GET', 'accounts/balance')

    def get_private_order_data(self, pair, _id):
        """
        https://developer.bitopro.com/docs#operation/getOrderStatus

        :param pair: the trading pair to query
        :param _id: the id of the order
        :return: a dict contains order detail
        """

        return self._send_request('private', 'GET', f"orders/{pair.lower()}/{_id}")

    def get_private_order_history(self):
        """
        https://developer.bitopro.com/docs#operation/getOrderHistory

        :return: a data list contains all completed orders
        """

        return self._send_request('private', 'GET', 'orders/history')

    def get_private_order_list(self, pair, page=1, active=True):
        """
        https://developer.bitopro.com/docs#operation/getOrders

        :param pair: the trading pair to query
        :param page: the page number to query
        :param active: the flag to specify if only active (in progress) orders will return
        :return: a data list contains all related orders
        """

        params = {
            'page': page,
            'active': active
        }

        return self._send_request('private', 'GET', f"orders/{pair.lower()}", params)

    # Private API (Write)
    def set_private_cancel_order(self, pair, _id):
        """
        https://developer.bitopro.com/docs#operation/cancelOrder

        :param pair: the trading pair to cancel
        :param _id: the id of the order
        :return: a dict contains whole order info
        """

        return self._send_request('private', 'DELETE', f"orders/{pair.lower()}/{_id}")

    def set_private_create_order(self, pair, action, amount, price, _type='LIMIT'):
        """
        https://developer.bitopro.com/docs#operation/createOrder

        :param pair: the trading pair to create
        :param action: the action type, should only be BUY or SELL
        :param amount: the amount of the order for the trading pair
        :param price: the price of the order for the trading pair
        :param _type: the order type, should only be LIMIT or MARKET
        :return: a dict contains whole order info
        """

        params = {
            'action': action.upper(),
            'amount': str(amount),
            'price': str(price),
            'timestamp': get_current_timestamp(),
            'type': _type.upper()
        }

        return self._send_request('private', 'POST', f"orders/{pair.lower()}", params)
