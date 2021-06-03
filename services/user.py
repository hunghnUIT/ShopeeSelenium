from settings import RECEIVE_NOTIFICATION_SERVICE_ADDRESS


async def notify_web_service_about_decreased_price(item_id: int, new_price: int, is_trying_again: bool = False):
    url = f'{RECEIVE_NOTIFICATION_SERVICE_ADDRESS}?item_id=${item_id}&new_price=${new_price}&platform=shopee'
    response = {}

    if response and response['status'] == 200:
        print('Notified web service about decreased price')
    elif (not response and not is_trying_again) or (response['status'] != 200 and not is_trying_again):
        await notify_web_service_about_decreased_price(item_id, True)
    elif (not response and is_trying_again) or (response['status'] != 200 and is_trying_again):
        print('Notify to web service failed')
