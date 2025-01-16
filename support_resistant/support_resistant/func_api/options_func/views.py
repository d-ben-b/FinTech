from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
import datetime
import pandas as pd
import json
from pandas import Timestamp
from lib.api_client import APIClient
from lib.gap.gap import SequentialDetectionGapAnalysis
from lib.support_resistance.support_resistance_analysis import SupportResistance
from lib.volume.volume_analysis import ProtrudingVolumeAnalysis
from lib.neckline.neckline_analysis import NecklineAnalysis
ac = APIClient()

class GapViewSet(viewsets.ModelViewSet):
    """
    A ViewSet to handle gap analysis for stock data.
    Supports creation of gap analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """

        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create a gap analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.
        Returns a JSON response containing the gap analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params) - set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params) - set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")
        # Request body contains invalid parameters
        quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        quote_res = quote_res[request.data.get("symbol")]
        # get stock data to dataframe
        keys = ['date', 'open', 'high', 'low', 'close', 'volume']
        result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        final_result = [keys] + result
        final_result = final_result[1:]
        stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        stock_history['date'] = pd.to_datetime(stock_history['date'])
        stock_history.set_index('date', inplace=True)
        # call the gap analysis function
        gap_case = SequentialDetectionGapAnalysis(
            request.data.get("params")["up_gap_interval"],
            request.data.get("params")["down_gap_interval"]
        )
        gap_res = gap_case.sequential_process(stock_history)
        res = {}
        for key, value in gap_res.items():
            date = self._default_handler(key[0])
            key = list(key)
            key[0] = date
            res.update({str(key)[1:-1]: value})
        # transform to json type
        res = json.dumps(res, default=self._default_handler, indent=2)
        res = json.loads(res)
        if res is None:
            response = Response(data={"msg": "not found"})
            response.status_code = 404
            return response
        response = Response(data={"msg": "Succeed", 'detail': res})
        response.status_code = 200
        return response
 

class VolumeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for analyzing stock volume data.
    Supports creation of volume analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings..
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
    
    def create(self, request):
        """
        Handle POST request to create a volume analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.
        Returns a JSON response containing the volume analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")
        # Request body contains invalid parameters
        quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        quote_res = quote_res[request.data.get("symbol")]
        # get stock data to dataframe   
        keys = ['date', 'open', 'high', 'low', 'close','volume']
        result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        final_result = [keys] + result
        final_result=final_result[1:]
        stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        stock_history['date'] = pd.to_datetime(stock_history['date'])
        stock_history.set_index('date', inplace=True)
        # call the volume analysis function
        volume_case = ProtrudingVolumeAnalysis(
            request.data.get("params")["previous_day"],
            request.data.get("params")["survival_time"]
        )
        volume_case.sequential_process(stock_history)
        large_volume_res = volume_case.bar_large_volume
        res = {}
        for key, value in large_volume_res.items():
            date = self._default_handler(key[0])
            key = list(key)
            key[0] = date
            res.update({str(key)[1:-1] : value})
        if res is None:
            response = Response(data={"msg":"not found"})
            response.status_code = 404
            return response
        response = Response(data={"msg":"Succeed", 'detail':res})  
        response.status_code = 200
        return response
    

class SupportResistanceViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for detecting support and resistance levels in stock data.
    Supports creation of support and resistance analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create support and resistance analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the support and resistance analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d') 
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")
        # Request body contains invalid parameters
        quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        quote_res = quote_res[request.data.get("symbol")]
        # get stock data to dataframe   
        keys = ['date', 'open', 'high', 'low', 'close','volume']
        result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        final_result = [keys] + result
        final_result=final_result[1:]
        stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        stock_history['date'] = pd.to_datetime(stock_history['date'])
        stock_history.set_index('date', inplace=True)
        # call the support and resistance analysis function
        sup_res_case = SupportResistance(
            request.data.get("params")["closeness_threshold"],
            request.data.get("params")["peak_left"],
            request.data.get("params")["peak_right"],
            request.data.get("params")["valley_left"],
            request.data.get("params")["valley_right"],
            request.data.get("params")["swap_times"]
        )
        sup_res_case.sequential_process(stock_history)
        sup_res_res = sup_res_case.supp_resis
        res = {}
        for key, value in sup_res_res.items():
            date = self._default_handler(key[0])
            key = list(key)
            key[0] = date
            res.update({str(key)[1:-1] : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response                                
        response = Response(data={"msg":"Succeed", 'detail':res})  
        response.status_code = 200
        return response


class SupportSignalViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for generating support signals based on stock data.
    Supports creation of support signal analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create support signal analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the support signal analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d') 
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")
        # Request body contains invalid parameters
        quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        quote_res = quote_res[request.data.get("symbol")]
        # get stock data to dataframe   
        keys = ['date', 'open', 'high', 'low', 'close','volume']
        result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        final_result = [keys] + result
        final_result=final_result[1:]
        stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        stock_history['date'] = pd.to_datetime(stock_history['date'])
        stock_history.set_index('date', inplace=True)
        # call the support and resistance analysis function
        sup_res_case = SupportResistance(
            request.data.get("params")["closeness_threshold"],
            request.data.get("params")["peak_left"],
            request.data.get("params")["peak_right"],
            request.data.get("params")["valley_left"],
            request.data.get("params")["valley_right"],
            request.data.get("params")["swap_times"]
        )
        sup_res_case.sequential_process(stock_history)
        sup_res_res = sup_res_case.support_firstcrossover
        res = {}
        for key, value in sup_res_res.items():
            date = self._default_handler(key)
            key = [key]
            key = date
            res.update({str(key) : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response
        response = Response(data={"msg":"Succeed", 'detail':res})  
        response.status_code = 200
        return response


class ResistanceSignalViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for generating resistance signals based on stock data.
    Supports creation of resistance signal analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
    
    def create(self, request):
        """
        Handle POST request to create resistance signal analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the resistance signal analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d') 
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")
        # Request body contains invalid parameters
        quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        quote_res = quote_res[request.data.get("symbol")]
        # get stock data to dataframe   
        keys = ['date', 'open', 'high', 'low', 'close','volume']
        result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        final_result = [keys] + result
        final_result=final_result[1:]
        stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        stock_history['date'] = pd.to_datetime(stock_history['date'])
        stock_history.set_index('date', inplace=True)
        # call the support and resistance analysis function
        sup_res_case = SupportResistance(
            request.data.get("params")["closeness_threshold"],
            request.data.get("params")["peak_left"],
            request.data.get("params")["peak_right"],
            request.data.get("params")["valley_left"],
            request.data.get("params")["valley_right"],
            request.data.get("params")["swap_times"]
        )
        sup_res_case.sequential_process(stock_history)
        sup_res_res = sup_res_case.resistance_firstcrossover
        res = {}
        for key, value in sup_res_res.items():
            date = self._default_handler(key)
            key = [key]
            key = date
            res.update({str(key) : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response
        response = Response(data={"msg":"Succeed", 'detail':res})  
        response.status_code = 200
        return response


class NecklineViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for performing neckline analysis on stock data.
    Supports creation of neckline analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create neckline analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the neckline analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")
        # Request body contains invalid parameters
        quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        quote_res = quote_res[request.data.get("symbol")]
        # get stock data to dataframe   
        keys = ['date', 'open', 'high', 'low', 'close','volume']
        result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        final_result = [keys] + result
        final_result=final_result[1:]
        stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        stock_history['date'] = pd.to_datetime(stock_history['date'])
        stock_history.set_index('date', inplace=True)
        # call the neckline analysis function
        neckline_case = NecklineAnalysis(
            request.data.get("params")["nk_valley_left"],
            request.data.get("params")["nk_valley_right"],
            request.data.get("params")["nk_peak_left"],
            request.data.get("params")["nk_peak_right"],
            request.data.get("params")["nk_startdate"],
            request.data.get("params")["nk_enddate"],
            request.data.get("params")["nk_interval"],
            request.data.get("params")["nk_value"],
        )
        x_line = [x for x in range(0,len(stock_history))]
        stock_history['X'] = x_line
        neckline_case.sequential_process(stock_history)
        neckline_res = neckline_case.neckline
        res = {}
        for key, value in neckline_res.items():
            date = self._default_handler(key[0])
            key = list(key)
            key[0] = date
            res.update({str(key)[1:-1] : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response                                             
        response = Response(data={"msg":"Succeed", 'detail' : res})  
        response.status_code = 200
        return response
    

class NecklineSupSignalViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for performing neckline support signal analysis on stock data.
    Supports creation of support signal analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create neckline analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the neckline analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")
        # Request body contains invalid parameters
        quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        quote_res = quote_res[request.data.get("symbol")]
        # get stock data to dataframe   
        keys = ['date', 'open', 'high', 'low', 'close','volume']
        result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        final_result = [keys] + result
        final_result=final_result[1:]
        stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        stock_history['date'] = pd.to_datetime(stock_history['date'])
        stock_history.set_index('date', inplace=True)
        # call the neckline analysis function
        neckline_case = NecklineAnalysis(
            request.data.get("params")["nk_valley_left"],
            request.data.get("params")["nk_valley_right"],
            request.data.get("params")["nk_peak_left"],
            request.data.get("params")["nk_peak_right"],
            request.data.get("params")["nk_startdate"],
            request.data.get("params")["nk_enddate"],
            request.data.get("params")["nk_interval"],
            request.data.get("params")["nk_value"],
        )
        x_line = [x for x in range(0,len(stock_history))]
        stock_history['X'] = x_line
        neckline_case.sequential_process(stock_history)
        neckline_res = neckline_case.support_neckline_singal
        res = {}
        for key, value in neckline_res.items():
            date = self._default_handler(key)
            key = [key]
            key = date
            res.update({str(key) : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response                                                      
        response = Response(data={"msg":"Succeed", 'detail' : res})  
        response.status_code = 200
        return response

class NecklineResSignalViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for performing neckline resistance signal analysis on stock data.
    Supports creation of resistance signal analysis based on provided parameters.
    """
    queryset = None
    parser_classes = (JSONParser,)
    response = None
    required_params = ["symbol", "start_date", "params"]
    valid_params = ["symbol", "start_date", "end_date", "params"]

    def _default_handler(self, obj):
        """
        Default handler to serialize objects to JSON.
        Handles datetime.Timestamp objects by converting them to ISO formatted strings.
        """
        if isinstance(obj, Timestamp):
            return obj.isoformat(sep='-')[0:10]
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

    def create(self, request):
        """
        Handle POST request to create neckline resistance signal analysis for provided stock data.
        Expects input parameters including 'symbol', 'start_date', 'end_date', and 'params'.

        Returns a JSON response containing the neckline resistance signal analysis results.
        """
        input_params = [ele for ele in request.data]
        if set(input_params)-set(self.required_params) == set():
            end_date = datetime.datetime.now().strftime('%Y-%m-%d')
        elif set(input_params)-set(self.required_params) == set(['end_date']):
            end_date = request.data.get("end_date")
        # Request body contains invalid parameters
        quote_res = ac.get_underlying_quotes(request.data.get("symbol"), request.data.get("start_date"), end_date)
        quote_res = quote_res[request.data.get("symbol")]
        # get stock data to dataframe   
        keys = ['date', 'open', 'high', 'low', 'close','volume']
        result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
        final_result = [keys] + result
        final_result=final_result[1:]
        stock_history = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
        stock_history['date'] = pd.to_datetime(stock_history['date'])
        stock_history.set_index('date', inplace=True)
        # call the neckline analysis function
        neckline_case = NecklineAnalysis(
            request.data.get("params")["nk_valley_left"],
            request.data.get("params")["nk_valley_right"],
            request.data.get("params")["nk_peak_left"],
            request.data.get("params")["nk_peak_right"],
            request.data.get("params")["nk_startdate"],
            request.data.get("params")["nk_enddate"],
            request.data.get("params")["nk_interval"],
            request.data.get("params")["nk_value"],
        )
        x_line = [x for x in range(0,len(stock_history))]
        stock_history['X'] = x_line
        neckline_case.sequential_process(stock_history)
        neckline_res = neckline_case.resistance_neckline_singal
        res = {}
        for key, value in neckline_res.items():
            date = self._default_handler(key)
            key = [key]
            key = date
            res.update({str(key) : value})
        if res is None:
            response = Response(data = {"msg":"not found"})
            response.status_code = 404
            return response       
        response = Response(data={"msg":"Succeed", 'detail' : res})  
        response.status_code = 200
        return response