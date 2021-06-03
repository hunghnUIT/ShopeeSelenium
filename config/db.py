import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://localhost:27017")
db_shopee = client['SHOPEE']
col_item = db_shopee['ItemsShopee']
col_item_price = db_shopee['ItemPriceShopee']

