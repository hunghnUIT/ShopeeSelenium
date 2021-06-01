from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

# Settings
from settings import (
    WAIT_TIME_LOAD_PAGE, NUMBER_PARTS_PAGE_HEIGHT, 
    CLASS_NAME_CARD_ITEM, MAXIMUM_PAGE_NUMBER, 
    LOAD_ITEM_SLEEP_TIME, 
)

# Functions
from helper import ( 
    proccess_category_url,
)
from controllers.item import (
    extract_data_from_category_dom_object, extract_field_from_category_dom_object
)



driver = webdriver.Firefox()

# input_url = 'https://shopee.vn/%C4%90i%E1%BB%87n-Tho%E1%BA%A1i-Ph%E1%BB%A5-Ki%E1%BB%87n-cat.84'
# input_url = 'https://shopee.vn/Gi%C3%A1-%C4%91%E1%BB%A1-K%E1%BA%B9p-cat.84.8728?page=0&sortBy=ctime'
input_url = 'https://shopee.vn/Gi%C3%A1-%C4%91%E1%BB%A1-K%E1%BA%B9p-cat.84.8728?locations=V%C4%A9nh%20Ph%C3%BAc&page=6&sortBy=ctime'

driver.get(input_url)

category_id = proccess_category_url(input_url)

page = 1
last_page_item_number = 0
count = 0 # temp

while True:
    # Format: [{idx: 1, item_info: {item}}, {idx: 6, item_info: {item}}]
    list_items_failed = []

    try:
        myElem = WebDriverWait(driver, WAIT_TIME_LOAD_PAGE).until(
            EC.presence_of_element_located((By.CLASS_NAME, CLASS_NAME_CARD_ITEM)))
        
        # Scroll to deal with lazy load.
        page_height = driver.execute_script("return document.body.scrollHeight")
        each_part_height = page_height//NUMBER_PARTS_PAGE_HEIGHT
        for part in range(1, NUMBER_PARTS_PAGE_HEIGHT-2): # Many the first parts, the end parts include no item
            y = part * each_part_height
            driver.execute_script(f'window.scrollTo(0, {y});')
            sleep(LOAD_ITEM_SLEEP_TIME)

        # query all items
        items = driver.find_elements_by_class_name(CLASS_NAME_CARD_ITEM)

        if len(items) == last_page_item_number and last_page_item_number < 50:
            print(f'Done crawling category {category_id}, last page: {page - 1}') # start from 1
            break

        if (items):
            for idx, el in enumerate(items):
                result = extract_data_from_category_dom_object(el, category_id)
                if not result['success']:
                    list_items_failed.append({
                        'idx': idx,
                        'item_info': result['data'],
                    })
                else:
                    count += 1
                    # print(result['data'])

        # Format "list_items_failed": [{idx: 1, item_info: {item}}, {idx: 6, item_info: {item}}]
        if list_items_failed:
            # try again twice
            for time in range(2):
                for i, item in enumerate(list_items_failed):
                    dom_object = items[item['idx']]
                    item_info = item['item_info']
                    if item_info: # A few fields failed
                        if item_info['thumbnailUrl'] == None:
                            result = extract_field_from_category_dom_object('thumbnailUrl', dom_object)
                            if result:
                                item_info['thumbnailUrl'] = result
                                # print(item_info)
                                count += 1
                                del list_items_failed[i]
                    else: # entire item failed
                        result = extract_data_from_category_dom_object(dom_object, category_id)
                        if result['success']:
                            # print(result['data'])
                            count += 1
                            del list_items_failed[i]

            list_items_failed = [] # Ignored items still failed after trying again twice.

    except TimeoutException:
        print("Loading took too much time!")

    print(f'Done crawling page #{page}. Total item: {count}') # page start from 1
    page += 1

    if page <= MAXIMUM_PAGE_NUMBER:
        next_page_button = driver.find_element_by_class_name('shopee-icon-button--right')
        driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
        ActionChains(driver).click(next_page_button).perform()
        last_page_item_number = len(items)
        # continue # this is unnecessary
    else:
        print(f'Done crawling category {category_id}, last page: {page - 1}') # start from 1
        break

driver.quit()


'''
id, name, sellerId, categoryId, rating, thumbnailUrl, 
totalReview, expired, productUrl, currentPrice,
platform, "shopee", update, lastPriceChange
'''
