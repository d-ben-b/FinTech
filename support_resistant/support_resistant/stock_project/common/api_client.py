import json
import requests
import time
import threading
import os

class APIClient(object):
    """
    Client for interacting with the API to fetch data for options trading strategies.

    This class provides methods to authenticate, refresh tokens, fetch options chain, quotes, and perform filtering.

    :ivar _instance: Singleton instance of the class.
    :ivar _token: Authentication token.
    :ivar ROOT: Root URL of the API.
    :ivar AUTH_URL: URL for authentication.
    :ivar REFRESH_URL: URL for refreshing tokens.
    :ivar QUOTE_FILTER_URL: URL for filtering from market quotes data.
    :ivar QUOTE_URL: URL for fetching market quotes data.
    :ivar OPTION_FILTER_URL: URL for filtering from option data.
    :ivar OPTION_QUOTE_URL: URL for fetching options data.
    :ivar MONITOR_SPREAD_URL: URL for monitoring spreads.
    """
    _instance = None
    _token = None
    ROOT = "http://140.116.214.156:7000/usData/" 
    AUTH_URL = ROOT + 'token/'
    REFRESH_URL = ROOT + 'token/refresh/'
    QUOTE_URL = ROOT + 'market/quotes/'   
    GET_OPTION_URL = ROOT + 'market/option/get_bt_option/'
    GET_OPTION_QUOTE_URL = ROOT + 'market/option/bt_option/'   
    
    def __new__(cls, *args, **kwargs):
        """
        Implementing Singleton pattern for the class instantiation.

        :return: Singleton instance of the class.
        :rtype: APIClient
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """
        Initialize the API client with authentication details and start token refresh thread.
        """
        self._api_info = {
            "username" : "course",
            "password" : "cosbi624001479"
        }     
        self._start()
    
    def _get_token(self):
        return self._token
    
    def _set_token(self, token: dict):
        self._token = token

    def _auth_token(self, username, password):
        response = requests.post(self.AUTH_URL, data={
                            "username":username,
                            "password":password
                        })
        api_token = response.json()
        return api_token
    
    def _refresh_token(self):
        request_header = { "Content-Type" : "application/json" }
        request_body = { "refresh" : self._token['refresh']}
        response = requests.post(self.REFRESH_URL, data=json.dumps(request_body), headers=request_header)
        
        if response.status_code != 200:
            self._set_token(self._auth_token(self._api_info['username'], self._api_info['password']))
            return
        
        self._set_token(response.json())
            
    def _create_refresh_job(self, *args):
        while(True):
            time.sleep(880)
            self._refresh_token()
    
    def _start(self):    
        self._set_token(self._auth_token(self._api_info['username'], self._api_info['password']))
            
        t1 = threading.Thread(target=self._create_refresh_job)
        t1.start()
    
    def _send_request(self, url: str, request_body: str):
        """
        Send a request to the API using the provided URL and request body.

        :param url: The API endpoint URL.
        :type url: str
        :param request_body: The request body in JSON format.
        :type request_body: str
        :return: The API response.
        :rtype: requests.Response
        """
        token = self._get_token()
        request_header = {
            "Authorization" : f"Bearer {token['access']}",
            "Content-Type"  : "application/json"
        }
        response = requests.post(url, data=json.dumps(request_body), headers=request_header)
        
        return response

    def get_options(
                    self, 
                    symbol: list,
                    option_type: str,
                    quote_date: str,
                    till_expiry_days: int,
                    price: int
                ):
        """
        Fetch options chain data from the API based on the provided parameters.

        :param symbol_list: List of symbols to fetch options for.
        :type symbol_list: list
        :param option_type: Type of option (Call or Put).
        :type option_type: str
        :return: Options chain data.
        :rtype: dict or None
        """
        
        request_body = {
            "symbols" : symbol,
            "option_type" : option_type,
            "quote_date" : quote_date,
            "till_expiry_days": till_expiry_days,
            "price" : price
        }

        response = self._send_request(self.GET_OPTION_URL, request_body)
        if response.status_code == 200:
            return response.json()['detail']
        
        else:
            print("Something wrong at getting options chain, status code:", response.status_code)
            print(response.json())
            return None
    
    def get_options_quote(self, contracts, quote_date: str):
        """
        Fetch options quotes data from the API based on the provided parameters.

        :param contracts: List of option contracts to fetch quotes for.
        :type contracts: list
        :param quote_date: quote date for the quote data (optional).
        :type quote_date: str or None
        :return: Options quotes data.
        :rtype: dict or None
        """
                
        request_body = {
            "contracts" : contracts,
            "quote_date": quote_date
        }
        
        response = self._send_request(self.GET_OPTION_QUOTE_URL, request_body)
        if response.status_code == 200:
            return response.json()['detail']
        
        else:
            print("Something wrong at getting options quote, status code:", response.status_code)
            print(response.json())
            return None
        
    def get_underlying_quotes(self, symbol, start_date=None, end_date=None, period=None):
        """
        Fetch underlying quotes data from the API based on the provided parameters.

        :param symbol: Symbol of the underlying asset to fetch quotes for.
        :type symbol: str
        :param start_date: Start date for the quote data (optional).
        :type start_date: str or None
        :param end_date: End date for the quote data (optional).
        :type end_date: str or None
        :param period: Time period for the quote data (optional).
        :type period: str or None
        :return: Underlying quotes data.
        :rtype: dict or None
        """
        request_body = {
                "symbols"       : symbol,
                "start_date"    : start_date,
                "end_date"      : end_date,
                "period"        : period
        }
        response = self._send_request(self.QUOTE_URL, request_body)
        
        if response.status_code == 200:
            return response.json()['detail']
        
        else:
            print("Something wrong at getting underlying quotes, status code:", response.status_code)
            print(response.json())
            return None
    
