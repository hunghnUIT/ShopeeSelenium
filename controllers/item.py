from selenium.common.exceptions import NoSuchElementException
from config.redis import redis_client as redis
from config.db import col_tracked_item

# Settings
from settings import (
    CLASS_NAME_NAME_ITEM, CLASS_NAME_ROW_STARS,
    CLASS_NAME_STAR, CLASS_NAME_SOLD_NUMBER,
    CLASS_NAME_PRICE,
    CLASS_NAME_ITEM_NAME, CLASS_NAME_ITEM_RATING,
    CLASS_NAME_ITEM_PRICE, CLASS_NAME_ITEM_IMAGE,
    CLASS_NAME_ITEM_TOTAL_REVIEW, CLASS_NAME_ITEM_CATEGORY_ID, 
    REDIS_TRACKED_ITEMS_HASH_NAME, REDIS_REPRESENTATIVE_TRUE_VALUE,
)

# Functions
from helper import (
    process_item_url, calculate_rating,
    convert_string_to_int, get_current_time_in_ms,
    process_item_price, extract_background_image_url,
    map_extract_image_url, 
)

import timing_value


def extract_data_from_category_dom_object(dom_object: object, category_id: int) -> object:
    item = {}
    try:
        product_url = dom_object.find_element_by_tag_name(
            'a').get_attribute('href')
        info_from_url = process_item_url(product_url)
        stars = dom_object.find_elements_by_css_selector(
            f'{CLASS_NAME_ROW_STARS} {CLASS_NAME_STAR}')
        sold = dom_object.find_element_by_css_selector(
            CLASS_NAME_SOLD_NUMBER).text

        item['id'] = info_from_url['itemId']
        item['name'] = dom_object.find_element_by_css_selector(
            CLASS_NAME_NAME_ITEM).text
        item['sellerId'] = info_from_url['sellerId']
        item['categoryId'] = category_id
        item['productUrl'] = product_url
        item['rating'] = calculate_rating(stars) if stars else 0
        item['totalReview'] = convert_string_to_int(
            sold.split(" ")[-1]) if sold else 0
        item['update'] = get_current_time_in_ms()
        item['expired'] = timing_value.expiredTime
        item['price'] = convert_string_to_int(
            dom_object.find_element_by_css_selector(CLASS_NAME_PRICE).text)
        item['thumbnailUrl'] = dom_object.find_element_by_tag_name(
            'img').get_attribute('src')
        if not item['thumbnailUrl']:
            return {
                'success': False,
                'data': item,
            }
        else:
            return {
                'success': True,
                'data': item,
            }

    except NoSuchElementException:
        return {
            'success': False,
            'data': None,
        }

# These fields below is usually failed.
def extract_field_from_category_dom_object(key: str, dom_object: object) -> any:
    switcher = {
        'thumbnailUrl': dom_object.find_element_by_tag_name('img').get_attribute('src')
    }
    return switcher.get(key, None)


def extract_data_from_item_dom_object(dom_object: object, product_url: str):
    item = {}
    try:
        info_from_url = process_item_url(product_url)
        rating = dom_object.find_elements_by_css_selector(CLASS_NAME_ITEM_RATING)
        total_review = dom_object.find_elements_by_css_selector(
            CLASS_NAME_ITEM_TOTAL_REVIEW)
        item_price = dom_object.find_element_by_css_selector(
            CLASS_NAME_ITEM_PRICE).text
        images = dom_object.find_elements_by_css_selector(
            CLASS_NAME_ITEM_IMAGE)

        # Update 28/6/2021: Shopee remove category ID from item detail, can not find any way to get this so categoryId won't be update anymore with item detail
        # category_ids = dom_object.find_elements_by_css_selector(
            # CLASS_NAME_ITEM_CATEGORY_ID)
        # href = category_ids[len(category_ids) - 1].get_attribute('href') if category_ids[len(category_ids) - 1] else ''
        # splitted_href = href.split('.') if href else []
        # category_id = 0
        # if splitted_href:
            # category_id = splitted_href[len(splitted_href) - 1]

        item['id'] = info_from_url['itemId']
        item['name'] = dom_object.find_element_by_css_selector(
            CLASS_NAME_ITEM_NAME).text
        item['sellerId'] = info_from_url['sellerId']
        # item['categoryId'] = int(category_id)
        item['productUrl'] = product_url
        item['rating'] = float(rating[0].text) if rating else 0.0
        item['totalReview'] = convert_string_to_int(
            total_review[1].text) if total_review else 0
        item['update'] = get_current_time_in_ms()
        item['expired'] = timing_value.expiredTime
        item['price'] = process_item_price(item_price)
        if images:
            item['thumbnailUrl'] = extract_background_image_url(images[0])
            item['images'] = map_extract_image_url(images)
        else:
            print('Can not get images')

        return {
            'success': True,
            'data': item,
        }
    except NoSuchElementException as err:
        print(str(err))
        return {
            'success': False,
            'data': None,
        }
    except Exception as err:
        print(str(err))


def store_tracked_items_to_redis():
    # Delete the old one before update new.
    redis.delete(REDIS_TRACKED_ITEMS_HASH_NAME)

    limit = 2000
    skip = 0
    tracked_items = []
    while True:
        items = list(col_tracked_item.find().limit(limit).skip(skip))
        if items:
            tracked_items += items
            skip += limit
        else:
            break

    for el in tracked_items:
        redis.hset(REDIS_TRACKED_ITEMS_HASH_NAME, int(el['itemId']), REDIS_REPRESENTATIVE_TRUE_VALUE)