import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

# Define the Chrome webdriver options
options = webdriver.ChromeOptions()
options.page_load_strategy = "none"

# Pass the defined options objects to initialize the web driver
driver = Chrome(options=options)

# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)

url = "https://chromewebstore.google.com/category/extensions/productivity/communication"

driver.get(url)
time.sleep(10)

while True:
    try:
        loadMoreButton = driver.find_element(By.XPATH, "//div[@class='acFDHd']//div//div//div//button")
        time.sleep(2)
        loadMoreButton.click()
        time.sleep(5)
    except:
        # print('Finish loading!')
        break

index = 0
fileRows = []

items = driver.find_elements(By.CLASS_NAME, 'cD9yc')
for item in items:
    link = item.find_element(By.CLASS_NAME, 'UvhDdd').get_property('href')
    name = item.find_element(By.CLASS_NAME, 'GzKZcb').text
    index += 1
    oneRow = []
    oneRow.append(index)
    oneRow.append(name)
    oneRow.append(link)
    fileRows.append(oneRow)
    # print(index)
    # print(name, link)

df = pd.DataFrame(fileRows, columns=['index', 'name', 'link'])
df.to_csv('communication.csv', index=False)

