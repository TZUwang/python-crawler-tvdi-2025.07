import asyncio
from crawl4ai import AsyncWebCrawler,CrawlerRunConfig,CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def main():
    raw_html = """<html>
      <body> 
        <div class='crypto-row'>
          <h2 class='coin-name'>Bitcoin</h2>
          <span class='coin-price'>$28,000</span>
        </div> 
        <div class='crypto-row'>
          <h2 class='coin-name'>Ethereum</h2>
          <span class='coin-price'>$1,800</span>
        </div> 
        <div class='crypto-row'>
          <h2 class='coin-name'>Tether</h2>
          <span class='coin-price'>$1</span>
      </body> 
    </html>"""

    schema = {
        "name":"範例項目",
        "baseSelector":"div.crypto-row", #功能為每個加密貨幣項目的CSS選擇器(CSS選擇器是用來選擇HTML元素的模式)
        "fields":[ 
            {
                "name":"幣名",
                "selector":"h2.coin-name", 
                "type":"text"
            },
            {
                "name":"價格",
                "selector":"span.coin-price", 
                "type":"text"
            }
        ]
    }

     #CrawlerRunConfig實體 
    run_config = CrawlerRunConfig( 
        cache_mode = CacheMode.BYPASS, 
        extraction_strategy=JsonCssExtractionStrategy(schema=schema) #schema=schema 前者是CrawlerRunConfig的參數名稱，後者是我們定義的schema
    )

    #建立一個AsyncWebCrawler的實體
    async with AsyncWebCrawler() as crawler:
        #Run the crawler on a URL
        result = await crawler.arun(
            url=f"raw://{raw_html}",
            config=run_config
        )
        print(type(result.extracted_content)) 
        print(result.extracted_content)
        

if __name__ == "__main__":
    asyncio.run(main())