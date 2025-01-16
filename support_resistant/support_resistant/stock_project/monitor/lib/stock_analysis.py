from typing import Any, List
import pandas as pd
import datetime
from datetime import datetime
import time
from . format_highchart import transform_bar_volume, transform_line, transform_bar_gap, transform_neckline,transform_sup_res_signal
import pprint
import os
from collections import defaultdict
from common.func_api_client import FuncClient
from common.api_client import APIClient

ac = APIClient()
func_client = FuncClient()

def convert_timestamp_to_highchart(time_str):
    return int(time.mktime(datetime.strptime(time_str, "%Y-%m-%d").timetuple()))*1000

def convert_str_to_datetime(time_str):
    return datetime.strptime(time_str, "%Y-%m-%d")

def get_stock_data(symbol, start_date):
    end_date = datetime.now().strftime('%Y-%m-%d')
    quote_res = ac.get_underlying_quotes(symbol, start_date, end_date)
    quote_res = quote_res[symbol]
    keys = ['date', 'open', 'high', 'low', 'close','volume']
    result = [list(item) for item in zip(quote_res['date'], quote_res['open'], quote_res['high'], quote_res['low'], quote_res['close'], quote_res['volume'])]
    final_result = [keys] + result
    final_result=final_result[1:]
    stock_data = pd.DataFrame(final_result, columns=['date', 'open', 'high', 'low', 'close', 'volume'])
    stock_data['date'] = pd.to_datetime(stock_data['date'])
    stock_data.set_index('date', inplace=True)
    # get ohlcv data
    timestamp_series = list(map(convert_timestamp_to_highchart, quote_res['date']))
    datetime_series = list(map(convert_str_to_datetime, quote_res['date']))
    ohlc = list(zip(timestamp_series, quote_res['open'], quote_res['high'], quote_res['low'],quote_res['close']))
    ohlcv1 = list(zip(datetime_series, quote_res['open'], quote_res['high'], quote_res['low'],quote_res['close'],quote_res['volume']))
    volume = list(zip(timestamp_series, quote_res['volume']))
    stock_data = pd.DataFrame(
        ohlcv1, columns=["date",'open','high','low','close','volume']
        )
    stock_data.sort_values('date', inplace=True)
    ohlc=list(zip((stock_data['date'].astype(int)/1000000), stock_data['open'], stock_data['high'], stock_data['low'], stock_data['close']))
    volume=list(zip((stock_data['date'].astype(int)/1000000), stock_data['volume']))
    stock_data = stock_data.set_index('date')
    x_line = [x for x in range(0,len(stock_data))]    
    stock_data['X'] = x_line
    return [stock_data, ohlc, volume]

def find_2signals(list1, list2):
    common_timestamps = set(data[0] for data in list1) & set(data[0] for data in list2)
    same_date = [data for data in list1 if data[0] in common_timestamps]
    return same_date

def find_3signals(list1, list2, list3):
    common_timestamps = set(data[0] for data in list1) & set(data[0] for data in list2) & set(data[0] for data in list3)
    same_date = [data for data in list1 if data[0] in common_timestamps]
    return same_date

def find_4signals(list1, list2, list3, list4):
    common_timestamps = set(data[0] for data in list1) & set(data[0] for data in list2) & set(data[0] for data in list3) & set(data[0] for data in list4)
    same_date = [data for data in list1 if data[0] in common_timestamps]
    return same_date

