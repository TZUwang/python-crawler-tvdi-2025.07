import asyncio
from crawl4ai import AsyncWebCrawler

async def main():
    #建立一個AsyncWebCrawler的實體
    async with AsyncWebCrawler() as crawler:
        #Run the crawler on a URL
        result = await crawler.arun(url='https://moondroplab.com/cn/home')

        #列印取出的結果
        print(result.markdown) #使用markdown語法

if __name__ == "__main__": # __name__是Python的特殊變數，當這個檔案被直接執行時，它的值會是'__main__'
    asyncio.run(main()) 