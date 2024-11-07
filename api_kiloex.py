import requests
import logging
from functools import wraps
import time

def retry_conservative(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        index = 0
        while True:
            try:
                return fn(*args, **kwargs)
            except Exception:
                index = index + 1
                time.sleep(index)
                if index > 5:
                    raise
                logging.info(f"Retrying request: {index}")
                continue
    return wrapper

def apienv(chain):
    if chain == 'OPBNB':
        return 'op'
    return 'op'

@retry_conservative
def index_price(product_id, chain='OPBNB'):
    """Get current price for product ID"""
    apistr = f'https://{apienv(chain)}api.kiloex.io/index/prices'
    res = requests.get(apistr)
    data = res.json()
    result = float(data['current'][str(product_id)])
    return result

@retry_conservative
def index_symbols(chain='OPBNB'):
    """Get all trading symbols"""
    apistr = f'https://{apienv(chain)}api.kiloex.io/index/symbols'
    res = requests.get(apistr)
    return res.json()

@retry_conservative
def query_fundingList(chain):
    """Get funding rate list"""
    apistr = f'https://{apienv(chain)}api.kiloex.io/common/queryKiloCache'
    res = requests.get(apistr)
    return res.json()['kiloCache']['fundingBorrowList']

@retry_conservative
def query_productList(chain):
    """Get product list"""
    apistr = f'https://{apienv(chain)}api.kiloex.io/common/queryProducts'
    res = requests.get(apistr)
    return res.json()['productList']