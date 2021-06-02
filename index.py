import os
import sys
from controllers.crawler import crawl_with_item_urls

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


crawl_with_item_urls([
    'https://shopee.vn/%C4%90%E1%BA%BF-tr%C6%B0ng-b%C3%A0y-%C4%91i%E1%BB%87n-tho%E1%BA%A1i-logo-iphone-samsung-opp-vivo-i.150020932.5012866193',
    'https://shopee.vn/Gi%C3%A1-%C4%90%E1%BB%A1-%C4%90i%E1%BB%87n-Tho%E1%BA%A1i-K%E1%BA%B9p-C%E1%BB%ADa-Gi%C3%B3-%C4%90i%E1%BB%81u-H%C3%B2a-%C3%94-T%C3%B4-Xe-H%C6%A1i-SENDEM-W6-W8-i.283889877.8156550588',
    ])
