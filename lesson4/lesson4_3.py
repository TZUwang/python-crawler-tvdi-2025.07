#非同步_多任務執行 等待的期間會去執行其他任務

import asyncio # asyncio是Python的非同步IO庫
import time 

async def task(id, delay):
    print(f"開始任務 {id}")
    await asyncio.sleep(delay)
    print(f"任務 {id} 完成")

async def main(): 
    start = time.time()
    # 使用 asyncio 來執行非同步任務
    # 解釋為何還是執行花費3秒
    # 因為這裡的任務是串行執行的，
    # 每個任務都需要等待前一個任務完成
    # 如果要實現真正的非同步，應該使用 asyncio.gather
    # 或 asyncio.create_task 來並行執行任務
    # 這樣可以讓多個任務同時進行，節省時間
    tasks = [task(1,1), task(2, 2), task(3, 3), task(4, 4), task(5, 5)] 
    await asyncio.gather(*tasks) #*tasks會將列表中的任務展開為多個參數傳遞給asyncio.gather
    print(f"總耗時: {time.time() - start:.2f} 秒") 

asyncio.run(main()) # asyncio.run() 用來執行非同步函數

#舉例
#async def main: 是一本食譜。
#main(): 是你按照食譜準備好、待下鍋的菜餚（協程物件）。
#asyncio.run(): 是一座烤箱。
#你必須把準備好的菜餚 main() 放進烤箱 asyncio.run() 裡烘烤。你不能把整本食譜 main 丟進烤箱裡，它會不知道怎麼處理。