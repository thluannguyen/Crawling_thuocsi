from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

import pandas as pd 
import warnings 
warnings.filterwarnings('ignore')

opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
opt.add_argument("--disable-notifications")
opt.add_argument("--disable-gpu")
opt.add_argument("--headless")
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })

driver = webdriver.Chrome('chromedriver.exe', options = opt)
driver.get("https://thuocsi.vn/")

email = '0935270307'
password = 'thanhluan7702'

try:
    driver.find_element(By.CLASS_NAME, 'styles_confirm_modal_wrap__ZqfQf').find_element(By.CLASS_NAME, 'MuiButton-label').click() # off frame service 
except: 
    pass

# login 
driver.find_elements(By.CLASS_NAME, 'MuiButton-label')[1].click()
driver.find_elements(By.NAME, 'username')[0].send_keys(email)
driver.find_elements(By.NAME, 'password')[0].send_keys(password)
driver.find_element(By.CLASS_NAME, 'MuiButtonBase-root.MuiButton-root.MuiButton-text.sc-5cbc0a6a-0.gAlqpx.styles_btn_register__zCg7F').click()

# click product button
time.sleep(2)
product_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div[1]/div/div[1]/div[1]")))
time.sleep(2)
product_button.click()

# find numbers of page
time.sleep(2)
pages = driver.find_element(By.CLASS_NAME, 'style_bottomPagging__kzl7h').find_elements(By.TAG_NAME, 'button')
time.sleep(2)
n_pages = int(pages[3].text)

data_json = []

# for page in range(1, n_pages+1): 
for page in range(1, 5): # demo 5 page
    driver.execute_script("window.open();")
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[1])
    driver.implicitly_wait(2)
    driver.get(f"https://thuocsi.vn/products?page={page}")
    time.sleep(2)
    driver.current_window_handle
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # find number of product in page 
    product = soup.find('div', {'class' : 'MuiGrid-root MuiGrid-container'}).find_all('div', {'class' : 'MuiGrid-root style_customGrid__9RXds MuiGrid-item MuiGrid-grid-xs-6 MuiGrid-grid-md-4'})
    n_prod = len(product)

    for idx_prod in range(n_prod): 
        json = {'name' : '', 'price' : ''}

        name = product[idx_prod].find("span", {"class" : "styles_product_name__R1JN_"}).text.strip()
        json['name'] = name
        price = product[idx_prod].find("p", {"class" : "MuiTypography-root styles_display_price__WOBxy MuiTypography-body1"}).text.strip()
        json['price'] = price

        data_json.append(json)
    time.sleep(1)
    driver.close()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0]) # back the first link
    time.sleep(1)
driver.quit()

print("Successfully Collection by Thanh Luan's Bot Crawling!!")
print(pd.DataFrame(data_json))
pd.DataFrame(data_json).to_csv("thuocsi_data.csv", index = False)