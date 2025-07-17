#若在ipynb無法運作 可能是jupyterNB的問題 可在py檔再次檢測是否安裝完成
#import crawl4ai
#print(crawl4ai.__version__.__version__)

from playwright.async_api import async_playwright
import asyncio

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://example.com')
        await page.wait_for_selector('p') #等待元素載入
        content = await page.inner_text('p')
        print(content)
        await browser.close()
    
asyncio.run(main())