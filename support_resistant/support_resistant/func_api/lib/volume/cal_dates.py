import calendar
from datetime import datetime
from datetime import timedelta
import pandas as pd

def get_weekday(datetime_obj, week_day):
    d = dict(zip(("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"), range(7))) 
    delta_hour = timedelta(days=1)  
    while datetime_obj.weekday() != d.get(week_day):
        if datetime_obj.weekday() > d.get(week_day):
            datetime_obj -= delta_hour
        elif datetime_obj.weekday() < d.get(week_day):
            datetime_obj += delta_hour
        else:
            pass
    return datetime_obj

def get_date(year, month, n, w):
    d = dict(zip(("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"), range(7)))  
    weekday, count_day = calendar.monthrange(year=year, month=month)  
    first_day = datetime(year=year, month=month, day=1)  
    last_day = datetime(year=year, month=month, day=count_day)
    # 第1個星期w
    if first_day.weekday() > d.get(w): 
        datetime_obj = first_day + timedelta(weeks=1)
    else:
        datetime_obj = first_day
    datetime_obj += timedelta(weeks=n - 1)
    first_weekday = get_weekday(datetime_obj=datetime_obj, week_day=w)
    return first_weekday

def cal_Qwd(stock_history):
    start_date=int(str(stock_history.index[0].date())[:4])
    end_date=int(str(stock_history.index[-1].date())[:4])
    month_list=[3,6,9,12]
    qwd_date=[]
    for y in range(start_date,end_date+1):
        for m in month_list:
            qwd=get_date(y,m,3,'friday')
            qwd_date.append(pd.Timestamp(qwd.date()))
    return qwd_date