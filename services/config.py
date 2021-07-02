from config.db import col_config
from settings import CRAWLER_NAME

AFFECT_PRIORITY = [CRAWLER_NAME, 'shopee_html_crawler', 'all_html_crawler']

def get_config_by_name_and_affect(name: str, affect: str):
    query = { 'name': name, 'affect': affect}

    config = col_config.find_one(query)

    return None if config is None else config['value']

def get_config(name: str, default_value: str):
    for affect in AFFECT_PRIORITY:
        res = get_config_by_name_and_affect(name, affect)
        if (res != None):
            return res
    return default_value
