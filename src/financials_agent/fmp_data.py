try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

import certifi
import json
import os
import ssl
from dotenv import load_dotenv

load_dotenv()

def get_jsonparsed_data(url):
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    print(data)
    return json.loads(data)


url = (f"https://financialmodelingprep.com/stable/balance-sheet-statement?symbol=AAPL&apikey={os.getenv('fmp_key')}")
print(get_jsonparsed_data(url))