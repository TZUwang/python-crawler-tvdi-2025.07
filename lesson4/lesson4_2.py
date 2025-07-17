#同步_執行完一個動作才會執行下一個

import time

def task(id, delay):
    print(f"開始任務 {id}")
    time.sleep(delay)
    print(f"任務 {id} 完成")

start = time.time()
task(1, 1)
task(2, 2)
task(3, 3)
task(4, 4)
task(5, 5)
print(f"總耗時: {time.time() - start:.2f} 秒") 