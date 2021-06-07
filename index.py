import os
import sys
import time

from fastapi import FastAPI
from models.request_body import UrlRequestBody, ListUrlRequestBody

from controllers.crawler import crawl_with_item_urls, crawl_with_category_url
from config.db import col_item

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))


app = FastAPI()

@app.get("/")
async def hello():
    return 'Hello from Shopee Selenium'

@app.post('/crawl-item')
async def crawl_each_item(body: ListUrlRequestBody) -> None:
    start = time.perf_counter()
    crawl_with_item_urls(body.urls)
    print(f'Time: {time.perf_counter() - start} second(s)')
    return 'processing...'


@app.post('/crawl-category')
async def crawl_category(body: UrlRequestBody) -> None:
    crawl_with_category_url(body.url)
    return 'processing...'

@app.get('/1')
def get_test():
    col_item.insert_one({'id': 1234, 'name': 'testing', 'update': 122222})
    return 'ok'

# crawl_with_item_urls(['https://shopee.vn/-M%C3%A3-ELFLASH5-gi%E1%BA%A3m-20K-%C4%91%C6%A1n-50K-S%E1%BA%A1c-D%E1%BB%B1-Ph%C3%B2ng-Romoss-Sense-4-10000mah-Ch%C3%ADnh-H%C3%A3ng-Check-Code-BH-1-n%C4%83m-i.8563637.225188954'])