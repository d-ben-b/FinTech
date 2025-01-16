from . import api_client
from . import func_api_client
from datetime import datetime, timedelta
from collections import defaultdict


class OptionBacktesting(object):

    start_quote = None
    end_quote = None
    all_signals = None
    
    def __init__(self):
        self.ac = api_client.APIClient()
        self.fc = func_api_client.FuncClient()
    
    def get_all_signals(self, params):
        
        res = self.fc.get_all_signals(
                    symbol = params["symbol"],
                    signal_numbers = params["signals_selected_values"],
                    signal_kinds = params["signals_selected_kinds"],
                    start_date = params["start_date"],
                    gap_interval = params["gap_interval"],
                    previous_day = params["previous_day"],
                    survival_time = params["survival_time"],
                    diff = params["closeness_threshold"],
                    peak_left = params["peak_left"],
                    peak_right = params["peak_right"],
                    valley_left = params["valley_left"],
                    valley_right = params["valley_right"],
                    swap_times = params["swap_times"],
                    nk_valley_left = params["nk_valley_left"],
                    nk_valley_right = params["nk_valley_right"],
                    nk_peak_left = params["nk_peak_left"],
                    nk_peak_right = params["nk_peak_right"],
                    nk_startdate = params["nk_startdate"],
                    nk_enddate = params["nk_enddate"],
                    nk_interval = params["nk_interval"],
                    nk_value = params["nk_value"],
                    )
        
        signals = defaultdict(list)
        for status , value in res.items():
            for signal_num, value1 in value.items():
                for kind, value2 in value1.items():
                    for signal in value2:
                        date = signal[0]
                        price = signal[1]
                        obj = {"number_of_signals":signal_num, "kind":kind, "status":status, "date":date, "price":price}
                        if status =="Long":
                            signals['Long'].append(obj)
                        else:
                            signals['Short'].append(obj)
                                                       
        long_signals = dict(signals).get('Long', [])
        short_signals = dict(signals).get('Short', [])
        
        return long_signals, short_signals
        
    def get_option(self, symbol, option_type, quote_date, buffer_date, price):
        # res 改成for迴圈拿取資料判斷option quote是否為None
        res = self.ac.get_options(symbol=symbol, option_type=option_type, quote_date=quote_date, till_expiry_days=buffer_date, price=price)
        return res
    
    def get_option_price(self, contract, quote_date, buffer_date):
               
        start_date = datetime.strptime(quote_date, "%Y-%m-%d")
        entry_date = start_date + timedelta(days=1)
        exit_date = entry_date + timedelta(days=buffer_date)
        
        start_quote = None
        for _ in range(3):
            start_quote_res = self.ac.get_options_quote(contracts=contract, quote_date=entry_date.strftime("%Y-%m-%d"))
            if start_quote_res is not None:
                start_quote = start_quote_res[contract]['bid_ask_mid'][0]
                break
            else:
                entry_date += timedelta(days=1)
                
        end_quote = None
        for _ in range(3):
            end_quote_res = self.ac.get_options_quote(contracts=contract, quote_date=exit_date.strftime("%Y-%m-%d"))
            if end_quote_res is not None:
                end_quote = end_quote_res[contract]['bid_ask_mid'][0]
                break
            else:
                exit_date += timedelta(days=1)
            
        return start_quote, end_quote, entry_date.strftime("%Y-%m-%d"), exit_date.strftime("%Y-%m-%d")
    
    def backtesting(self, start_quote, end_quote):
        profit = end_quote - start_quote
        return round(profit, 2)

    def main(self, params):
        
        self.all_signals = defaultdict(list)
        symbol = params["symbol"]
        buffer_date = params["buffer_date"]
        
        long_signals, short_signals = self.get_all_signals(params)

        for signal in long_signals:
            
            contracts = self.get_option([symbol], 'C', str(signal['date']), int(buffer_date), int(signal['price']))
            if contracts is not None:
                for contract in contracts:
                
                    start_quote, end_quote, entry_date, exit_date = self.get_option_price(str(contract), str(signal['date']), int(buffer_date))
                    
                    if (start_quote is not None) and (end_quote is not None):  #增加判斷結束日期尚未到達那也break
                        profit = self.backtesting(start_quote, end_quote)
                        signal['contract'] = contract
                        signal['start_date'] = entry_date
                        signal['start_quote'] = round(start_quote, 2)
                        signal['end_date'] = exit_date
                        signal['end_quote'] = round(end_quote, 2)
                        signal['profit'] = profit
                        signal['buffer_date'] = buffer_date
                        break
                    
                    else:
                        signal['contract'] = contract
                        signal['start_date'] = entry_date
                        signal['start_quote'] = start_quote
                        signal['end_date'] = exit_date
                        signal['end_quote'] = end_quote
                        signal['profit'] = None
                        signal['buffer_date'] = buffer_date                
            else:
                signal['contract'] = "X"
                signal['start_date'] = "X"
                signal['start_quote'] = "X"
                signal['end_date'] = "X"
                signal['end_quote'] = "X"
                signal['profit'] = "X"
                signal['buffer_date'] = "X"
            
            self.all_signals['Long'].append(signal)
                       
        for signal in short_signals:
            
            contracts = self.get_option([symbol], 'P', str(signal['date']), int(buffer_date), int(signal['price']))
            if contracts is not None:
                for contract in contracts:
                    
                    start_quote, end_quote, entry_date, exit_date = self.get_option_price(str(contract), str(signal['date']), int(buffer_date))
                    
                    if (start_quote is not None) and (end_quote is not None):  #增加判斷結束日期尚未到達那也break
                        profit = self.backtesting(start_quote, end_quote)
                        signal['contract'] = contract
                        signal['start_date'] = entry_date
                        signal['start_quote'] = round(start_quote, 2)
                        signal['end_date'] = exit_date
                        signal['end_quote'] = round(end_quote, 2)
                        signal['profit'] = profit
                        signal['buffer_date'] = buffer_date
                        break
                    else:
                        signal['contract'] = contract
                        signal['start_date'] = entry_date
                        signal['start_quote'] = start_quote
                        signal['end_date'] = exit_date
                        signal['end_quote'] = end_quote
                        signal['profit'] = None
                        signal['buffer_date'] = buffer_date                
            else:
                signal['contract'] = "X"
                signal['start_date'] = "X"
                signal['start_quote'] = "X"
                signal['end_date'] = "X"
                signal['end_quote'] = "X"
                signal['profit'] = "X"
                signal['buffer_date'] = "X"
            
            self.all_signals['Short'].append(signal)
                    
                        
        
