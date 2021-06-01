from datetime import datetime
import math
from settings import TIME_BETWEEN_CRAWLING_IN_HOUR


def init_timing_value() -> object:
    now = datetime.now()
    crawl_time_in_day_count = math.floor(
        now.hour/TIME_BETWEEN_CRAWLING_IN_HOUR)
    start_time = now.replace(
        hour=(crawl_time_in_day_count*TIME_BETWEEN_CRAWLING_IN_HOUR), minute=0, second=0)

    global startTime
    startTime = int(start_time.timestamp()) * 1000  # timestamp to millisecond

    global expiredTime
    # Minus 1ms for felling guaranteed
    expiredTime = startTime + (TIME_BETWEEN_CRAWLING_IN_HOUR*60*60*1000) - 1

    start = now.replace(hour=0, minute=0, second=0)
    global startOfDay
    startOfDay = int(start.timestamp()) * 1000

    global endOfDay
    endOfDay = startOfDay + 86400000  # End=start+24hrs