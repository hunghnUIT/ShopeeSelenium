# Shopee Selenium Crawler

### What will this crawler do?
1. This is a **back-up crawler**, which means this crawler is not crawling every day using cron jobs like other crawlers, **just waiting for signals from the main crawlers**.
2. Receiving signals from the main crawlers, this crawler will crawling items with **URL of category** or with **URLs of items** or do them **both**.
3. This crawler is using **thread** to speed up crawler's speed and **queue** for queueing crawling tasks.
4. Updating...

### Technologies used:
* Selenium
* FastAPI
* Firefox
* MongoDB
* Multi threading and Queue

### Note: 
0. Current thread allow to use for crawling is **5 threads** when crawling with **category's URL** and **2 threads** when crawling with **item's URL**.
1. This crawler using the same approaching in processing and saving items with the main crawler.

***
*This crawler is a part of my thesis.*

**Author: Hoàng Ngọc Hùng - VNU HCMC- UIT**