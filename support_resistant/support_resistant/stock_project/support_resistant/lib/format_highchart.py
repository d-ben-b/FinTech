import time
import json
import pathlib
from typing import Any, List
import pandas as pd
from datetime import timedelta
from datetime import datetime
from collections import defaultdict
import numpy as np
from collections import OrderedDict


class PdEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, pd.Timestamp):
            return str(obj)
        return json.JSONEncoder.default(self, obj)

def get_sup_res_time(stock_sup_res):
    stock_sup_res_result = {}
    for key, value in stock_sup_res.items():
        key = eval(key)
        stock_sup_res_result.update({key : value})
    stock_supp_resis_str = {
        str(k): stock_sup_res_result[k] for k in stock_sup_res_result}
    stock_supp_resis_json = json.dumps(stock_supp_resis_str, cls=PdEncoder)
    a = str(stock_supp_resis_json)
    local_file = eval(a)
    pricekey_date_list = []
    pricekey_value_list = []
    points_tulpe = []
    for number in local_file.keys():
        pricekey_date = time.strptime(number[2:12], "%Y-%m-%d")
        pricekey_date = time.mktime(pricekey_date)
        pricekey_date = int(round(pricekey_date * 1000))
        pricekey_value = [number[15:-1]]
        floatArray = np.asfarray(pricekey_value, dtype=np.float64)
        pricekey_date_list.append(pricekey_date)
        pricekey_value_list.append(floatArray[0])
        points_tulpe = list(zip(pricekey_date_list, pricekey_value_list))
    date_list = []
    for number in local_file.values():
        if len(number) == 2:
            number[0][0] = time.strptime(number[0][0][0:10], "%Y-%m-%d")
            number[0][0] = time.mktime(number[0][0])
            number[0][0] = int(round(number[0][0] * 1000))
            date_list.append(number)
        if len(number) == 3:
            number[0][0] = time.strptime(number[0][0][0:10], "%Y-%m-%d")
            number[0][0] = time.mktime(number[0][0])
            number[0][0] = int(round(number[0][0] * 1000))
            number[1][0] = time.strptime(number[1][0][0:10], "%Y-%m-%d")
            number[1][0] = time.mktime(number[1][0])
            number[1][0] = int(round(number[1][0] * 1000))
            date_list.append(number)
        if len(number) == 4:
            number[0][0] = time.strptime(number[0][0][0:10], "%Y-%m-%d")
            number[0][0] = time.mktime(number[0][0])
            number[0][0] = int(round(number[0][0] * 1000))
            number[1][0] = time.strptime(number[1][0][0:10], "%Y-%m-%d")
            number[1][0] = time.mktime(number[1][0])
            number[1][0] = int(round(number[1][0] * 1000))
            number[2][0] = time.strptime(number[2][0][0:10], "%Y-%m-%d")
            number[2][0] = time.mktime(number[2][0])
            number[2][0] = int(round(number[2][0] * 1000))
            date_list.append(number)
    supp_resis = defaultdict(list)
    for i, j in zip(points_tulpe, date_list):
        supp_resis[i] = j
    return supp_resis

def transform_line(stock_sup_res, stock_data):
    stock_sup_res = get_sup_res_time(stock_sup_res)
    support = []
    resistance = []
    support_active = []
    support_inactive = []
    resistance_active = []
    resistance_inactive = []
    for pricekey in stock_sup_res.keys():
        if stock_sup_res[pricekey][0][1] == 'support':
            support.append(
                [pricekey, (stock_sup_res[pricekey][0][0], pricekey[1])])
        if stock_sup_res[pricekey][0][1] == 'resistance':
            resistance.append(
                [pricekey, (stock_sup_res[pricekey][0][0], pricekey[1])])
        if len(stock_sup_res[pricekey]) == 2:
            continue
        for i in range(0, len(stock_sup_res[pricekey])-2):
            if stock_sup_res[pricekey][i+1][1] == 'support':
                support.append([
                    (stock_sup_res[pricekey][i][0], pricekey[1]),
                    (stock_sup_res[pricekey][i+1][0], pricekey[1]),
                ])
            if stock_sup_res[pricekey][i+1][1] == 'resistance':
                resistance.append([
                    (stock_sup_res[pricekey][i][0], pricekey[1]),
                    (stock_sup_res[pricekey][i+1][0], pricekey[1]),
                ])
    for pricekey in range(len(support)):
        end_date = str(stock_data.index[-1])
        end_date = int(time.mktime(datetime.strptime(
            end_date, "%Y-%m-%d %H:%M:%S").timetuple()))*1000
        if support[pricekey][1][0] == end_date:
            support_active.append(support[pricekey])
        else:
            support_inactive.append(support[pricekey])
    for pricekey in range(len(resistance)):
        end_date = str(stock_data.index[-1])
        end_date = int(time.mktime(datetime.strptime(
            end_date, "%Y-%m-%d %H:%M:%S").timetuple()))*1000
        if resistance[pricekey][1][0] == end_date:
            resistance_active.append(resistance[pricekey])
        else:
            resistance_inactive.append(resistance[pricekey])
    return support_active, support_inactive, resistance_active, resistance_inactive

