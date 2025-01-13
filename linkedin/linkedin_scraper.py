from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import random
import time
import pickle

# memo the data using pandas
import pandas as pd

data = {
    'company': [],
    'title': [],
    'description': [],
}

filename = 'american_jobs_more.csv'

base_url = 'https://www.linkedin.com/jobs/search/?currentJobId=4119757602&geoId=103644278&origin=JOB_SEARCH_PAGE_JOB_FILTER&refresh=true&sortBy=R&start='

driver = webdriver.Edge()
actions = ActionChains(driver)

# Load cookies
driver.get(base_url)
for cookie in pickle.load(open('linkedin_cookies.pkl', 'rb')):
    driver.add_cookie(cookie)

PAGES = 500
OFFSET_STEP = 25
MAX_OFFSET = PAGES * OFFSET_STEP
for offset in range(0, MAX_OFFSET, OFFSET_STEP):
    print(f"Scraping page {offset // OFFSET_STEP}, {offset}: ", end='')
    url = base_url + str(offset)
    driver.get(url)
    try:
        wait = WebDriverWait(driver, 10)
        time.sleep(1 + 1 * random.random())
        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT).perform()
        time.sleep(0.5 + 0.5 * random.random())
        for _ in range(10):
            actions.send_keys(Keys.PAGE_UP).perform()
            time.sleep(0.1)
    except:
        print("Failed to load jobs")
        continue

    jobs = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-job-id]')))
    print(f"Scraping {len(jobs)} jobs")
    for job in jobs:
        actions.move_to_element(job).perform()
        job.click()
        time.sleep(1 + 2 * random.random())

        try:
            company = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="job-details-jobs-unified-top-card__company-name"]')))
            title = wait.until(EC.presence_of_element_located((By.XPATH, '//h1/a[@class="ember-view"]')))
            description = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="mt4"]/p[@dir="ltr"]')))
            company = company.text if company else ''
            title = title.text if title else ''
            description = description.text if description else ''
            data['company'].append(company)
            data['title'].append(title)
            data['description'].append(description)
        except:
            print("Failed to scrape job details")

    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

df = pd.DataFrame(data)
df.to_csv(filename, index=False)
print(f"Data saved to {filename}")
print(df)
