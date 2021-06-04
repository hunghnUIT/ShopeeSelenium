from config.db import col_item, col_item_price
import timing_value
from settings import SHOPEE, REDIS_TRACKED_ITEMS_HASH_NAME, A_DAY_IN_MS
from services.user import notify_web_service_about_decreased_price
from config.redis import redis_client as redis


async def save_item(found_item, item) -> object:
    if found_item:
        updating_item = {}

        updating_item['lastPriceChange'] = int(
            item['price']) - found_item['currentPrice']
        updating_item['name'] = item['name']
        if item['categoryId']:
            updating_item['categoryId'] = item['categoryId']
        updating_item['productUrl'] = item['productUrl']
        updating_item['rating'] = item['rating']
        updating_item['totalReview'] = item['totalReview']
        updating_item['thumbnailUrl'] = item['thumbnailUrl']
        updating_item['expired'] = timing_value.expiredTime
        updating_item['currentPrice'] = item['price']
        updating_item['update'] = item['update']
        updating_item['platform'] = SHOPEE

        if 'images' in item:
            updating_item['images'] = item['images']

        col_item.update_one({'id': item['id']}, {'$set': updating_item})
    else:
        col_item.insert_one({
            'id': item['id'],
            'name': item['name'],
            'sellerId': item['sellerId'],
            'categoryId': item['categoryId'],
            'productUrl': item['productUrl'],
            'rating': item['rating'],
            'thumbnailUrl': item['thumbnailUrl'],
            'totalReview': item['totalReview'],
            'expired': timing_value.expiredTime,
            'currentPrice': item['price'],
            'lastPriceChange': 0,
            'update': item['update'],
            'platform': SHOPEE,
        })


async def save_item_price(item, is_flash_sale) -> None:
    found_item_price = await col_item_price.find_one({
        'itemId': item['id'],
        'update': {'$gte': timing_value.startOfDay, '$lte': timing_value.endOfDay}
    })

    if found_item_price:
        updating_item_price = {}
        updating_item_price['itemId'] = item['id']
        updating_item_price['price'] = item['price']
        updating_item_price['update'] = item['update']
        updating_item_price['priceChangeInDay'] = found_item_price['priceChangeInDay'] + [
            {'price': item['price'], 'update': item['update'], 'isFlashSale': is_flash_sale}]
        # updating_item_price['priceChangeInDay'].append(
        #     {'price': item['price'], 'update': item['update'], 'isFlashSale': is_flash_sale})

        col_item_price.update_one({'itemId': item['id']}, {
                                    '$set': updating_item_price})
    else:
        col_item_price.insert_one({
            'itemId': item['id'],
            'price': item['price'],
            'update': item['update'],
            'priceChangeInDay': [{'price': item['price'], 'update': item['update'], 'isFlashSale': is_flash_sale}]
        })


async def create_item_price_day_before(item) -> None:
    found_item_price = await col_item_price.find_one({
        'itemId': item['id'],
        'update': {'$gte': timing_value.startOfDay-A_DAY_IN_MS, '$lte': timing_value.endOfDay-A_DAY_IN_MS}
    })

    if not found_item_price:
        col_item_price.insert_one({
            'itemId': item['id'],
            # Not item['price'] because passed item is item in DB.
            'price': item['currentPrice'],
            'update': item['update'] - A_DAY_IN_MS,
            'priceChangeInDay': [{'price': item['currentPrice'], 'update': item['update'], 'isFlashSale': False}]
        })


async def save_item_to_db(item, is_flash_sale: bool = False) -> None:
    if (item['id'] and item['name'] and item['sellerId']
            and (item['rating'] or item['rating'] == 0)
            and (item['totalReview'] or item['totalReview'] == 0)):

        found_item = await col_item.find_one({'id': item['id']})
        await save_item(found_item, item)

        if (found_item and found_item['currentPrice'] != item['price']) or not found_item:
            await save_item_price(item, is_flash_sale)
            #  Price is decreased?
            if found_item and found_item['currentPrice'] > item['price']:
                #  Check if this item being tracked by any user.
                is_tracked = redis.hget(REDIS_TRACKED_ITEMS_HASH_NAME, item['id'])
                if is_tracked:
                    #  Notify to server
                    notify_web_service_about_decreased_price(item['id'], item['price'])

        # If price is changed, create a node price the day before the price is changed
        if found_item and found_item['currentPrice'] != item['price']:
            await create_item_price_day_before(found_item)