def transform_bar_volume(volume):
    volume_result = {}
    for key, value in volume.items():
        key = eval(key)
        volume_result.update({key : value})
    get_plt_bar = defaultdict(list)
    bar_active = []
    bar_inactive = []
    bar_stategy=[]
    bar_report=[]
    for pricekey in volume_result.keys():
        pricekey_date = time.strptime(str(pricekey[0]), "%Y-%m-%d")
        pricekey_date = time.mktime(pricekey_date)
        pricekey_date = int(round(pricekey_date * 1000))
        get_plt_bar[pricekey_date, pricekey[1], pricekey[2]]
    pricekey_values = []
    for pricevalue in volume_result.values():
        pricekey_date = time.strptime(
            str(pricevalue['end_date'][0:10]), "%Y-%m-%d")
        pricekey_date = time.mktime(pricekey_date)
        pricekey_date = int(round(pricekey_date * 1000))
        pricekey_values.append([pricekey_date]+[pricevalue['state']])
    for i, j in zip(get_plt_bar.keys(), pricekey_values):
        get_plt_bar[i] = j
    for pricekey in get_plt_bar.keys():
        bar_stategy.append([pricekey[0],pricekey[1]])
        if get_plt_bar[pricekey][1] == 'active':
                unix_timestamp = pricekey[0] / 1000  # 將毫秒轉換為秒
                timestamp = datetime.fromtimestamp(unix_timestamp)
                formatted_date = timestamp.strftime('%Y-%m-%d')
                first_crossover=volume_result[formatted_date,pricekey[1], pricekey[2]]['first']
                if first_crossover != None:
                    first_crossover_date = time.strptime(str(first_crossover[1][0:10]), "%Y-%m-%d")
                    first_crossover_date = time.mktime(first_crossover_date)
                    first_crossover_date = int(round(first_crossover_date * 1000))
                    bar_report=[[ pricekey[0], pricekey[1], pricekey[2],first_crossover_date]]
                bar_active.append(
                    [[pricekey[0], pricekey[1], pricekey[2]],
                     [(get_plt_bar[pricekey][0]), pricekey[1], pricekey[2]]])
        else:
                bar_inactive.append(
                    [[pricekey[0], pricekey[1], pricekey[2]],
                     [(get_plt_bar[pricekey][0]), pricekey[1], pricekey[2]]])
    return bar_active, bar_inactive,bar_stategy,bar_report

