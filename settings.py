#region Firefox Profile
from selenium import webdriver
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.set_preference("network.http.pipelining", True)
firefox_profile.set_preference("network.http.proxy.pipelining", True)
firefox_profile.set_preference("network.http.pipelining.maxrequests", 8)
firefox_profile.set_preference("content.notify.interval", 500000)
firefox_profile.set_preference("content.notify.ontimer", True)
firefox_profile.set_preference("content.switch.threshold", 250000)
firefox_profile.set_preference("browser.cache.memory.capacity", 65536) # Increase the cache capacity.
firefox_profile.set_preference("browser.startup.homepage", "about:blank")
firefox_profile.set_preference("reader.parse-on-load.enabled", False) # Disable reader, we won't need that.
firefox_profile.set_preference("browser.pocket.enabled", False) # Duck pocket too!
firefox_profile.set_preference("loop.enabled", False)
firefox_profile.set_preference("browser.chrome.toolbar_style", 1) # Text on Toolbar instead of icons
firefox_profile.set_preference("browser.display.show_image_placeholders", False) # Don't show thumbnails on not loaded images.
firefox_profile.set_preference("browser.display.use_document_colors", False) # Don't show document colors.
firefox_profile.set_preference("browser.display.use_document_fonts", 0) # Don't load document fonts.
firefox_profile.set_preference("browser.display.use_system_colors", True) # Use system colors.
firefox_profile.set_preference("browser.formfill.enable", False) # Autofill on forms disabled.
firefox_profile.set_preference("browser.helperApps.deleteTempFileOnExit", True) # Delete temprorary files.
firefox_profile.set_preference("browser.shell.checkDefaultBrowser", False)
firefox_profile.set_preference("browser.startup.homepage", "about:blank")
firefox_profile.set_preference("browser.startup.page", 0) # blank
firefox_profile.set_preference("browser.tabs.forceHide", True) # Disable tabs, We won't need that.
firefox_profile.set_preference("browser.urlbar.autoFill", False) # Disable autofill on URL bar.
firefox_profile.set_preference("browser.urlbar.autocomplete.enabled", False) # Disable autocomplete on URL bar.
firefox_profile.set_preference("browser.urlbar.showPopup", False) # Disable list of URLs when typing on URL bar.
firefox_profile.set_preference("browser.urlbar.showSearch", False) # Disable search bar.
firefox_profile.set_preference("extensions.checkCompatibility", False) # Addon update disabled
firefox_profile.set_preference("extensions.checkUpdateSecurity", False)
firefox_profile.set_preference("extensions.update.autoUpdateEnabled", False)
firefox_profile.set_preference("extensions.update.enabled", False)
firefox_profile.set_preference("general.startup.browser", False)
firefox_profile.set_preference("plugin.default_plugin_disabled", False)
# firefox_profile.set_preference("permissions.default.image", 2) # Image load disabled again <== this cause img src of item not shown
#endregion

# Global variable
CRAWLER_ID = '00'
SHOPEE = 'shopee'
REDIS_TRACKED_ITEMS_HASH_NAME = 'trackedItems-shopee'
RECEIVE_NOTIFICATION_SERVICE_ADDRESS = 'http://10.255.255.8:5050/notify-for-item' # param: itemId=...., newPrice=..., platform=...
A_DAY_IN_MS = 86400000 # = 24hrs
REDIS_REPRESENTATIVE_TRUE_VALUE = 1
HEADLESS = True
FIREFOX_PROFILE = firefox_profile
MAX_THREAD_NUMBER_FOR_ITEM = 2
MAX_THREAD_NUMBER_FOR_CATEGORY = 5

# After receiving crawling message
ALLOWED_CATEGORIES_TO_CRAWL = {
    84: 'Điện thoại và phụ kiện'
}
WILL_CRAWL_ALL_CATEGORIES = False
SHOPEE_URL = 'https://shopee.vn'

# Settings for crawler
TIME_BETWEEN_CRAWLING_IN_HOUR = 8

WAIT_TIME_LOAD_PAGE = 3 # seconds
NUMBER_PARTS_PAGE_HEIGHT = 7 # Assuming an page have this number of part corresponding to its height 

# configs about crawling items by category
CLASS_NAME_CARD_ITEM = '.shopee-search-item-result__item' # card component contains all item's info
CLASS_NAME_NAME_ITEM = '._36CEnF'
CLASS_NAME_PRICE = '._29R_un' # string 5.800.000 
CLASS_NAME_ROW_STARS = '.shopee-rating-stars__stars'
CLASS_NAME_STAR = '.shopee-rating-stars__lit'
CLASS_NAME_SOLD_NUMBER = '.go5yPW'
CLASS_NAME_BUTTON_NEXT = '.shopee-icon-button--right'
MAXIMUM_PAGE_NUMBER = 100
LOAD_ITEM_SLEEP_TIME = 0.3 # second

# configs about crawling item by item detail
CLASS_NAME_ITEM_BRIEF = 'product-briefing'
CLASS_NAME_ITEM_PRICE = '._3e_UQT'
CLASS_NAME_ITEM_NAME = '.attM6y span'
CLASS_NAME_ITEM_RATING = '._1mYa1t'
CLASS_NAME_ITEM_TOTAL_REVIEW = '.OitLRu'
CLASS_NAME_ITEM_IMAGE = '._2GchKS'
CLASS_NAME_ITEM_CATEGORY_ID = '._3YDLCj'