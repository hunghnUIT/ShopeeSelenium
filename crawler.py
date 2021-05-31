from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

# Settings
from settings import (
    WAIT_TIME_LOAD_PAGE, NUMBER_PARTS_PAGE_HEIGHT, 
    CLASS_FOR_CARD_ITEM, CLASS_FOR_NAME_ITEM,
    CLASS_FOR_ROW_STARS, CLASS_FOR_STAR
)

# Functions
from helper import ( 
    process_item_url, proccess_category_url, calculate_rating, 
    convert_string_to_number, get_current_time_in_ms,
)



driver = webdriver.Edge()

input_url = 'https://shopee.vn/%C4%90i%E1%BB%87n-Tho%E1%BA%A1i-Ph%E1%BB%A5-Ki%E1%BB%87n-cat.84'

driver.get(input_url)

idx = 0

while True:
    try:
        myElem = WebDriverWait(driver, WAIT_TIME_LOAD_PAGE).until(
            EC.presence_of_element_located((By.CLASS_NAME, CLASS_FOR_CARD_ITEM)))
        
        # Scroll to deal with lazy load.
        page_height = driver.execute_script("return document.body.scrollHeight")
        each_part_height = page_height//NUMBER_PARTS_PAGE_HEIGHT
        for part in range(1, NUMBER_PARTS_PAGE_HEIGHT): # The part end the first part include no item
            y = part * each_part_height
            driver.execute_script(f'window.scrollTo(0, {y});')

        # query all items
        items = driver.find_elements_by_class_name(CLASS_FOR_CARD_ITEM)
        category_id = proccess_category_url(input_url)

        if (items):
            for el in items:
                try:
                    item = {} # FIXME change to model later.
                    product_url = el.find_element_by_tag_name('a').get_attribute('href')
                    info_from_url = process_item_url(product_url)
                    row_rating_stars = el.find_elements_by_class_name(CLASS_FOR_ROW_STARS)
                    stars = []
                    for star in row_rating_stars:
                        stars.append(star.find_element_by_class_name(CLASS_FOR_STAR).get_attribute('style'))
                    sold = el.find_element_by_class_name('go5yPW').text

                    item['id'] = info_from_url['itemId']
                    item['name'] = el.find_element_by_class_name(CLASS_FOR_NAME_ITEM).text
                    item['sellerId'] = info_from_url['sellerId']
                    item['categoryId'] = category_id
                    item['thumbnailUrl'] =  el.find_element_by_tag_name('img').get_attribute('src')
                    item['productUrl'] = product_url
                    item['rating'] = calculate_rating(stars) if stars else 0
                    item['totalReview'] = convert_string_to_number(sold.split(" ")[-1]) if sold else 0
                    item['update'] = get_current_time_in_ms()

                    print(item)
                except NoSuchElementException:
                    continue

    except TimeoutException:
        print("Loading took too much time!")

    if idx <= 3:
        idx += 1
        nextButton = driver.find_element_by_class_name('shopee-icon-button--right')
        ActionChains(driver).click(nextButton).perform()
        continue
    else:
        break

driver.quit()


'''
id, name, sellerId, categoryId, rating, thumbnailUrl, 
totalReview, expired, productUrl, currentPrice,
platform, "shopee", update, lastPriceChange
'''
