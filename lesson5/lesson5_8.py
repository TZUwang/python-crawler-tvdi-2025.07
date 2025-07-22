import asyncio
from crawl4ai import AsyncWebCrawler,CrawlerRunConfig,CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
import json

def process_data(datas): #處理下面抓取到的資料
     for item in datas:  #for in迴圈抓取datas中的items
            print(item)

async def main():
    url = 'https://rate.bot.com.tw/xrt?Lang=zh-TW'

    schema = {
        "name":"台幣匯率",
        "baseSelector":"table[title='牌告匯率'] tr", #tr前空格很重要 選擇table中title為牌告匯率的tr元素 
        "fields":[
            {
                "name":"幣名",
                "selector":"td[data-table='幣別'] div.visible-phone.print_hide", #意思是選擇td元素中屬性data-table為幣別的div元素，並且提取這div元素中visible-phone print_hide這個class
                "type":"text"
            },
            {
                "name":"現金匯率_本行買入",
                "selector":'[data-table="本行現金買入"]',
                "type":"text"
            },
            {
                "name":"現金匯率_本行賣出",
                "selector":'[data-table="本行現金賣出"]',
                "type":"text"
            },
            {
                "name":"即期匯率_本行買入",
                "selector":'[data-table="本行即期買入"]',
                "type":"text"
            },
            {
                "name":"即期匯率_本行賣出",
                "selector":'[data-table="本行即期賣出"]',
                "type":"text"
            }
        ]
    }

    #CrawlerRunConfig實體
    run_config = CrawlerRunConfig(
        cache_mode = CacheMode.BYPASS,
        extraction_strategy=JsonCssExtractionStrategy(schema=schema)
    )

    #建立一個AsyncWebCrawler的實體
    async with AsyncWebCrawler() as crawler:
        #Run the crawler on a URL
        result = await crawler.arun(
            url=url,
            config=run_config
        )
        datas = json.loads(result.extracted_content) #將抓取到的資料轉換成Python的資料結構
        process_data(datas) #呼叫process_data函式來處理抓取到的資料
        

if __name__ == "__main__":
    asyncio.run(main())