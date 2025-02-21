from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd

options = Options()
website = 'https://www.adamchoi.co.uk/teamgoals/detailed'

options.headless = True

driver = webdriver.Chrome(options=options)


driver.get(website)
all_matches_button = driver.find_element(By.XPATH, '//label[@analytics-event="All matches"]')
all_matches_button.click()
matches = driver.find_elements(By.TAG_NAME,'tr')
date = []
for match in matches:
    try:
        date_text = match.find_element(By.XPATH, "./td[1]").text  # Extract first <td> (date column)
        date.append(date_text)  # Append the extracted text
    except:
        print("Skipping row (No date found).")  # Skip if the row doesn't contain a <td>

df = pd.DataFrame({'date':date})
df.to_csv('matches2.csv', index=False)
print(df)
input("Press Enter to close the browser...")
driver.quit()
