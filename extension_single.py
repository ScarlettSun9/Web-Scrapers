import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from review_from_link import review_from_link
import csv

# Define the Chrome webdriver options
options = webdriver.ChromeOptions()
options.page_load_strategy = "none"

# Pass the defined options objects to initialize the web driver
driver = Chrome(options=options)

# Set an implicit wait of 5 seconds to allow time for elements to appear before throwing an exception
driver.implicitly_wait(5)

def basic_info(url):
    driver.get(url)
    time.sleep(5)

    name = driver.find_element(By.CLASS_NAME, "Pa2dE").text

    try:
        establishedPublisherBadge = driver.find_element(By.CLASS_NAME, "cJI8ee").text
    except:
        establishedPublisherBadge = ''

    try:
        featuredBadge = driver.find_element(By.XPATH, "//div[@class='j3zrsd']//span[@class='OmOMFc']").text
    except:
        featuredBadge = ''

    userNumber = driver.find_element(By.XPATH, "//div[@class='F9iKBc']").text

    try:
        overviewButton = driver.find_element(By.CLASS_NAME, "vZf0bf")
        overviewButton.click()
    except:
        overviewButton = None
    overview = driver.find_element(By.XPATH, "//div[@class='K1RSbf ']").text

    totalRating = driver.find_element(By.XPATH, "//h2[@class='kavJkb Yemige']//span[@class='yf8lh']").text

    ratingNumber = driver.find_element(By.XPATH, "//h2[@class='kavJkb Yemige']//span[@class='PmmSTd']").text

    # Details
    details = driver.find_element(By.CLASS_NAME, "SOAK0")
    version = details.find_element(By.XPATH, "//li[@class='Qt4bne HV0oG']//div[2]").text
    updated = details.find_element(By.XPATH, "//li[@class='Qt4bne kBFnc']//div[2]").text
    try:
        offeredBy = details.find_element(By.XPATH, "//li[@class='Qt4bne rlxkgb']//div[2]").text
    except:
        offeredBy = ''
    size = details.find_element(By.XPATH, "//li[@class='Qt4bne ZEfx6b']//div[2]").text
    language = details.find_element(By.XPATH, "//li[@class='Qt4bne ukkdxf']//div[2]//div").text
    try:
        developer = details.find_element(By.XPATH, "//li[@class='Qt4bne Lj9Zzc']//div[2]//div[@class='Lj9Zzc']//div[@class='C2WXF']").text
    except:
        developer = ''
    try:
        website = details.find_element(By.XPATH, "//li[@class='Qt4bne Lj9Zzc']//div[2]//div[@class='Lj9Zzc']//a").get_attribute('href')
    except:
        website = ''

    emailButton = details.find_element(By.XPATH, "//li[@class='Qt4bne Lj9Zzc']//div[2]//div[@class='Lj9Zzc']//details[@class='nJ6Dxb']")
    emailButton.click()
    email = emailButton.find_element(By.CLASS_NAME, "yNyGQd").text
    traderOrNot = details.find_element(By.XPATH, "//li[@class='Qt4bne C0lQ7e']//div[1]").text
    traderOrNotContent = details.find_element(By.XPATH, "//li[@class='Qt4bne C0lQ7e']//div[2]").text

    # Privacy
    privacy = driver.find_element(By.XPATH, "//section[@class='H8vIqf']//div[2]//div[@class='HPlN1b']")
    try:
        dataCollection1 = privacy.find_element(By.XPATH, "//div[@class='zogkbb']//div[1]").text
    except:
        dataCollection1 = ''
    try:
        dataCollection2 = privacy.find_element(By.XPATH, "//div[@class='jHXffc']//span").text
    except:
        dataCollection2 = ''
    dataCollection = dataCollection1 + dataCollection2

    dataUse = privacy.find_element(By.CLASS_NAME, "IyszAe").text

    row = [name, url, establishedPublisherBadge, featuredBadge, userNumber, overview, totalRating, ratingNumber, version, updated, offeredBy, size, language, developer, website, email, traderOrNot, traderOrNotContent, dataCollection, dataUse]

    # reviews
    try:
        seeAllReviewsButton = driver.find_element(By.XPATH, "//div[@class='VfPpkd-dgl2Hf-ppHlrf-sM5MNb']//div//a")
        seeAllReviewsLink = url + '/reviews'
        print(seeAllReviewsLink)
        dfReview = review_from_link(seeAllReviewsLink, name)
        if dfReview:
            print(f'Review - {name}.csv saved!')
    except:
        # save reviews from current page into an independent review file
        seeAllReviewsLink = None
        index = 0
        fileRows = []
        reviewArea = driver.find_element(By.XPATH,
                                         "//section[@class='H8vIqf Yemige']//div[@jsname='bN97Pc']//div[@class='EC1Ti']")
        if len(reviewArea.text) != 0:
            reviews = reviewArea.find_elements(By.CLASS_NAME, "gztbie")
            for review in reviews:
                reviewer = review.find_element(By.CLASS_NAME, "Nm6JXe").text
                star = review.find_element(By.CLASS_NAME, "B1UG8d").get_attribute('aria-label')
                reviewTime = review.find_element(By.CLASS_NAME, "IkzKWc").text
                reviewContent = review.find_element(By.TAG_NAME, "p").text
                helpful = review.find_element(By.CLASS_NAME, "MnTPbf").text
                try:
                    others = review.find_element(By.CLASS_NAME, "WiDGcf").text
                except:
                    others = ''
                index += 1
                oneRow = []
                oneRow.extend([index, reviewer, reviewTime, star, reviewContent, helpful, others])
                fileRows.append(oneRow)
        else:
            oneRow = ['', '', '', '', '', '', '']
            fileRows.append(oneRow)
        dfReview = pd.DataFrame(fileRows, columns=['index', 'reviewer', 'review time', 'rating star', 'review', 'helpful', 'other info'])
        dfReview.to_csv(f'Review - {name}.csv', index=False)

    print(row)
    return row

if __name__ == '__main__':
    communication = pd.read_csv('communication.csv')
    communicationLinks = communication['link'].tolist()
    with open('communication_extensions.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Name', 'Link', 'Established Publisher Badge', 'Featured Badge', 'Number of User', 'Overview', 'Total Rating', 'Number of Rating', 'Version', 'Update', 'Offered By', 'Size', 'Language', 'Developer', 'Website', 'Email', 'Trader Or Not', 'Trader Or Not Content', 'Data Collection', 'Data Usage'])

        for link in communicationLinks:
            basicInfoRow = basic_info(link)
            print(basicInfoRow)
            writer.writerow(basicInfoRow)
