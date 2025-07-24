#主要執行檔

import asyncio 
import wantgoo #引入自訂的module

def main(): 
    urls = [
        "https://www.wantgoo.com/stock/2330/technical-chart",
        "https://www.wantgoo.com/stock/2317/technical-chart",
        "https://www.wantgoo.com/stock/2454/technical-chart",
        "https://www.wantgoo.com/stock/2303/technical-chart",
        "https://www.wantgoo.com/stock/2412/technical-chart",
        "https://www.wantgoo.com/stock/2884/technical-chart",
        "https://www.wantgoo.com/stock/2881/technical-chart",
        "https://www.wantgoo.com/stock/2308/technical-chart",
        "https://www.wantgoo.com/stock/2337/technical-chart",
        "https://www.wantgoo.com/stock/2882/technical-chart",
    ] 
    reuslts:list[dict] = asyncio.run(wantgoo.get_stock_data(urls=urls)) #使用自訂的wantgoo模組 wantgoo.get_stock_data(urls=urls)會回傳一個list，裡面是dict
    for stock in reuslts: #列印每一支股票的資訊
        print(stock)

if __name__ == "__main__": 
    main() 