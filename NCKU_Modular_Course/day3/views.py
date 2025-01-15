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

# Create your views here.
options = Options()
options.add_argument("--headless")  # 不開啟瀏覽器
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")


def fetch_stock_performance(request, stock_id, option):
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        url = f"https://goodinfo.tw/tw/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID={stock_id}&CHT_CAT={
            option}"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        amg = []
        row_data = []
        months = []
        n_months = 5
        ohlc_data = []  # 初始化為空列表
        ohlc = [[None] * 4 for _ in range(n_months)]  # 假設每個項目有 6 個欄位
        line1, line2, line3, line4, line5, line6 = [], [], [], [], [], []

        EPS = 0
        for i in range(1, 7):
            amg_Xpath = f"//*[@id='tblDetail']/tbody/tr[2]/th[{i}]"
            element = wait.until(
                EC.presence_of_element_located((By.XPATH, amg_Xpath))
            )
            amg.append(float(element.text.replace("X", "")))

        # 抓取和流線/EPS
        for i in range(0, n_months):
            id = f'row{i}'
            element = wait.until(
                EC.presence_of_element_located((By.ID, id))
            )
            row_data.append(element.text)
            row_data[i] = row_data[i].split(" ")
            months.append(row_data[i][0])
            line1.append(round(float(row_data[i][6]), 2))
            line2.append(round(float(row_data[i][7]), 2))
            line3.append(round(float(row_data[i][8]), 2))
            line4.append(round(float(row_data[i][9]), 2))
            line5.append(round(float(row_data[i][10]), 2))
            line6.append(round(float(row_data[i][11]), 2))
        EPS = round(float(row_data[0][4]), 2)

        url = "https://goodinfo.tw/tw/ShowK_Chart.asp?STOCK_ID=2330&CHT_CAT=MONTH&PRICE_ADJ=F&SCROLL2Y=0"
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        for i in range(0, n_months):
            id = f'row{i}'
            try:
                # 等待元素出現
                element = wait.until(
                    EC.presence_of_element_located((By.ID, id))
                )
                # 獲取元素文本
                ohlc_data.append(element.text)
                ohlc_data[i] = ohlc_data[i].split(" ")

                # 檢查數據完整性
                if len(ohlc_data[i]) < 6:
                    print(f"Insufficient data in row {i}: {ohlc_data[i]}")
                    continue

                # 賦值給 ohlc
                ohlc[i][:] = ohlc_data[i][2:6]  # 假設目標數據在索引 2 到 5
            except TimeoutException:
                print(f"Element with ID {id} not found.")
                continue

        result = {
            "Lines": {
                "line1": line1,
                "line2": line2,
                "line3": line3,
                "line4": line4,
                "line5": line5,
                "line6": line6,
            },
            "amg": amg,
            "months": months,
            "EPS": EPS,
            "ohlc": ohlc,
        }
        return JsonResponse(result, safe=True, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    finally:
        driver.quit()
