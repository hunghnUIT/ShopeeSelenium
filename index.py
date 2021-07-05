import os, sys, threading
from settings import MAX_THREAD_NUMBER_FOR_ITEM, MAX_THREAD_NUMBER_FOR_CATEGORY
from queue import Queue

from fastapi import FastAPI
from models.request_body import UrlRequestBody, ListUrlRequestBody

from controllers.crawler import crawl_with_item_urls, crawl_with_category_url, crawl_all_items, renew_ignored_items

sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

THREAD_COUNT_AT_START = threading.active_count()

jobs_category = Queue()
jobs_item = Queue()

app = FastAPI()

@app.get("/")
async def hello():
    return 'Hello from Shopee Selenium'

@app.post('/crawl-item')
async def crawl_each_item(body: ListUrlRequestBody) -> None:
    if threading.active_count() - THREAD_COUNT_AT_START < MAX_THREAD_NUMBER_FOR_ITEM:
        t = threading.Thread(target=crawl_with_item_urls, args=[body.urls, jobs_item])
        t.start()
    else:
        jobs_item.put(body.urls)
    return 'processing...'


@app.post('/crawl-category')
async def crawl_category(body: UrlRequestBody) -> None:
    if threading.active_count() - THREAD_COUNT_AT_START < MAX_THREAD_NUMBER_FOR_CATEGORY:
        t = threading.Thread(target=crawl_with_category_url, args=[body.url, jobs_category])
        t.start()
    else:
        jobs_category.put(body.url)
    return 'processing...'

@app.post('/crawl-all-items')
def get_all_categories(start_index: int= 0):
    crawl_all_items(start_index, jobs_category, THREAD_COUNT_AT_START)
    return 'processing...'

@app.post('/renew-ignored-items')
def renew_items():
    renew_ignored_items(jobs_item, THREAD_COUNT_AT_START)
    return 'processing...'

@app.get('/check')
def get_test():
    return 'ok'