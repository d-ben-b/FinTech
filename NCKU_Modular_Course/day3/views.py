from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import yfinance as yf
import numpy as np
import twstock

# Create your views here.
options = Options()
options.add_argument("--headless")  # 不開啟瀏覽器
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")


def fetch_stock_performance(request, stock_id, option, period):
    try:
        driver = webdriver.Chrome(
            options=options
        )
        base_url = "https://goodinfo.tw/tw/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID="
        url = f"{base_url}{stock_id}&CHT_CAT={option}"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        amg = []
        row_data = []
        months = []
        n_months = period
        ohlc_data = []  # 初始化為空列表
        ohlc = [[None] * 4 for _ in range(n_months)]
        line1, line2, line3, line4, line5, line6 = [], [], [], [], [], []

        EPS = 0
        for i in range(1, 7):
            amg_Xpath = f"//*[@id='tblDetail']/tbody/tr[2]/th[{i}]"
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, amg_Xpath))
            )
            amg.append(element.text)

        # 抓取和流線/EPS
        for i in range(0, n_months):
            id = f'row{i}'
            element = wait.until(
                EC.presence_of_element_located((By.ID, id))
            )
            row_data.append(element.text)
            row_data[i] = row_data[i].split(" ")
            months.append(row_data[i][0])
            line1.append(
                round(float(row_data[i][6] if row_data[i][6] != '-' else 0), 2))
            line2.append(
                round(float(row_data[i][7] if row_data[i][6] != '-' else 0), 2))
            line4.append(
                round(float(row_data[i][9] if row_data[i][6] != '-' else 0), 2))
            line3.append(
                round(float(row_data[i][8] if row_data[i][6] != '-' else 0), 2))
            line5.append(
                round(float(row_data[i][10]if row_data[i][6] != '-' else 0), 2))
            line6.append(
                round(float(row_data[i][11]if row_data[i][6] != '-' else 0), 2))
        EPS = round(float(row_data[0][4]), 2)
        base_url = "https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID="
        url = f"{base_url}{stock_id}&CHT_CAT={option}&PRICE_ADJ=F&SCROLL2Y=0"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        for i in range(n_months):
            id = f'row{i}'
            try:
                # 等待元素出現
                element = wait.until(
                    EC.presence_of_element_located((By.ID, id))
                )
                # 獲取元素文本
                if element.text != "-" and element.text != "":
                    ohlc_data.append(element.text)
                ohlc_data[i] = ohlc_data[i].split(" ")
                if len(ohlc_data[i]) < 4:
                    print(f"Row {i} data incomplete: {ohlc_data[i]}")
                    continue

                # 賦值給 ohlc
                ohlc[i][:] = ohlc_data[-1][2:6]
            except TimeoutException:
                print(f"Element with ID {id} not found.")
                continue

        stock_info = twstock.realtime.get(stock_id)
        bid = float(stock_info["realtime"]["best_bid_price"][-1])
        ask = float(stock_info["realtime"]["best_ask_price"][-1])

        now_price = (bid + ask) / 2

        high_price = round(float(amg[5].replace("X", "")) * EPS, 2)
        avg_price = round((float(amg[3].replace("X", "")) +
                           float(amg[2].replace("X", "")))/2 * EPS, 2)
        low_price = round(float(amg[0].replace("X", "")) * EPS, 2)
        max_price = high_price * 1.2

        result = {
            "Lines": {
                "line1": line1[::-1],
                "line2": line2[::-1],
                "line3": line3[::-1],
                "line4": line4[::-1],
                "line5": line5[::-1],
                "line6": line6[::-1],
            },
            "amg": amg,
            "months": months[::-1],
            "EPS": EPS,
            "ohlc": ohlc[::-1],
            "max_data": max_price,
            "high_price": high_price,
            "low_price": low_price,
            "avg_price": avg_price,
            "now_price": now_price,
        }
        return JsonResponse(result, safe=True, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        driver.quit()


def format_data(data):
    data = data.to_numpy().flatten().tolist()
    data = [round(x, 2) for x in data]
    return data


def ceiling_floor(request, stockSymbol, start_date, MA, MA_type, method_type):
    MA_timeperiod = MA
    neg_BIAS_std = 0
    pos_BIAS_std = 0
    neg_BIAS_mean = 0
    pos_BIAS_mean = 0
    pos_BIAS = []
    neg_BIAS = []
    ceiling = []
    ceiling_99 = []
    floor_1 = []
    floor = []
    BIAS = 0
    flag_up = []
    flag_down = []

    try:
        data = yf.download(stockSymbol + ".TW", start=start_date)
    except Exception:
        data = yf.download(stockSymbol + ".TWO", start=start_date)
    flatten_data = data["Close"].to_numpy().flatten()
    volume = data["Volume"].to_numpy().flatten()

    MA = data["Close"].rolling(
        window=MA_timeperiod).mean().to_numpy().flatten() if MA_type == "SMA" else data["Close"].rolling(window=MA_timeperiod).apply(
            lambda x: np.dot(x, np.arange(1, MA_timeperiod + 1)) / np.arange(1, MA_timeperiod + 1).sum(), raw=True).to_numpy().flatten()
    MA_cleaned = np.nan_to_num(MA, nan=0)
    MA_cleaned = np.round(MA_cleaned, 2)

    for i in range(0, len(MA_cleaned)):
        BIAS = (flatten_data[i] - MA_cleaned[i]) / \
            MA_cleaned[i] if MA_cleaned[i] != 0 else None

        if BIAS is not None:
            pos_BIAS.append(BIAS) if BIAS > 0 else neg_BIAS.append(BIAS)

    pos_BIAS.sort()
    neg_BIAS.sort()

    if method_type == 1:
        pos_BIAS_val = pos_BIAS[int(len(pos_BIAS) * 0.95)]
        neg_BIAS_val = neg_BIAS[int(len(neg_BIAS) * 0.05)]

    elif method_type == 2:
        neg_BIAS_mean = np.mean(neg_BIAS)
        pos_BIAS_mean = np.mean(pos_BIAS)
        neg_BIAS_std = np.std(neg_BIAS)
        pos_BIAS_std = np.std(pos_BIAS)

        pos_BIAS_val = pos_BIAS_mean + (pos_BIAS_std * 2)
        neg_BIAS_val = neg_BIAS_mean - (neg_BIAS_std * 2)

    else:
        pos_BIAS_val = pos_BIAS[int(len(pos_BIAS) * 0.95)]
        neg_BIAS_val = neg_BIAS[int(len(neg_BIAS) * 0.05)]
        pos_BIAS_val_99 = pos_BIAS[int(len(pos_BIAS) * 0.99)]
        neg_BIAS_val_1 = neg_BIAS[int(len(neg_BIAS) * 0.01)]

    for i in range(len(MA_cleaned)):
        ceiling.append((MA_cleaned[i] * (1 + pos_BIAS_val)).round(2))
        floor.append((MA_cleaned[i] * (1 + neg_BIAS_val)).round(2))

        if method_type == 3:
            ceiling_99.append(
                (MA_cleaned[i] * (1 + pos_BIAS_val_99)).round(2))
            floor_1.append((MA_cleaned[i] * (1 + neg_BIAS_val_1)).round(2))
            if i >= 20:
                flag_up.append(
                    1 if flatten_data[i] > ceiling[i] and volume[i] > 2 * np.mean(volume[i-20:i]) else 0)
                flag_down.append(
                    1 if flatten_data[i] < floor[i] and volume[i] > 2 * np.mean(volume[i-20:i]) else 0)
            else:
                flag_up.append(0)  # 或者其他處理方式
                flag_down.append(0)  # 或者其他處理方式
        else:
            flag_up.append(1 if flatten_data[i] > ceiling[i] else 0)
            flag_down.append(1 if flatten_data[i] < floor[i] else 0)

    try:
        result = {
            "ceiling": ceiling,
            "floor": floor,
            "MA": MA_cleaned.tolist(),
            "candle_data": {
                "Open": format_data(data["Open"]),
                "High": format_data(data["High"]),
                "Low": format_data(data["Low"]),
                "Close": format_data(data["Close"]),
            },
            "flag_up": flag_up,
            "flag_down": flag_down,
            "volume": volume.tolist(),
        } if method_type != 3 else {
            "ceiling": ceiling,
            "floor": floor,
            "ceiling_99": ceiling_99,
            "floor_1": floor_1,
            "MA": MA_cleaned.tolist(),
            "candle_data": {
                "Open": format_data(data["Open"]),
                "High": format_data(data["High"]),
                "Low": format_data(data["Low"]),
                "Close": format_data(data["Close"]),
            },
            "flag_up": flag_up,
            "flag_down": flag_down,
            "volume": volume.tolist(),
        }
        return JsonResponse(result, safe=True, status=200)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
