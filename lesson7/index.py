#建立一個tkinter的基本樣板
#請使用物件導向的方式來建立一個簡單的GUI應用程式
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from datetime import datetime
import threading
import asyncio
import wantgoo

try:
    import wantgoo
except ImportError:
    raise ImportError("請確保已安裝 wantgoo 模組，或將 wantgoo.py 放在相同目錄下。")

class SimpleApp:
    def __init__(self, root):
        self.root = root
        try:
            self.stock_codes: list[dict] = wantgoo.get_stocks_with_twstock()
            if not isinstance(self.stock_codes, list):
                raise ValueError("wantgoo.get_stocks_with_twstock() 應回傳一個股票字典的 list。")
        except Exception as e:
            self.stock_codes = []
            print(f"取得股票資料時發生錯誤: {e}")


        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.root, text="即時股票資訊", font=("Arial", 20, "bold"))
        self.label.pack(pady=20)        
        
        # 建立root_left_frame來包含左側的內容 
        root_left_frame = tk.Frame(self.root)
        root_left_frame.pack(side=tk.LEFT, pady=10, padx=10, fill=tk.BOTH, expand=True)

        # 建立左側的標題
        # left_title的文字靠左        
        left_title = tk.Label(root_left_frame, text="請選擇股票(可多選)", font=("Arial"), anchor="w", justify="left")
        left_title.pack(pady=(10,0), fill=tk.X,padx=10)

        # 建立leftFrame來包含 listbox 和 scrollbar
        left_frame = tk.Frame(root_left_frame)
        left_frame.pack(pady=10, padx=10,fill=tk.BOTH, expand=True)

        

        # 增加left_frame內的內容
        self.scrollbar = tk.Scrollbar(left_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.stock_listbox = tk.Listbox(left_frame,
                                        selectmode=tk.MULTIPLE,
                                        yscrollcommand=self.scrollbar.set,
                                        width=15,
                                        height=20)
        #抓取stock_listbox的選取事件
        self.stock_listbox.bind('<<ListboxSelect>>', self.on_stock_select) # 在選取股票時會及時更新右側顯示的資訊
        
        # 手動插入股票資料
        for stock in self.stock_codes:
            self.stock_listbox.insert(tk.END, f"{stock['code']} - {stock['name']}")
            
        self.stock_listbox.pack(side=tk.LEFT)
        self.scrollbar.config(command=self.stock_listbox.yview)

        
        # cancel_button,改變寬度和高度
        cancel_button = tk.Button(root_left_frame, text="取消", command=self.clear_selection)
        cancel_button.pack(side=tk.BOTTOM, pady=(0,10), fill=tk.X, expand=True)

        # 建立root_right_frame來包含選取股票的資訊
        root_right_frame = tk.Frame(self.root)
        root_right_frame.pack(side=tk.RIGHT, pady=10,padx=10,fill=tk.BOTH, expand=True)

        # 在右側顯示選取的股票資訊
        #增加self.selected_button按鈕click功能
        self.selected_button = tk.Button(root_right_frame,
                                        text="選取的股票資訊",
                                        font=("Arial", 12, "bold"),
                                        state=tk.DISABLED) #state=tk.DISABLED表示初始時按鈕為不可用狀態
        self.selected_button.pack(pady=10, padx=10, fill=tk.X)
        self.selected_button.bind("<Button-1>", self.start_crawling) #增加按鈕點擊事件

        # 新增一個 ScrolledText 用於顯示結果
        result_label = tk.Label(root_right_frame, text="爬取結果:", font=("Arial", 10), anchor="w")
        result_label.pack(padx=10, fill=tk.X)

        self.result_text = scrolledtext.ScrolledText(root_right_frame, wrap=tk.WORD, height=20, font=("Arial", 10))
        self.result_text.pack(pady=(0, 10), padx=10, fill=tk.BOTH, expand=True)
        self.result_text.insert(tk.END, "點擊按鈕開始爬取，結果將會顯示在這裡...")
        self.result_text.config(state=tk.DISABLED)

    def on_stock_select(self, _=None):
        """當股票被選取時，更新右側顯示的資訊"""
        self.selected_stocks = [self.stock_listbox.get(i) for i in self.stock_listbox.curselection()]
        self.selected_button.config(text=f"待爬取的股票數量:{len(self.selected_stocks)}筆")
        if len(self.selected_stocks) == 0:
            self.selected_button.config(state=tk.DISABLED)
        else:
            self.selected_button.config(state=tk.NORMAL)

    def clear_selection(self):
        """清除選取的股票資訊"""
        self.stock_listbox.selection_clear(0, tk.END)
        self.on_stock_select() #表示清除選取後，右側標籤也一併更新

    def start_crawling(self, _=None):
        """開始爬蟲"""
        if not self.selected_stocks:
            messagebox.showwarning("警告", "請先選擇股票！")
            return
        
        # 停用按鈕，防止重複點擊
        self.selected_button.config(state=tk.DISABLED, text="正在爬取中...")

        # 將耗時的爬蟲任務放到一個新的執行緒中，避免GUI凍結
        threading.Thread(target=self._crawl_in_thread, daemon=True).start()

    def _crawl_in_thread(self):
        """在背景執行緒中執行爬蟲"""
        urls:list[str] = []
        for info in self.selected_stocks:
            code, name = info.split(' - ')
            url_template = f'https://www.wantgoo.com/stock/{code}/technical-chart'
            urls.append(url_template)
        
        try:
            result:list[dict] = asyncio.run(wantgoo.get_stock_data(urls))
            # 當爬蟲完成後，使用 root.after 將結果傳回主執行緒來更新UI或顯示
            self.root.after(0, self.on_crawling_complete, result)
        except Exception as e:
            self.root.after(0, self.on_crawling_error, e)

    def on_crawling_complete(self, result: list[dict]):
        """爬蟲成功完成後的回呼函式"""
        # 移除彈出式提示
        # messagebox.showinfo("完成", f"成功爬取 {len(result)} 筆資料！")
        print(f"爬取股票資料結果: {result}")

        # 在 ScrolledText 中顯示結果
        self.result_text.config(state=tk.NORMAL) # 啟用編輯
        self.result_text.delete(1.0, tk.END) # 清除先前內容

        if not result:
            self.result_text.insert(tk.END, "沒有爬取到任何資料。\n")
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.result_text.insert(tk.END, f"爬取時間: {current_time}\n")
            self.result_text.insert(tk.END, f"爬取數量: {len(result)} 支股票\n")
            self.result_text.insert(tk.END, "="*50 + "\n\n")

            for stock_data in result:
                self.result_text.insert(tk.END, f"【 {stock_data.get('股票號碼', '')} {stock_data.get('股票名稱', '')} 】\n")
                for key, value in stock_data.items():
                    self.result_text.insert(tk.END, f"  {key}: {value}\n")
                self.result_text.insert(tk.END, "-"*40 + "\n\n")
        
        self.result_text.config(state=tk.DISABLED) # 禁用編輯
        self.on_stock_select() # 重設按鈕狀態
    
    def on_crawling_error(self, error: Exception):
        """爬蟲失敗後的回呼函式"""
        messagebox.showerror("錯誤", f"爬取時發生錯誤: {error}")
        self.on_stock_select() # 重設按鈕狀態

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleApp(root)
    root.mainloop()