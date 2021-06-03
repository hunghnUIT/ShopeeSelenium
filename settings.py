# Global variable
SHOPEE = 'shopee'
REDIS_TRACKED_ITEMS_HASH_NAME = 'trackedItems-shopee'
RECEIVE_NOTIFICATION_SERVICE_ADDRESS = 'http://10.255.255.8:5050/notify-for-item' # param: itemId=...., newPrice=..., platform=...
A_DAY_IN_MS = 86400000 # = 24hrs

# Settings for crawler
TIME_BETWEEN_CRAWLING_IN_HOUR = 8

WAIT_TIME_LOAD_PAGE = 3 # seconds
NUMBER_PARTS_PAGE_HEIGHT = 7 # Assuming an page have this number of part corresponding to its height 

# configs about crawling items by category
CLASS_NAME_CARD_ITEM = 'shopee-search-item-result__item' # card component contains all item's info
CLASS_NAME_NAME_ITEM = '_36CEnF'
CLASS_NAME_PRICE = '_29R_un' # string 5.800.000 
CLASS_NAME_ROW_STARS = 'shopee-rating-stars__stars'
CLASS_NAME_STAR = 'shopee-rating-stars__lit'
CLASS_NAME_SOLD_NUMBER = 'go5yPW'
CLASS_NAME_BUTTON_NEXT = 'shopee-icon-button--right'
MAXIMUM_PAGE_NUMBER = 100
LOAD_ITEM_SLEEP_TIME = 0.3 # second

# configs about crawling item by item detail
CLASS_NAME_ITEM_BRIEF = 'product-briefing'
CLASS_NAME_ITEM_PRICE = '_3e_UQT'
CLASS_NAME_ITEM_NAME = 'attM6y'
CLASS_NAME_ITEM_RATING = '_1mYa1t'
CLASS_NAME_ITEM_TOTAL_REVIEW = 'OitLRu'
CLASS_NAME_ITEM_IMAGE = '_2GchKS'
CLASS_NAME_ITEM_CATEGORY_ID = '_3YDLCj'