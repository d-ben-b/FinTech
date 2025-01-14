from django.http import JsonResponse
import requests
from icecream import ic
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time


def clean_float_list(data):
    return [float(d) for d in data if d.replace(".", "", 1).isdigit()]


def fetch_stock_performance(request, stock_id, n_months):
    """
    爬取 GoodInfo 的股票數據並處理多行表頭
    """
    url = f"https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID={stock_id}"

    ALL_PBR = []
    ALL_PER = []
    PBR_avg = {}
    PER_avg = {}
    EPS = []

    # 設定 Selenium 瀏覽器
    options = Options()
    options.add_argument("--headless")  # 無頭模式
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get(url)
    time.sleep(3)  # 等待網頁加載
    select_element = driver.find_element(By.ID, "selSheet")
    select = Select(select_element)
    select.select_by_value("PER/PBR")  # 選擇 "PER/PBR"
    time.sleep(2)  # 等待表格刷新

    try:
        # 本淨比法
        print("-------------------------------本淨比法-----------------------------")
        # 抓取最低PBR
        for i in range(3, n_months + 4):  # 從第 3 行開始
            try:
                path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[16]"
                PER_element = driver.find_element(By.XPATH, path)
                PER_text = PER_element.text.strip()  # 提取文字並去除空格
                if PER_text and PER_text != "-":  # 檢查是否為空
                    ALL_PBR.append(float(PER_text))  # 轉換為浮點數並添加到列表
            except Exception as e:
                print(f"Error on row {i}: {e}")  # 打印錯誤，便於排查
                continue

        # 計算平均值
        if ALL_PBR:
            PBR_avg["low PBR"] = sum(ALL_PBR) / len(ALL_PBR)  # 計算平均值
        else:
            PBR_avg["low PBR"] = None  # 如果沒有有效數據，設置為 None
        ALL_PBR.clear()

        # 抓取最平均PBR
        for i in range(3, n_months + 4):  # 從第 3 行開始
            try:
                path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[17]"
                PER_element = driver.find_element(By.XPATH, path)
                PER_text = PER_element.text.strip()  # 提取文字並去除空格
                if PER_text and PER_text != "-":  # 檢查是否為空
                    ALL_PBR.append(float(PER_text))  # 轉換為浮點數並添加到列表
            except Exception as e:
                print(f"Error on row {i}: {e}")  # 打印錯誤，便於排查
                continue

        # 計算平均值
        if ALL_PBR:
            PBR_avg["average PBR"] = sum(ALL_PBR) / len(ALL_PBR)  # 計算平均值
        else:
            PBR_avg["average PBR"] = None  # 如果沒有有效數據，設置為 None
        ALL_PBR.clear()

        # 抓取最high PBR
        for i in range(3, n_months + 4):  # 從第 3 行開始
            try:
                path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[15]"
                PER_element = driver.find_element(By.XPATH, path)
                PER_text = PER_element.text.strip()  # 提取文字並去除空格
                if PER_text and PER_text != "-":  # 檢查是否為空
                    ALL_PBR.append(float(PER_text))  # 轉換為浮點數並添加到列表
            except Exception as e:
                print(f"Error on row {i}: {e}")  # 打印錯誤，便於排查
                continue

        # 計算平均值
        if ALL_PBR:
            PBR_avg["high PBR"] = sum(ALL_PBR) / len(ALL_PBR)  # 計算平均值
        else:
            PBR_avg["high PBR"] = None  # 如果沒有有效數據，設置為 None
        ALL_PBR.clear()

        # 抓BPS抓BPS
        path = "/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[4]/td[14]"
        BPS = driver.find_element(By.XPATH, path).text.strip()
        path = "/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[4]/td[1]"
        BPS_title = driver.find_element(By.XPATH, path).text.strip()

        low_price = PBR_avg["low PBR"] * float(BPS)
        avg_price = PBR_avg["average PBR"] * float(BPS)
        high_price = PBR_avg["high PBR"] * float(BPS)

        # 本益比法
        print("-------------------------------本益比法-----------------------------")
        # 抓取最低PER
        for i in range(3, n_months + 4):  # 從第 3 行開始
            try:
                path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[12]"
                PER_element = driver.find_element(By.XPATH, path)
                PER_text = PER_element.text.strip()  # 提取文字並去除空格
                if PER_text and PER_text != "-":  # 檢查是否為空
                    ALL_PER.append(float(PER_text))  # 轉換為浮點數並添加到列表
            except Exception as e:
                print(f"Error on row {i}: {e}")  # 打印錯誤，便於排查
                continue

        # 計算平均值
        if ALL_PER:
            PER_avg["low PER"] = sum(ALL_PER) / len(ALL_PER)  # 計算平均值
        else:
            PER_avg["low PER"] = None  # 如果沒有有效數據，設置為 None
        ALL_PER.clear()

        # 抓取最平均PBR
        for i in range(3, n_months + 4):  # 從第 3 行開始
            try:
                path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[13]"
                PER_element = driver.find_element(By.XPATH, path)
                PER_text = PER_element.text.strip()  # 提取文字並去除空格
                if PER_text and PER_text != "-":  # 檢查是否為空
                    ALL_PER.append(float(PER_text))  # 轉換為浮點數並添加到列表
            except Exception as e:
                print(f"Error on row {i}: {e}")  # 打印錯誤，便於排查
                continue

        # 計算平均值
        if ALL_PER:
            PER_avg["average PER"] = sum(ALL_PER) / len(ALL_PER)  # 計算平均值
        else:
            PER_avg["average PER"] = None  # 如果沒有有效數據，設置為 None
        ALL_PER.clear()

        # 抓取最high PBR
        for i in range(3, n_months + 4):  # 從第 3 行開始
            try:
                path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[11]"
                PER_element = driver.find_element(By.XPATH, path)
                PER_text = PER_element.text.strip()  # 提取文字並去除空格
                if PER_text and PER_text != "-":  # 檢查是否為空
                    ALL_PER.append(float(PER_text))  # 轉換為浮點數並添加到列表
            except Exception as e:
                print(f"Error on row {i}: {e}")  # 打印錯誤，便於排查
                continue

        # 計算平均值
        if ALL_PER:
            PER_avg["high PER"] = sum(ALL_PER) / len(ALL_PER)  # 計算平均值
        else:
            PER_avg["high PER"] = None  # 如果沒有有效數據，設置為 None
        ALL_PER.clear()

        # 抓取EPS
        for i in range(3, n_months + 4):
            EPS_path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[10]"
            EPS_data = driver.find_element(By.XPATH, EPS_path).text.strip()
            if EPS_data and EPS_data != "-":
                EPS.append(EPS_data)
        EPS_avg = (float(EPS[0]) + (sum([float(i) for i in EPS]) / len(EPS))) / 2

        low_price_per = EPS_avg * PER_avg["low PER"]
        avg_price_per = EPS_avg * PER_avg["average PER"]
        high_price_per = EPS_avg * PER_avg["high PER"]

        # 高低價法
        print("-------------------------------高低價法-----------------------------")
        high = []
        avg = []
        low = []

        # 抓取最高價
        for i in range(3, n_months + 4):
            path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[4]"
            price = driver.find_element(By.XPATH, path).text.strip()
            if price and price != "-":
                high.append(price)
        if high:
            high_avg = sum(high) / len(high)  # 計算平均值
        else:
            high_avg = None  # 如果沒有有效數據，設置為 None

        # 抓取最低價
        for i in range(3, n_months + 4):
            path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[5]"
            price = driver.find_element(By.XPATH, path).text.strip()
            if price and price != "-":
                low.append(price)
        if low:
            low_avg = sum(low) / len(low)
        else:
            low_avg = None

        # 抓取平均價
        for i in range(3, n_months + 4):
            path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[6]"
            price = driver.find_element(By.XPATH, path).text.strip()
            if price and price != "-":
                avg.append(price)

        if avg:
            avg_avg = sum(avg) / len(avg)
        else:
            avg_avg = None

        # 股利法：
        print("-------------------------------股利法-----------------------------")
        select_element = driver.find_element(By.ID, "selSheet")
        select = Select(select_element)
        select.select_by_value("股利政策(發放年度)")  # 選擇 "股利政策(發放年度)"
        time.sleep(2)  # 等待表格刷新

        dividend = []

        # 抓取低股利
        for i in range(5, n_months + 6):
            path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[8]"
            Dividend = driver.find_element(By.XPATH, path).text.strip()
            if Dividend and Dividend != "-":
                dividend.append(Dividend)
        if dividend:
            avg = sum(dividend) / len(dividend)
        else:
            avg = None

        low_dividend = avg * 15
        avg_dividend = avg * 20
        high_dividend = avg * 30

        # 組織數據
        result = {
            "PBR": {
                "low": low_price,  # 基於 PBR 計算的低價
                "avg": avg_price,  # 基於 PBR 計算的中價
                "high": high_price,  # 基於 PBR 計算的高價
            },
            "PER": {
                "low": low_price_per,  # 基於 PER 計算的低價
                "avg": avg_price_per,  # 基於 PER 計算的中價
                "high": high_price_per,  # 基於 PER 計算的高價
            },
            "high_low": {
                "high": high_avg,  # 最高價
                "low": low_avg,  # 最低價
                "avg": avg_avg,  # 平均價
            },
            "dividend": {
                "low": low_dividend,  # 低股利
                "avg": avg_dividend,  # 平均股利
                "high": high_dividend,  # 高股利
            },
        }

        return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    finally:
        driver.quit()