def transform_bar_gap(gap):
    gap_result = {}
    for key, value in gap.items():
        key = eval(key)
        gap_result.update({key : value})
    get_plt_bar = defaultdict(list)
    up_gap_active = []
    up_gap_inactive = []
    down_gap_active = []
    down_gap_inactive = []
    up_gap_signal=[]
    down_gap_signal=[]
    for pricekey in gap_result.keys():
        pricekey_date = time.strptime(str(pricekey[0]), "%Y-%m-%d")
        pricekey_date = time.mktime(pricekey_date)
        pricekey_date = int(round(pricekey_date * 1000))
        get_plt_bar[pricekey_date, pricekey[1], pricekey[2]]
    pricekey_values = []
    for pricevalue in gap_result.values():
        pricekey_date = time.strptime(
            str(pricevalue['end_date']), "%Y-%m-%d")
        pricekey_date = time.mktime(pricekey_date)
        pricekey_date = int(round(pricekey_date * 1000))
        pricekey_values.append([pricekey_date]+[pricevalue['attribute']]+[pricevalue['state']])
    for i, j in zip(get_plt_bar.keys(), pricekey_values):
        get_plt_bar[i] = j
    for pricekey in get_plt_bar.keys():
        if get_plt_bar[pricekey][1] == 'up_gap':
            up_gap_signal.append([pricekey[0],pricekey[1]])
            if get_plt_bar[pricekey][2] == 'active':
                up_gap_active.append(
                    [[pricekey[0], pricekey[1], pricekey[2]],
                     [(get_plt_bar[pricekey][0]), pricekey[1], pricekey[2]]])
            else:
                up_gap_inactive.append(
                    [[pricekey[0], pricekey[1], pricekey[2]],
                     [(get_plt_bar[pricekey][0]), pricekey[1], pricekey[2]]])
        elif get_plt_bar[pricekey][1] == 'down_gap':
            down_gap_signal.append([pricekey[0],pricekey[2]])
            if get_plt_bar[pricekey][2] == 'active':
                down_gap_active.append(
                    [[pricekey[0], pricekey[1], pricekey[2]],
                     [(get_plt_bar[pricekey][0]), pricekey[1], pricekey[2]]])
            else:
                down_gap_inactive.append(
                    [[pricekey[0], pricekey[1], pricekey[2]],
                     [(get_plt_bar[pricekey][0]), pricekey[1], pricekey[2]]])
    return up_gap_active, up_gap_inactive, down_gap_active, down_gap_inactive,up_gap_signal,down_gap_signal

def transform_neckline(neckline):
    neckline_res = {}
    for key, value in neckline.items():
        key = eval(key)
        neckline_res.update({key : value})
    neckline_resistance_inactive = []
    neckline_resistance_active = []
    neckline_support_active = []
    neckline_support_inactive =  []
    neckline_report=[]
    if len(neckline_res)!=0:
        for i in neckline_res.keys():
            if neckline_res[i] != []:
                k1=neckline_res[i]['line'][0]
                b=neckline_res[i]['line'][1]
                x1=neckline_res[i]['start_date']['date'][0:10]
                x1=int(time.mktime(datetime.strptime(
                    str(x1), "%Y-%m-%d").timetuple()))*1000
                y1 = round((neckline_res[i]['start_date']['xline']*k1+b), 2)
                x2 = neckline_res[i]['end_date']['date'][0:10]
                x2 = int(time.mktime(datetime.strptime(
                    str(x2), "%Y-%m-%d").timetuple()))*1000
                y2 = round((neckline_res[i]['end_date']['xline']*k1+b), 2)
                neckline_resistance_chart=[(x1,y1),(x2,y2)]
                if neckline_res[i]['attribute'] == 'resistance' and neckline_res[i]['state']['end'] == 'inactive':
                    neckline_resistance_inactive.append(neckline_resistance_chart)
                elif neckline_res[i]['attribute'] == 'resistance' and neckline_res[i]['state']['end'] == 'active':
                    neckline_report.append([y1,x1,y2,'resistance'])
                    neckline_resistance_active.append(neckline_resistance_chart)
                elif neckline_res[i]['attribute'] == 'support' and neckline_res[i]['state']['end'] == 'active':
                    neckline_report.append(['support',y1,x1,y2])
                    neckline_support_active.append(neckline_resistance_chart)
                elif neckline_res[i]['attribute'] == 'support' and neckline_res[i]['state']['end'] == 'inactive':
                    neckline_support_inactive.append(neckline_resistance_chart)
    return neckline_resistance_inactive, neckline_resistance_active, neckline_support_active, neckline_support_inactive,neckline_report

def transform_sup_res_signal(sup_res):
    if len(sup_res) != 0:
     sup_res_signal=[[int(time.mktime(datetime.strptime(
                    str(key), "%Y-%m-%d").timetuple()))*1000, value] for key, value in sup_res.items()]
    else:
        sup_res_signal=[]
    return sup_res_signal