def get_all_technical_analysis(
          symbol, 
          start_date, 
          peak_left,
          peak_right,
          valley_left, 
          valley_right,
          closeness_threshold,
          swap_times,
          previous_day, 
          survival_time,
          gap_interval,
          nk_valley_left,
          nk_valley_right,
          nk_peak_left,
          nk_peak_right,
          nk_startdate,
          nk_enddate,
          nk_interval,
          nk_value):
    analysis_results = {}
    # Gap
    res = func_client.get_gap(symbol, start_date, gap_interval)
    # transform to timestamp   
    gap = transform_bar_gap(res)
    gap_up_active=gap[0]
    gap_up_inactive=gap[1]
    gap_down_active=gap[2]
    gap_down_inactive=gap[3]
    gap_up_signal=gap[4]
    gap_down_signal=gap[5]
    analysis_results["gap_up_active"]=gap_up_active
    analysis_results["gap_up_inactive"]=gap_up_inactive
    analysis_results["gap_down_active"]=gap_down_active
    analysis_results["gap_down_inactive"]=gap_down_inactive
    analysis_results["gap_up_signal"]=gap_up_signal
    analysis_results["gap_down_signal"]=gap_down_signal
    
    # Volume
    res = func_client.get_volume(symbol, start_date, previous_day, survival_time)

    # transform to timestamp    
    large_volume = transform_bar_volume(res)
    large_volume_acitve=large_volume[0]
    large_volume_inacitve=large_volume[1]
    large_volume_strategy=large_volume[2]
    large_volume_report=large_volume[3]
    analysis_results["bar_active"] = large_volume_acitve
    analysis_results["bar_inactive"] =large_volume_inacitve
    # bar report
    analysis_results["bar_report"] =large_volume_report
    analysis_results["big_volume"] =large_volume_strategy
    # SupportRisistant
    res = func_client.get_supres(symbol, start_date, closeness_threshold, peak_left, peak_right, valley_left, valley_right, swap_times)
    stock_data = get_stock_data(symbol, start_date)[0]
    support_resistance = transform_line(res, stock_data)

     # support signal
    res = func_client.get_supsignal(symbol, start_date, closeness_threshold, peak_left, peak_right, valley_left, valley_right, swap_times)


    sup_signal  = transform_sup_res_signal(res)
    
    # resistance signal
    res = func_client.get_ressignal(symbol, start_date, closeness_threshold, peak_left, peak_right, valley_left, valley_right, swap_times)

    res_signal  = transform_sup_res_signal(res)
    # transform to timestamp
    support_active = support_resistance[0]
    support_inactive = support_resistance[1]
    resistance_active=support_resistance[2]
    resistance_inactive=support_resistance[3]
    analysis_results["support_active"] = support_active
    analysis_results["support_inactive"] = support_inactive
    analysis_results["resistance_active"] = resistance_active
    analysis_results["resistance_inactive"] = resistance_inactive
    analysis_results["resistance_signal"] = res_signal
    analysis_results["support_signal"] = sup_signal
    # Neckline
    res = func_client.get_neckline(symbol, start_date, nk_valley_left, nk_valley_right, nk_peak_left, nk_peak_right, nk_startdate, nk_enddate,nk_interval,nk_value)    
    neckline = transform_neckline(res)
    # Neckline support signal
    res = func_client.get_neckline_sup_signal(symbol, start_date, nk_valley_left, nk_valley_right, nk_peak_left, nk_peak_right, nk_startdate, nk_enddate,nk_interval,nk_value)
    neckline_sup_signal  = transform_sup_res_signal(res)
    res = func_client.get_neckline_res_signal(symbol, start_date, nk_valley_left, nk_valley_right, nk_peak_left, nk_peak_right, nk_startdate, nk_enddate,nk_interval,nk_value)
    neckline_res_signal  = transform_sup_res_signal(res)
    # transform to timestamp
    analysis_results["neckline_resistance_inactive"] = neckline[0]
    analysis_results["neckline_resistance_active"] = neckline[1]
    analysis_results["neckline_support_active"] = neckline[2]
    analysis_results["neckline_support_inactive"] = neckline[3]
    # report
    analysis_results["neckline_report"] = neckline[4]
    # signal
    analysis_results["neckline_support_signal"]=neckline_sup_signal
    analysis_results["neckline_resistance_signal"]=neckline_res_signal
    #  Long signals
    two_signals_upgap_bar=find_2signals(gap_up_signal,large_volume_strategy)
    two_signals_upgap_resistance=find_2signals(gap_up_signal,res_signal)
    two_signals_upgap_resistance_neckline=find_2signals(gap_up_signal,neckline_res_signal)
    two_signals_bar_resistance=find_2signals(large_volume_strategy,res_signal)
    two_signals_bar_resistance_neckline=find_2signals(large_volume_strategy,neckline_res_signal)
    two_signals_resistance_resistance_neckline=find_2signals(res_signal,neckline_res_signal)
    three_signals_upgap_bar_resistance=find_3signals(gap_up_signal,large_volume_strategy,res_signal)
    three_signals_upgap_bar_resistance_neckline=find_3signals(gap_up_signal,large_volume_strategy,neckline_res_signal)
    three_signals_upgap_resistance_resistance_neckline=find_3signals(gap_up_signal,res_signal,neckline_res_signal)
    three_signals_bar_resistance_resistance_neckline=find_3signals(large_volume_strategy,res_signal,neckline_res_signal)
    four_signals_buy=find_4signals(gap_up_signal,large_volume_strategy,res_signal,neckline_res_signal)
    # Short Signals
    two_signals_downgap_bar=find_2signals(gap_down_signal,large_volume_strategy)
    two_signals_downgap_support=find_2signals(gap_down_signal,sup_signal)
    two_signals_downgap_support_neckline=find_2signals(gap_down_signal,neckline_sup_signal)
    two_signals_bar_support=find_2signals(large_volume_strategy,sup_signal)
    two_signals_bar_support_neckline=find_2signals(large_volume_strategy,neckline_sup_signal)
    two_signals_support_support_neckline=find_2signals(sup_signal,neckline_sup_signal)
    three_signals_downgap_bar_support=find_3signals(gap_down_signal,large_volume_strategy,sup_signal)
    three_signals_downgap_bar_support_neckline=find_3signals(gap_down_signal,large_volume_strategy,neckline_sup_signal)
    three_signals_bar_support_support_neckline=find_3signals(large_volume_strategy,sup_signal,neckline_sup_signal)
    three_signals_downgap_support_support_neckline=find_3signals(gap_down_signal,sup_signal,neckline_sup_signal)
    four_signals_sell=find_4signals(gap_down_signal,large_volume_strategy,sup_signal,neckline_sup_signal)
    analysis_results["two_signals_upgap_bar"]=two_signals_upgap_bar
    analysis_results["two_signals_upgap_resistance"]=two_signals_upgap_resistance
    analysis_results["two_signals_upgap_resistance_neckline"]=two_signals_upgap_resistance_neckline
    analysis_results["two_signals_bar_resistance"]=two_signals_bar_resistance
    analysis_results["two_signals_bar_resistance_neckline"]=two_signals_bar_resistance_neckline
    analysis_results["two_signals_resistance_resistance_neckline"]=two_signals_resistance_resistance_neckline
    analysis_results["three_signals_upgap_bar_resistance"]=three_signals_upgap_bar_resistance
    analysis_results["three_signals_upgap_bar_resistance_neckline"]=three_signals_upgap_bar_resistance_neckline
    analysis_results["three_signals_bar_resistance_resistance_neckline"]=three_signals_bar_resistance_resistance_neckline
    analysis_results["three_signals_upgap_resistance_resistance_neckline"]=three_signals_upgap_resistance_resistance_neckline
    analysis_results["four_signals_buy"]=four_signals_buy
    analysis_results["two_signals_downgap_bar"]=two_signals_downgap_bar
    analysis_results["two_signals_downgap_support"]=two_signals_downgap_support
    analysis_results["two_signals_downgap_support_neckline"]=two_signals_downgap_support_neckline
    analysis_results["two_signals_bar_support"]=two_signals_bar_support
    analysis_results["two_signals_bar_support_neckline"]=two_signals_bar_support_neckline
    analysis_results["two_signals_support_support_neckline"]=two_signals_support_support_neckline
    analysis_results["three_signals_downgap_bar_support"]=three_signals_downgap_bar_support
    analysis_results["three_signals_downgap_bar_support_neckline"]=three_signals_downgap_bar_support_neckline
    analysis_results["three_signals_bar_support_support_neckline"]=three_signals_bar_support_support_neckline
    analysis_results["three_signals_downgap_support_support_neckline"]=three_signals_downgap_support_support_neckline
    analysis_results["four_signals_sell"]=four_signals_sell
    analysis_results["stock_data"] = get_stock_data(symbol, start_date)[1]
    analysis_results['volume'] = get_stock_data(symbol, start_date)[2]
    return analysis_results

