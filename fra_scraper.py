from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
from datetime import datetime
import time

fra_urls = {
  "1x4": "https://www.patria.cz/kurzy/PLN/1x4/fra/graf.html",
  "3x6": "https://www.patria.cz/kurzy/PLN/3x6/fra/graf.html",
  "6x9": "https://www.patria.cz/kurzy/PLN/6x9/fra/graf.html",
  "9x12": "https://www.patria.cz/kurzy/PLN/9x12/fra/graf.html"
}

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.binary_location = '/usr/bin/chromium-browser'  # ← to dodajemy

driver = webdriver.Chrome(options=options)

fra_data = {}

try:
    for label, url in fra_urls.items():
        driver.get(url)
        time.sleep(5)
        elem = driver.find_element(By.CSS_SELECTOR, '.dce-rate-value')
        value = elem.text.strip().replace(',', '.')
        fra_data[label] = value

    data = {
        "data": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "fra": fra_data
    }

    with open('fra.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

finally:
    driver.quit()