if __name__ == "__main__":
    ac = api_client.APIClient()
    
    symbol = "AAPL"
    option_type = "P"
    quote_date = "2023-11-01"
    buffer_date = 12 
    price = 200
    contract = ac.get_options(symbol=symbol, option_type=option_type, quote_date=quote_date, buffer_date=buffer_date, price=price)[0][0]
    print(contract)

    # contract = self.get_option([symbol], 'C', str(signal['date']), int(buffer_date), int(signal['price']))[0]
    # if contract is not None:
    #     start_quote, end_quote, entry_date, exit_date = self.get_option_price(str(contract), str(signal['date']), int(buffer_date))
        
    #     if (start_quote is not None) and (end_quote is not None):
    #         profit = self.backtesting(start_quote, end_quote)
            
    #         signal['contract'] = contract
    #         signal['start_date'] = entry_date
    #         signal['start_quote'] = round(start_quote, 2)
    #         signal['end_date'] = exit_date
    #         signal['end_quote'] = round(end_quote, 2)
    #         signal['profit'] = profit
    #         signal['buffer_date'] = buffer_date
    #         self.all_signals['Long'].append(signal)
    #     else:
    #         signal['contract'] = contract
    #         signal['start_date'] = entry_date
    #         signal['start_quote'] = start_quote
    #         signal['end_date'] = exit_date
    #         signal['end_quote'] = end_quote
    #         signal['profit'] = None
    #         signal['buffer_date'] = buffer_date
    #         self.all_signals['Long'].append(signal)
    # else:
    #     signal['contract'] = contract
    #     signal['start_date'] = None
    #     signal['start_quote'] = None
    #     signal['end_date'] = None
    #     signal['end_quote'] = None
    #     signal['profit'] = None
    #     signal['buffer_date'] = None
    #     self.all_signals['Long'].append(signal)