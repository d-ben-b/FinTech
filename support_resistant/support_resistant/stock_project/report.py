from typing import Any, List
import os
import time
import datetime
import pandas as pd
from datetime import datetime
from collections import defaultdict

from common.func_api_client import FuncClient
from common.api_client import APIClient
from common.mail import MailHandler
from common.user_setting_operation import  UserTrackingHandler


class ReportHandler(object):

    def __init__(self):
        # self.ac = APIClient()
        self.mail = MailHandler()
        self.uth = UserTrackingHandler()
        self.fc = FuncClient()
        self.folder_path = "/home/thomas/Desktop/safetrader/saferTrader/stock_project/email_report/"

    def _create_local_file(self, data, user):

        df_short = pd.DataFrame(data['Short'])
        short_path = os.path.join(self.folder_path, 'all_short_signals.xlsx')
        with pd.ExcelWriter(short_path, engine='xlsxwriter') as short_writer:
            df_short.to_excel(short_writer, sheet_name='Short', index=False)
            short_writer.save()

        df_long = pd.DataFrame(data['Long'])
        long_path = os.path.join(self.folder_path, 'all_long_signals.xlsx')
        with pd.ExcelWriter(long_path, engine='xlsxwriter') as long_writer:
            df_long.to_excel(long_writer, sheet_name='Long', index=False)
            long_writer.save()

        print("Excel completed")

    def _remove_local_file(self, filename: str):
        print(f"successful remove {filename}!")
        os.remove(filename)

    def _get_signals(self, track):
        
        start_date = datetime.strptime(track[1], '%b-%d-%Y')
        start_date = start_date.strftime('%Y-%m-%d')        

        res = self.fc.get_all_signals(
                        start_date= start_date, 
                        symbol = track[2],  
                        signal_numbers = track[3],
                        gap_interval= track[4],
                        diff= track[6], 
                        peak_left = track[7],
                        peak_right = track[8],
                        valley_left = track[9], 
                        valley_right = track[10],  
                        swap_times = track[11],
                        previous_day= track[12],
                        survival_time= track[13],
                        nk_valley_left = track[14], 
                        nk_valley_right = track[15], 
                        nk_peak_left = track[16],
                        nk_peak_right = track[17], 
                        nk_startdate = track[18], 
                        nk_enddate = track[19],
                        nk_interval = track[20],
                        nk_value = track[21]
                    )
        
        all_signals = defaultdict(list)
        for status , value in res.items():
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

    def main(self):
        user_info = self.uth.get_all_user_info()   
        for ele in user_info:
            user, email = ele
            # print(user, email)
            track_info = self.uth.get_track_spreads_from_user(user)
            for track in track_info:
                # print(track)
                res = self._get_signals(track)
                # send email
                if res != {}: 
                    self._create_local_file(res, user)
                    res = self.mail.send(email, self.folder_path)

                    if res=={}:
                        print("Send email successful!")
                        self._remove_local_file(self.folder_path + "all_long_signals.xlsx")
                        self._remove_local_file(self.folder_path + "all_short_signals.xlsx")
                    else:
                        print("Send email failed!")
                
if __name__ == "__main__":
    report = ReportHandler()
    report.main()