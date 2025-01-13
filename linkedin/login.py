from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time

url = 'https://www.linkedin.com/login/zh-tw?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
username = ''
password = ''

driver = webdriver.Edge()

# 如果沒有 cookies，則需要登入
driver.get(url)
time.sleep(2)

try:
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, 'session_key'))
    )
    username_input = driver.find_element(By.NAME, 'session_key')
    password_input = driver.find_element(By.NAME, 'session_password')
    username_input.send_keys(username)
    password_input.send_keys(password)
    driver.find_element(By.XPATH, '//button[@type="submit"]').click()

except:
    print('元素未找到或加載失敗')

# 等待登入完成
time.sleep(5)

# 登入後保存 cookies
pickle.dump(driver.get_cookies(), open('linkedin_cookies.pkl', 'wb'))

driver.quit()
