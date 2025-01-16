import os
import pathlib
import requests
import json


class FuncClient(object):
    _instance = None
    # //////////////////要修改////////////////////////  ex:http://*****:****/usFunc/
    ROOT = "http://127.0.0.1:8081/usFunc/"
    GAP_URL = ROOT + "gap/"
    VOLUME_URL = ROOT + "volume/"
    SUPRES_URL = ROOT + "supportresistance/"
    NECKLINE_URL = ROOT + "neckline/"
    SUPSIGNAL_URL = ROOT + "supportsignal/"
    RESSIGNAL_URL = ROOT + "resistancesignal/"
    NECKLINESUPSIGNAL_URL = ROOT + "necklinesupsignal/"
    NECKLINERESSIGNAL_URL = ROOT + "necklineressignal/"
    GETSIGNALS_URL = ROOT + "find_signal/"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        pass

    def _send_request(self, url: str, request_body: str):
        request_header = {
            "Content-Type": "application/json"
        }

        response = requests.post(url, data=json.dumps(
            request_body), headers=request_header)
        return response

    def get_gap(self,
                symbol: str,
                start_date: str,
                gap_interval: int):

        params = {
            "up_gap_interval": gap_interval,
            "down_gap_interval": gap_interval
        }

        request_body = {
            "symbol": symbol,
            "start_date": start_date,
            "params": params
        }
        response = self._send_request(self.GAP_URL, request_body)

        if response.status_code == 200:
            return response.json()['detail']

        elif response.status_code == 404:
            print("It has no trading pair found!")
        else:
            print("Something wrong at get spreads, status code:",
                  response.status_code)
            print(response.json())

        return None

    def get_volume(self,
                   symbol: str,
                   start_date: str,
                   previous_day: int,
                   survival_time: int):

        params = {
            "previous_day": previous_day,
            "survival_time": survival_time
        }

        request_body = {
            "symbol": symbol,
            "start_date": start_date,
            "params": params
        }

        response = self._send_request(self.VOLUME_URL, request_body)

        if response.status_code == 200:
            return response.json()['detail']

        elif response.status_code == 404:
            print("It has no trading pair found!")
        else:
            print("Something wrong at get spreads, status code:",
                  response.status_code)
            print(response.json())

        return None

    def get_supres(self,
                   symbol: str,
                   start_date: str,
                   closeness_threshold: int,
                   peak_left: int,
                   peak_right: int,
                   valley_left: int,
                   valley_right: int,
                   swap_times: int):
        params = {
            "diff": closeness_threshold,
            "peak_left": peak_left,
            "peak_right": peak_right,
            "valley_left": valley_left,
            "valley_right": valley_right,
            "swap_times": swap_times
        }

        request_body = {
            "symbol": symbol,
            "start_date": start_date,
            "params": params
        }

        response = self._send_request(self.SUPRES_URL, request_body)

        if response.status_code == 200:
            return response.json()['detail']

        elif response.status_code == 404:
            print("It has no trading pair found!")
        else:
            print("Something wrong at get spreads, status code:",
                  response.status_code)
            print(response.json())

        return None

    def get_supsignal(self,
                      symbol: str,
                      start_date: str,
                      closeness_threshold: int,
                      peak_left: int,
                      peak_right: int,
                      valley_left: int,
                      valley_right: int,
                      swap_times: int):

        params = {
            "diff": closeness_threshold,
            "peak_left": peak_left,
            "peak_right": peak_right,
            "valley_left": valley_left,
            "valley_right": valley_right,
            "swap_times": swap_times
        }

        request_body = {
            "symbol": symbol,
            "start_date": start_date,
            "params": params
        }

        response = self._send_request(self.SUPSIGNAL_URL, request_body)

        if response.status_code == 200:
            return response.json()['detail']

        elif response.status_code == 404:
            print("It has no trading pair found!")
        else:
            print("Something wrong at get spreads, status code:",
                  response.status_code)
            print(response.json())

        return None

    def get_ressignal(self,
                      symbol: str,
                      start_date: str,
                      closeness_threshold: int,
                      peak_left: int,
                      peak_right: int,
                      valley_left: int,
                      valley_right: int,
                      swap_times: int):

        params = {
            "diff": closeness_threshold,
            "peak_left": peak_left,
            "peak_right": peak_right,
            "valley_left": valley_left,
            "valley_right": valley_right,
            "swap_times": swap_times
        }

        request_body = {
            "symbol": symbol,
            "start_date": start_date,
            "params": params
        }

        response = self._send_request(self.RESSIGNAL_URL, request_body)

        if response.status_code == 200:
            return response.json()['detail']

        elif response.status_code == 404:
            print("It has no trading pair found!")
        else:
            print("Something wrong at get spreads, status code:",
                  response.status_code)
            print(response.json())

        return None

    def get_neckline(self,
                     symbol: str,
                     start_date: str,
                     nk_valley_left: int,
                     nk_valley_right: int,
                     nk_peak_left: int,
                     nk_peak_right: int,
                     nk_startdate: int,
                     nk_enddate: int,
                     nk_interval: int,
                     nk_value: int):

        params = {
            "nk_valley_left": nk_valley_left,
            "nk_valley_right": nk_valley_right,
            "nk_peak_left": nk_peak_left,
            "nk_peak_right": nk_peak_right,
            "nk_startdate": nk_startdate,
            "nk_enddate": nk_enddate,
            "nk_interval": nk_interval,
            "nk_value": nk_value
        }

        request_body = {
            "symbol": symbol,
            "start_date": start_date,
            "params": params
        }

        response = self._send_request(self.NECKLINE_URL, request_body)

        if response.status_code == 200:
            return response.json()['detail']

        elif response.status_code == 404:
            print("It has no trading pair found!")
        else:
            print("Something wrong at get spreads, status code:",
                  response.status_code)
            print(response.json())

        return None

    def get_neckline_sup_signal(self,
                                symbol: str,
                                start_date: str,
                                nk_valley_left: int,
                                nk_valley_right: int,
                                nk_peak_left: int,
                                nk_peak_right: int,
                                nk_startdate: int,
                                nk_enddate: int,
                                nk_interval: int,
                                nk_value: int):

        params = {
            "nk_valley_left": nk_valley_left,
            "nk_valley_right": nk_valley_right,
            "nk_peak_left": nk_peak_left,
            "nk_peak_right": nk_peak_right,
            "nk_startdate": nk_startdate,
            "nk_enddate": nk_enddate,
            "nk_interval": nk_interval,
            "nk_value": nk_value
        }

        request_body = {
            "symbol": symbol,
            "start_date": start_date,
            "params": params
        }

        response = self._send_request(self.NECKLINESUPSIGNAL_URL, request_body)

        if response.status_code == 200:
            return response.json()['detail']

        elif response.status_code == 404:
            print("It has no trading pair found!")
        else:
            print("Something wrong at get spreads, status code:",
                  response.status_code)
            print(response.json())

        return None

    def get_neckline_res_signal(self,
                                symbol: str,
                                start_date: str,
                                nk_valley_left: int,
                                nk_valley_right: int,
                                nk_peak_left: int,
                                nk_peak_right: int,
                                nk_startdate: int,
                                nk_enddate: int,
                                nk_interval: int,
                                nk_value: int):

        params = {
            "nk_valley_left": nk_valley_left,
            "nk_valley_right": nk_valley_right,
            "nk_peak_left": nk_peak_left,
            "nk_peak_right": nk_peak_right,
            "nk_startdate": nk_startdate,
            "nk_enddate": nk_enddate,
            "nk_interval": nk_interval,
            "nk_value": nk_value
        }

        request_body = {
            "symbol": symbol,
            "start_date": start_date,
            "params": params
        }

        response = self._send_request(self.NECKLINERESSIGNAL_URL, request_body)

        if response.status_code == 200:
            return response.json()['detail']

        elif response.status_code == 404:
            print("It has no trading pair found!")
        else:
            print("Something wrong at get spreads, status code:",
                  response.status_code)
            print(response.json())

        return None

    def get_all_signals(self,
                        symbol: str,
                        start_date: str,
                        signal_numbers: list,
                        signal_kinds: list,
                        gap_interval: int,
                        previous_day: int,
                        survival_time: int,
                        diff: int,
                        peak_left: int,
                        peak_right: int,
                        valley_left: int,
                        valley_right: int,
                        swap_times: int,
                        nk_valley_left: int,
                        nk_valley_right: int,
                        nk_peak_left: int,
                        nk_peak_right: int,
                        nk_startdate: int,
                        nk_enddate: int,
                        nk_interval: int,
                        nk_value: int):

        request_body = {
            "symbol": symbol,
            "start_date": start_date,
            "signal_numbers": signal_numbers,
            "signal_kinds": signal_kinds,
            "params": {
                "gap": {
                    "up_gap_interval": gap_interval,
                    "down_gap_interval": gap_interval
                },
                "sup_res": {
                    "diff": diff,
                    "peak_left": peak_left,
                    "peak_right": peak_right,
                    "valley_left": valley_left,
                    "valley_right": valley_right,
                    "swap_times": swap_times
                },
                "volume": {
                    "previous_day": previous_day,
                    "survival_time": survival_time
                },
                "neckline": {
                    "nk_valley_left": nk_valley_left,
                    "nk_valley_right": nk_valley_right,
                    "nk_peak_left": nk_peak_left,
                    "nk_peak_right": nk_peak_right,
                    "nk_startdate": nk_startdate,
                    "nk_enddate": nk_enddate,
                    "nk_interval": nk_interval,
                    "nk_value": nk_value
                }
            }
        }

        response = self._send_request(self.GETSIGNALS_URL, request_body)

        if response.status_code == 200:
            return response.json()['detail']
        elif response.status_code == 404:
            print("It has no trading pair found!")
        else:
            print("Something wrong at get spreads, status code:",
                  response.status_code)
            print(response.json())

        return None
