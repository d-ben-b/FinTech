# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select, WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import time
from icecream import ic


# # 設定瀏覽器選項
# options = Options()
# options.add_argument("--headless")  # 不開啟瀏覽器
# options.add_argument("--disable-gpu")  # 禁用GPU加速

# # 啟動 WebDriver
# driver = webdriver.Chrome(
#     service=Service(ChromeDriverManager().install()), options=options
# )

# try:
#     url = f"https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID=2330"
#     driver.get(url)
#     wait = WebDriverWait(driver, 10)
#     EPS = []
#     PER_avg = {}
#     n_months = 5
#     # 切換到 "PER/PBR" 選項
#     select_element = driver.find_element(By.ID, "selSheet")
#     select = Select(select_element)
#     select.select_by_value("PER/PBR")  # 選擇 "PER/PBR"
#     time.sleep(2)  # 等待表格刷新

#     # 抓取最低PBR
#     for i in range(3, n_months + 4):
#         EPS_path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[10]"
#         EPS_data = driver.find_element(By.XPATH, EPS_path).text.strip()
#         if EPS_data and EPS_data != "-":
#             EPS.append(EPS_data)
#     EPS_avg = (float(EPS[0]) + (sum([float(i) for i in EPS]) / len(EPS))) / 2
#     # 計算平均值
#     ic(EPS_avg)
# finally:
#     # 關閉瀏覽器
#     driver.quit()

arr = {}
arr["assd asdas"] = 1
ic(arr.clear())
