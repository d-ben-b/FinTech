from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from common.user_setting_operation import  UserTrackingHandler
from .lib.stock_analysis import get_all_technical_analysis, get_signals
import datetime
import json

uth = UserTrackingHandler()

def web(request):
    # render search page
    if not request.user.is_authenticated:
        messages.success(request, 'Sorry ! Please Log In.')
        return redirect(f'/saferTrader/account/login')
    return (render(request,"quote/monitor.html"))

@csrf_exempt
def add_track(request):

    start_date = request.POST.get('start_date')
    symbol = request.POST.get('symbol')
    signals_selected_values = request.POST.get('signals_selected_values')
    
    # gap
    up_gap_interval = request.POST.get('gap_interval')
    down_gap_interval = request.POST.get('gap_interval')

    # support_resistant
    diff = request.POST.get('diff') 
    peak_left = request.POST.get('peak_left')
    peak_right = request.POST.get('peak_right')
    valley_left = request.POST.get('valley_left')
    valley_right = request.POST.get('valley_right')
    swap_times = request.POST.get('swap_times')

    # volume
    previous_day = request.POST.get('previous_day')
    survival_time = request.POST.get('survival_time')

    # neckline
    nk_valley_left = request.POST.get('nk_valley_left')
    nk_valley_right = request.POST.get('nk_valley_right')
    nk_peak_left = request.POST.get('nk_peak_left')
    nk_peak_right = request.POST.get('nk_peak_right')
    nk_startdate = request.POST.get('nk_startdate')
    nk_enddate = request.POST.get('nk_enddate')
    nk_interval = request.POST.get('nk_interval')
    nk_value = request.POST.get('nk_value')

    if len(signals_selected_values) > 1:
        signals_selected_values = list(eval(signals_selected_values))
    else:
        signals_selected_values = [int(ele) for ele in list(signals_selected_values)]
        
    uth.add(
        username=str(request.user),
        start_date=start_date,
        symbol=symbol, 
        signals_selected_values=signals_selected_values, 
        up_gap_interval=up_gap_interval, 
        down_gap_interval=down_gap_interval,
        diff=diff, 
        peak_left=peak_left, 
        peak_right=peak_right, 
        valley_left=valley_left, 
        valley_right=valley_right, 
        swap_times=swap_times, 
        previous_day=previous_day, 
        survival_time=survival_time, 
        nk_valley_left=nk_valley_left, 
        nk_valley_right=nk_valley_right,
        nk_peak_left=nk_peak_left, 
        nk_peak_right=nk_peak_right, 
        nk_startdate=nk_startdate, 
        nk_enddate=nk_enddate, 
        nk_interval=nk_interval, 
        nk_value=nk_value, 
    )
    
    return JsonResponse({"msg": "Successful!"})

@csrf_exempt
def get_track_list(request):
    user = str(request.user)
    res = uth.get_track_spreads_from_user(user)

    track_data  = []
    for track in res:    
        start_date = datetime.datetime.strptime(track[1], '%b-%d-%Y')
        start_date = start_date.strftime('%Y-%m-%d')    
        ele = {
            'track_date':track[0],
            'start_date':start_date,
            'symbol':track[2],
            'signals_selected_values':track[3],
            'gap_interval':track[4],
            'diff':track[6],
            'peak_left':track[7],
            'peak_right':track[8],
            'valley_left':track[9], 
            'valley_right':track[10],  
            'swap_times':track[11],
            'previous_day':track[12],
            'survival_time':track[13],
            'nk_valley_left':track[14], 
            'nk_valley_right':track[15], 
            'nk_peak_left':track[16],
            'nk_peak_right':track[17], 
            'nk_startdate':track[18],
            'nk_enddate':track[19],
            'nk_interval':track[20],
            'nk_value':track[21],
        }
        track_data.append(ele)

    if track_data is None:
        """error handling"""
        pass
    
    return JsonResponse({"track_data": track_data}) 

@csrf_exempt
def remove_track(request):
    symbol = request.POST.get('symbol')
    start_date = request.POST.get('start_date')
    user = str(request.user)
    uth.remove(user, symbol, start_date)
    return JsonResponse({'msg': 'Successful'})

@csrf_exempt
def run_analysis(request):
    signals_selected_values = request.POST.get('signals_selected_values')
    start_date = request.POST.get('start_date')
    symbol = request.POST.get('symbol')
    peak_left = request.POST.get('peak_left')
    peak_right = request.POST.get('peak_right')
    valley_left = request.POST.get('valley_left')
    valley_right = request.POST.get('valley_right')
    diff = request.POST.get('diff')
    swap_times=request.POST.get('swap_times')
    previous_day = request.POST.get('previous_day')
    survival_time = request.POST.get('survival_time')
    gap_interval = request.POST.get('gap_interval')
    nk_valley_left = request.POST.get('nk_valley_left')
    nk_valley_right = request.POST.get('nk_valley_right')
    nk_peak_left = request.POST.get('nk_peak_left')
    nk_peak_right = request.POST.get('nk_peak_right')
    nk_startdate = request.POST.get('nk_startdate')
    nk_enddate = request.POST.get('nk_enddate')
    nk_interval = request.POST.get('nk_interval')
    nk_value = request.POST.get('nk_value')
    
    if len(signals_selected_values) > 1:
        signals_selected_values = list(eval(signals_selected_values))
    else:
        signals_selected_values = [int(ele) for ele in list(signals_selected_values)]

    
    all_signals = get_signals(
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
          nk_value
    )
    
    AllData = get_all_technical_analysis(
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
        nk_value
    )

    AllData['symbol'] = symbol
    AllData['all_signals'] = all_signals
    AllData = json.dumps(AllData)
    
    return HttpResponse(AllData)
