from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
import time
from icecream import ic
import twstock

# Create your views here.
options = Options()
options.add_argument("--headless")  # 不開啟瀏覽器
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")


def fetch_stock_performance(request, stock_id, option, period):
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
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
