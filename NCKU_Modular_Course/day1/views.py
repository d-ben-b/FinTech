from django.http import JsonResponse
from django.shortcuts import render
import yfinance as yf
import pandas as pd
import numpy as np
import talib
from icecream import ic
import json


def analyze(request):
    symbol = request.GET.get("symbol")
    start = request.GET.get("start")
    end = request.GET.get("end")

    # 取得股票資料
    df = yf.download(symbol, start=start, end=end)
    if df.empty or "Volume" not in df.columns:
        return JsonResponse(
            {"error": "No data available for the selected date range."}, status=400
        )

    # 將 MultiIndex 列名簡化為單層
    df.columns = df.columns.get_level_values(0)

    # 填補 NaN 值為 0
    df["Volume"] = df["Volume"].fillna(0)

    # 計算 5 日均量
    df["5DayAvgVolume"] = talib.SMA(
        df["Volume"].values.astype(np.float64), timeperiod=5
    )
    df.rename(columns={"5DayAvgVolume": "AvgVolume"}, inplace=True)
    df["AvgVolume"].fillna(0, inplace=True)

    df["is_spike"] = df["Volume"] > df["AvgVolume"]

    for row in df.itertuples():
        ic(row)

    # 準備數據給前端
    candlestick_data = [
        [row.Index.strftime("%Y-%m-%d"), row.Open, row.High, row.Low, row.Close]
        for row in df.itertuples()
    ]
    volume_data = [
        {
            "date": row.Index.strftime("%Y-%m-%d"),
            "volume": row.Volume,
            "avg_volume": row.AvgVolume,
            "is_spike": row.is_spike,
        }
        for row in df.itertuples()
    ]
    table_data = [
        {
            "date": row.Index.strftime("%Y-%m-%d"),
            "high_volume": row.Volume,
            "five_day_ma": row.AvgVolume,
        }
        for row in df.itertuples()
        if row.is_spike  # 只顯示爆量的行
    ]

    dates = df.index.strftime("%Y-%m-%d").tolist()

    response = {
        "stock_symbol": symbol,
        "start_date": start,
        "end_date": end,
        "stock_data": candlestick_data,
        "volume_data": volume_data,
        "table_data": table_data,
        "dates": dates,
    }
    ic(response)

    return render(request, "day1.html", response)


def day1_view(request):
    return render(
        request,
        "day1.html",
        {
            "stock_symbol": "",
            "start_date": "",
            "end_date": "",
            "stock_data": [],
            "volume_data": [],
            "dates": [],
        },
    )


def analyze_from_vue(request):
    symbol = request.GET.get("symbol")
    start = request.GET.get("start")
    end = request.GET.get("end")

    # Validate input
    if not symbol or not start or not end:
        return JsonResponse({"error": "Invalid input parameters."}, status=400)

    # Fetch stock data
    try:
        df = yf.download(symbol, start=start, end=end)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    if df.empty or "Volume" not in df.columns:
        return JsonResponse(
            {"error": "No data available for the selected date range."}, status=400
        )

    # Simplify MultiIndex column names
    df.columns = df.columns.get_level_values(0)

    # Fill NaN values in Volume
    df["Volume"] = df["Volume"].fillna(0)

    # Calculate 5-day moving average of Volume
    df["5DayAvgVolume"] = talib.SMA(
        df["Volume"].values.astype(np.float64), timeperiod=5
    )
    df.rename(columns={"5DayAvgVolume": "AvgVolume"}, inplace=True)
    df["AvgVolume"].fillna(0, inplace=True)

    # Identify volume spikes
    df["is_spike"] = df["Volume"] > df["AvgVolume"]

    # Prepare data for the front-end
    candlestick_data = [
        [row.Index.strftime("%Y-%m-%d"), row.Open, row.High, row.Low, row.Close]
        for row in df.itertuples()
    ]
    volume_data = [
        {
            "date": row.Index.strftime("%Y-%m-%d"),
            "volume": row.Volume,
            "avg_volume": row.AvgVolume,
            "is_spike": row.is_spike,
        }
        for row in df.itertuples()
    ]
    table_data = [
        {
            "date": row.Index.strftime("%Y-%m-%d"),
            "high_volume": row.Volume,
            "five_day_ma": row.AvgVolume,
        }
        for row in df.itertuples()
        if row.is_spike  # Only include rows with volume spikes
    ]

    # Build response
    response = {
        "stock_symbol": symbol,
        "start_date": start,
        "end_date": end,
        "stock_data": candlestick_data,
        "volume_data": volume_data,
        "table_data": table_data,
    }
    ic(response)
    return JsonResponse(response, safe=False)
