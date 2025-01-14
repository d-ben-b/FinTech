from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from icecream import ic


# 設定瀏覽器選項
options = Options()
# options.add_argument("--headless")  # 不開啟瀏覽器
options.add_argument("--disable-gpu")  # 禁用GPU加速

# 啟動 WebDriver
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

try:
    url = f"https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID=2330"
    driver.get(url)
    time.sleep(3)
    ALL_PER = []
    PER_avg = {}
    n_months = 5
    # 切換到 "PER/PBR" 選項
    select_element = driver.find_element(By.ID, "selSheet")
    select = Select(select_element)
    select.select_by_value("股利發放年度")  # 選擇 "PER/PBR"
    time.sleep(2)  # 等待表格刷新

    # 抓取最低PBR
    for i in range(3, n_months + 4):  # 從第 3 行開始
        try:
            path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[5]/td[8]"
            PER_element = driver.find_element(By.XPATH, path)
            PER_text = PER_element.text.strip()  # 提取文字並去除空格
            ic(PER_text)
            if PER_text:  # 檢查是否為空
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

    # 抓取最avgPBR
    for i in range(3, n_months + 4):
        path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[17]"
        PER = driver.find_element(By.XPATH, path)
        ALL_PER.append(PER)
    PER_avg["average PER"] = sum([float(i[0]) for i in ALL_PER]) / len(ALL_PER)

    ALL_PER.clear()

    # 抓取最high PBR
    for i in range(3, n_months + 4):
        path = f"/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[{i}]/td[15]"
        PER = driver.find_element(By.XPATH, path)
        ALL_PER.append(PER)
    PER_avg["high PER"] = sum([float(i[0]) for i in ALL_PER]) / len(ALL_PER)

    # 抓BPS抓BPS
    path = "/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[4]/td[14]"
    BPS = driver.find_element(By.XPATH, path)
    path = "/html/body/table[2]/tbody/tr[2]/td[3]/main/section[2]/div/div/table[1]/tbody/tr[4]/td[1]"
    BPS_title = driver.find_element(By.XPATH, path)

    ic(PER_avg)
    ic(BPS_title.text)
    ic(BPS.text)


finally:
    # 關閉瀏覽器
    driver.quit()
