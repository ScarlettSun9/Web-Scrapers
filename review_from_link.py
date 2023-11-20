import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

def review_from_link(url, name):
    # Define the Chrome webdriver options
    options = webdriver.ChromeOptions()
    options.page_load_strategy = "none"

    # Pass the defined options objects to initialize the web driver
    reviewDriver = Chrome(options=options)

    # Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
    reviewDriver.implicitly_wait(5)

    reviewDriver.get(url)
    time.sleep(5)

    while True:
        try:
            loadMoreButton = reviewDriver.find_element(By.XPATH, "//div[@class='Aglzs']//div//button")
            time.sleep(2)
            loadMoreButton.click()
            time.sleep(5)
        except:
            # print('Finish loading!')
            break

    index = 0
    fileRows = []

    reviews = reviewDriver.find_elements(By.CLASS_NAME, "gztbie")
    for review in reviews:
        index += 1
        reviewer = review.find_element(By.CLASS_NAME, "Nm6JXe").text
        reviewTime = review.find_element(By.CLASS_NAME, "IkzKWc").text
        star = review.find_element(By.CLASS_NAME, "B1UG8d").get_attribute('aria-label')
        reviewContent = review.find_element(By.TAG_NAME, "p").text
        helpful = review.find_element(By.CLASS_NAME, "MnTPbf").text
        try:
            others = review.find_element(By.CLASS_NAME, "WiDGcf").text
        except:
            others = ''

        row = [index, reviewer, reviewTime, star, reviewContent, helpful, others]
        print(row)
        fileRows.append(row)

    dfReview = pd.DataFrame(fileRows, columns=['index', 'reviewer', 'review time', 'rating star', 'review', 'helpful', 'other info'])
    dfReview.to_csv(f"Review of {name}.csv", index=False)
    return True