def get_signals(
          signals_selected_values,
          symbol, 
          start_date, 
          peak_left,
          peak_right,
          valley_left, 
          valley_right,
          diff,
          swap_times,
          previous_day, 
          survival_time,
          gap_interval,
          nk_valley_left,
          nk_valley_right,
          nk_peak_left,
          nk_peak_right,
          nk_startdate,
          nk_enddate,
          nk_interval,
          nk_value):
    
    res = func_client.get_all_signals(
                    symbol = symbol, 
                    signal_numbers = signals_selected_values,
                    start_date= start_date, 
                    gap_interval= gap_interval,
                    previous_day= previous_day,
                    survival_time= survival_time,
                    diff= diff, 
                    peak_left = peak_left, 
                    peak_right = peak_right, 
                    valley_left = valley_left, 
                    valley_right = valley_right, 
                    swap_times = swap_times,
                    nk_valley_left = nk_valley_left, 
                    nk_valley_right = nk_valley_right, 
                    nk_peak_left = nk_peak_left, 
                    nk_peak_right = nk_peak_right, 
                    nk_startdate = nk_startdate, 
                    nk_enddate = nk_enddate,
                    nk_interval = nk_interval,
                    nk_value = nk_value)
    
    all_signals = defaultdict(list)
    for status , value in  res.items():
        for signal_num, value1 in value.items():
            for kind, value2 in value1.items():
                for signal in value2:
                    date = signal[0]
                    price = signal[1]
                    obj = {"number_of_signals":signal_num, "kind":kind, "status":status, "date":date, "price":price}
                    if status =="Long":
                        all_signals['Long'].append(obj)
                    else:
                        all_signals['Short'].append(obj)                  
    
    return dict(all_signals)