def fetch_stock_data(request, stock_id):
    # API URL
    url = f"https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_{stock_id}.tw&json=1&delay=0"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("rtcode") == "0000":
            stock_info = data.get("msgArray", [])[0]
            ic(stock_info)
            return JsonResponse(stock_info, safe=False)
        else:
            return JsonResponse({"error": data.get("rtmessage")}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def fetch_stock_analysis(request, stock_id):
    try:
        # 使用 yfinance 獲取財務數據
        stock = yf.Ticker(f"{stock_id}.TW")
        info = stock.info

        # 獲取數據
        book_value = info.get("bookValue")  # 每股淨值 (BPS)
        trailing_eps = info.get("trailingEps")  # 每股收益 (EPS)
        market_cap = info.get("marketCap")  # 市值
        total_book_value = (
            book_value * info.get("sharesOutstanding")
            if book_value and info.get("sharesOutstanding")
            else None
        )

        if not book_value or not trailing_eps or not market_cap:
            return JsonResponse({"error": "無法獲取完整的財務數據"}, status=400)

        # 實際計算 PBR 和 PER
        current_pbr = market_cap / total_book_value if total_book_value else None
        current_per = (
            market_cap / (trailing_eps * info.get("sharesOutstanding"))
            if trailing_eps and info.get("sharesOutstanding")
            else None
        )

        # 返回結果
        result = {
            "current_pbr": current_pbr,
            "current_per": current_per,
            "pbr_method": [book_value * 0.8, book_value, book_value * 1.2],  # 範例範圍
            "per_method": [
                trailing_eps * 10,
                trailing_eps * 15,
                trailing_eps * 20,
            ],  # 範例範圍
        }
        return JsonResponse(result, safe=False)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
