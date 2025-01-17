from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import yfinance as yf
import time
import numpy as np
import talib
from icecream import ic
from math import inf


# # 設定瀏覽器選項
# options = Options()
# options.add_argument("--headless")  # 不開啟瀏覽器
# options.add_argument("--disable-gpu")  # 禁用GPU加速
# options.add_argument(
#     "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")


# # 啟動 WebDriver
# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()), options=options
# )

# try:
#     url = f"https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID=2330&CHT_CAT=MONTH&PRICE_ADJ=F&SCROLL2Y=0"
#     driver.get(url)
#     wait = WebDriverWait(driver, 10)
#     amg = []
#     PER_avg = {}
#     row_data = []
#     n_months = 5

#     # 抓取最低PBR
#     for i in range(0, n_months):
#         id = f'row{i}'
#         element = wait.until(
#             EC.presence_of_element_located((By.ID, id))
#         )
#         row_data.append(element.text)
#         row_data[i] = row_data[i].split(" ")
#     ic(row_data)
# finally:
#     # 關閉瀏覽器
#     driver.quit()
# stock_id = '0000'
# option = "MONTH"
# base_url = "https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID="
# url = f"{base_url}{stock_id}&CHT_CAT={option}"

# print(url)
stockSymbol = "2330"
start_date = "2024-01-01"
MA_timeperiod = 20
pos_BIAS = []
neg_BIAS = []
celing = []
floor = []
BIAS = 0
try:
    data = yf.download(stockSymbol + ".TW", start=start_date)
except Exception:
    data = yf.download(stockSymbol + ".TWO", start=start_date)
flatten_data = data["Close"].to_numpy().flatten()
price = data["Volume"].to_numpy().flatten()

# MA = talib.SMA(flatten_data, timeperiod=MA_timeperiod)
# print(MA)
# MA = data["Close"].rolling(window=MA_timeperiod).mean()
# print(MA.to_numpy().flatten())
MA = talib.WMA(flatten_data, timeperiod=MA_timeperiod)
print(MA)
weights = np.arange(1, MA_timeperiod + 1)
MA = data["Close"].rolling(window=MA_timeperiod).apply(
    lambda x: np.dot(x, weights) / weights.sum(), raw=True
)
print(MA.to_numpy().flatten())

# # TODO: WMA
# MA_cleaned = np.nan_to_num(MA, nan=0)
# MA_cleaned = np.round(MA_cleaned, 2)


# for i in range(0, len(MA_cleaned)):
#     BIAS = (flatten_data[i] - MA_cleaned[i]) / \
#         MA_cleaned[i] if MA_cleaned[i] != 0 else None

#     if BIAS is not None:
#         pos_BIAS.append(BIAS) if BIAS > 0 else neg_BIAS.append(BIAS)

# pos_BIAS.sort()
# neg_BIAS.sort()
# pos_BIAS_val = pos_BIAS[int(len(pos_BIAS) * 0.95)]
# neg_BIAS_val = neg_BIAS[int(len(neg_BIAS) * 0.05)]

# for i in range(0, len(MA_cleaned)):
#     celing.append(MA_cleaned[i] * (1 + pos_BIAS_val))
#     floor.append(MA_cleaned[i] * (1 + neg_BIAS_val))
#     ic(celing[i], floor[i], i)
