import time
from typing import List

conventions = {
    "k": 1000,
    "m": 1000000,
}


def process_item_url(url: str) -> object:
    result = {}
    # Remove params
    if url.find('?') > -1:
        url = url[0:url.find('?')]
    #  E.g: https://shopee.vn/product/283338743/9918567180?smtt=0.174867900-1616510545.9 // Shop id first, then item id
    if 'shopee.vn/product/' in url:
        splitted_by_splash = url.split('/')

        result['itemId'] = int(splitted_by_splash[len(splitted_by_splash) - 1])
        result['sellerId'] = int(
            splitted_by_splash[len(splitted_by_splash) - 2])

    #  E.g: https://shopee.vn/bach-tuoc-cam-xuc-2-mat-cam-xuc-do-choi-bach-tuoc-co-the-dao-nguoc-tam-trang-bach-tuoc-sang-trong-i.283338743.9918567180 //id shop first, then id item
    else:
        splitted_by_dot = url.split('.')

        result['itemId'] = int(splitted_by_dot[len(splitted_by_dot) - 1])
        result['sellerId'] = int(splitted_by_dot[len(splitted_by_dot) - 2])

    return result


'''
**@return** int number which is current category id 
'''
def proccess_category_url(url: str) -> int:
    category_id = -1
    if url.find('?') > -1 and 'search' not in url:
        url = url[0:url.find('?')]
    if '-cat.' in url:
        category_id = int(url.split('.')[-1])
    elif 'subcategory=' in url:
        category_id = int(url.split('subcategory=')[-1])
    return category_id


def convert_string_to_int(string: str) -> int:
    string = string.replace('₫', '')
    number = 0
    if not string.isdigit():
        unit = ''
        if string[-1].isalpha():
            unit = string[-1]
            string = string.replace(unit, '')
        string = string.replace('.', '')
        string = string.replace(",", '.')
        if unit:
            number = float(string) * conventions[unit]
        else:
            number = string
    else:
        number = string
    if isinstance(number, str):
        number = number.strip()
    return int(number)


def calculate_rating(rates: list) -> float:
    rating = 0.0
    for rate in rates:
        star = rate.get_attribute('style')
        star = star.replace('width:', '')
        star = star.replace('%;', '')
        rating += round(float(star.strip())/100, 1)

    return rating


def get_current_time_in_ms() -> int:
    return round(time.time() * 1000)


def process_item_price(price: str) -> int:
    price = price.split('-')
    return convert_string_to_int(price[0])


def extract_background_image_url(dom_object: object) -> str:
    # background-image: url("https://cf.shopee.vn/file/ee5e00f2460509388cd01a23fa8115bf"); background-size: contain; background-repeat: no-repeat;
    string = dom_object.get_attribute('style')
    start = string.find('url("') + 5 # 5 characters in url("
    end = string.find('")')
    return string[start: end]

def map_extract_image_url(arr:List[object]) -> List[str]:
    res = []
    for el in arr:
        res.append(extract_background_image_url(el))
    return res