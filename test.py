# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import time
# from icecream import ic


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
stock_id = '0000'
option = "MONTH"
base_url = "https://goodinfo.tw/StockInfo/StockBzPerformance.asp?STOCK_ID="
url = f"{base_url}{stock_id}&CHT_CAT={option}"

print(url)
