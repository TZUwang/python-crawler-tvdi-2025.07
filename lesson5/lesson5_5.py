import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode 
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy #JsonCssExtractionStrategy功能為提取網頁內容並轉為JSON格式

async def main():
    raw_html = """<html> 
    <head> 
        <title>測試網頁</title> 
    </head>
    <body>
        <div class='item'> # 定義一個class為item的div
            <h2>項目1</h2> 
            <a href='https://example.com/item1'>連結1</a> #atribute 功能為提取連結
        </div>
    </body>
    </html>"""

    schema = { # 定義提取的JSON結構
        "name":"範例項目",
        "baseSelector":"div.item", 
        "fields":[ # 定義提取的欄位
            {
                "name":"產品", 
                "selector":"h2", 
                "type":"text" 
            },
            {
                "name":"連結", 
                "selector":"a", 
                "type":"attribute", 
                "attribute":"href" 
            }
        ]
    }

    #CrawlerRunConfig實體
    run_config = CrawlerRunConfig( # 設定爬蟲運行配置
        cache_mode = CacheMode.BYPASS, #CacheMode.BYPASS功能為不使用緩存
        extraction_strategy=JsonCssExtractionStrategy(schema=schema) # 提取策略使用JsonCssExtractionStrategy，並傳入schema
    )

#建立一個AsyncWebCrawler的實體
    async with AsyncWebCrawler() as crawler: 
        #Run the crawler on a URL
        result = await crawler.arun( # 使用arun方法運行爬蟲
            url=f"raw://{raw_html}", #raw://功能為提取原始HTML內容
            config=run_config 
        )
        print(type(result.extracted_content)) 
        print(result.extracted_content) 
        

if __name__ == "__main__":
    asyncio.run(main())