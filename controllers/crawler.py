from time import sleep
from typing import List
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Settings
from settings import (
    WAIT_TIME_LOAD_PAGE, NUMBER_PARTS_PAGE_HEIGHT, 
    CLASS_NAME_CARD_ITEM, MAXIMUM_PAGE_NUMBER, 
    LOAD_ITEM_SLEEP_TIME, CLASS_NAME_ITEM_PRICE,
    HEADLESS, FIREFOX_PROFILE
)

# Functions
from helper import ( 
    proccess_category_url,
)
from controllers.item import (
    extract_data_from_category_dom_object, extract_field_from_category_dom_object,
    extract_data_from_item_dom_object, store_tracked_items_to_redis
)
import timing_value
from services.item import save_item_to_db


'''
Function receive a category URL at a moment, start at page #1, then crawl to the last page and exit browser.
@route      {{BASE_URL}}/crawl-category?url=https://shopee.vn/category-cat.id...
@method     POST
@body       None
'''
def crawl_with_category_url(url:str):
    timing_value.init_timing_value()
    store_tracked_items_to_redis()

    # options = EdgeOptions()
    # options.use_chromium = True
    # options.add_argument("headless")
    # options.add_argument("disable-gpu")

    # driver = Edge(options=options)

    options = Options()
    if HEADLESS:
        options.headless = True
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')

    driver = webdriver.Firefox(options=options, firefox_profile=FIREFOX_PROFILE)

    # driver = webdriver.Edge() # Uncomment this to use none headless browser
    driver.get(url)

    category_id = proccess_category_url(url)

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
            actions = ActionChains(driver)
            for _ in range(8): # space 8 times = heigh of the document
                actions.send_keys(Keys.SPACE).perform()
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
                        save_item_to_db(result['data'])

            # Format "list_items_failed": [{idx: 1, item_info: {item}}, {idx: 6, item_info: {item}}]
            if list_items_failed:
                # try again twice
                for _ in range(2):
                    for i, item in enumerate(list_items_failed):
                        dom_object = items[item['idx']]
                        item_info = item['item_info']
                        if item_info: # A few fields failed
                            if item_info['thumbnailUrl'] == None:
                                result = extract_field_from_category_dom_object('thumbnailUrl', dom_object)
                                if result:
                                    item_info['thumbnailUrl'] = result
                                    # print(item_info)
                                    save_item_to_db(item_info)
                                    count += 1
                                    del list_items_failed[i]
                        else: # entire item failed
                            result = extract_data_from_category_dom_object(dom_object, category_id)
                            if result['success']:
                                # print(result['data'])
                                save_item_to_db(result['data'])
                                count += 1
                                del list_items_failed[i]

                list_items_failed = [] # Ignored items still failed after trying again twice.

        except TimeoutException:
            print("Loading took too much time!")
            items = []

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
Function receive a item URLs, crawl items one by one and quit browser.
@route      {{BASE_URL}}/crawl-item
@method     POST
@body       { urls: list[str] }
'''
def crawl_with_item_urls(urls:List[str]):
    timing_value.init_timing_value()
    store_tracked_items_to_redis()

    options = Options()
    if HEADLESS:
        options.headless = True

    driver = webdriver.Firefox(options=options, firefox_profile=FIREFOX_PROFILE)
    for url in urls:
        try:
            driver.get(url)

            myElem = WebDriverWait(driver, WAIT_TIME_LOAD_PAGE).until(
                EC.presence_of_element_located((By.CLASS_NAME, CLASS_NAME_ITEM_PRICE)))

            # # Scroll to deal with lazy load.
            # page_height = driver.execute_script("return document.body.scrollHeight")
            # each_part_height = page_height//NUMBER_PARTS_PAGE_HEIGHT
            # for part in range(1, NUMBER_PARTS_PAGE_HEIGHT-2): # Many the first parts, the end parts include no item
            #     y = part * each_part_height
            #     driver.execute_script(f'window.scrollTo(0, {y});')
            # sleep(LOAD_ITEM_SLEEP_TIME)

            result = extract_data_from_item_dom_object(driver, url)
            if result['success']:
                # print(result['data'])
                print('ok')
                save_item_to_db(result['data'])
            else:
                print('error')
        except TimeoutException:
            print("Loading took too much time!")
        except Exception as err:
            print(str(err))

    driver.quit()