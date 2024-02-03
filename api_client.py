import requests

def fetch_trades(symbol, start_time):
    # 示例API URL，需要替换为实际的API URL
    url = f"https://pro.apex.exchange/api/v2/trades?symbol={symbol}"
    response = requests.get(url)
    return response.json()
