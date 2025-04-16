from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from datetime import datetime

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
options.binary_location = '/usr/bin/chromium-browser'

driver = webdriver.Chrome(options=options)
fra_data = {}

try:
    for label, url in fra_urls.items():
        driver.get(url)
        driver.save_screenshot(f"debug_{label}.png")  # DEBUG: zapisz screenshot

        try:
            WebDriverWait(driver, 15).until(
                EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, "iframe"))
            )
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".dce-rate-value"))
            )
            elem = driver.find_element(By.CSS_SELECTOR, '.dce-rate-value')
            value = elem.text.strip().replace(',', '.')
            fra_data[label] = value
        except Exception as e:
            fra_data[label] = f"Błąd: {str(e)}"

        driver.switch_to.default_content()

    data = {
        "data": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "fra": fra_data
    }

    with open('fra.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

finally:
    driver.quit()