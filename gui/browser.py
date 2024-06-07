import tkinter as tk

from typing import List

from url import URL
from browser_requests.request import request

# WIDTH, HEIGHT = 800, 600
HSTEP, VSTEP = 9, 18
SCROLL_STEP = 100

def layout(width: int, text: str) -> List[tuple]:
    display_list: List[tuple] = []
    cursor_x, cursor_y = HSTEP, VSTEP
    for c in text:
        display_list.append((cursor_x, cursor_y, c))
        cursor_x += HSTEP
        if c == "\n":
            cursor_y += VSTEP
            cursor_x = HSTEP
            continue
        if cursor_x >= width - HSTEP:
            cursor_y += VSTEP
            cursor_x = HSTEP
    return display_list

class Browser:
    def __init__(self) -> None:
        self.window = tk.Tk()
        
        self.width = self.window.winfo_width()
        self.height = self.window.winfo_height()
        
        
        self.canvas = tk.Canvas(
            self.window,
            width=self.width,
            height=self.height
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.scroll: int = 0
        
        self.window.bind("<Down>", self.scroll_down)
        self.window.bind("<Up>", self.scroll_up)
        self.window.bind("<MouseWheel>", self.on_mouse_wheel)
        self.window.bind("<Configure>", self.on_resize)
        
    def draw(self) -> None:
        self.canvas.delete("all")
        for x, y, c in self.display_list:
            if y > self.scroll + self.height: continue
            if y + VSTEP < self.scroll: continue
            self.canvas.create_text(x, y - self.scroll, text=c)
            
    def scroll_up(self, e):
        if self.scroll >= SCROLL_STEP:       
            self.scroll -= SCROLL_STEP
            self.draw()
    
    def scroll_down(self, e):
        max_scroll = max(y for _, y, _ in self.display_list) - self.height
        if self.scroll + SCROLL_STEP <= max_scroll:
            self.scroll += SCROLL_STEP
        else:
            self.scroll = max_scroll
        self.draw()
    
    def on_mouse_wheel(self, e):
        if e.delta > 0:
            self.scroll_up(e)
        else:
            self.scroll_down(e)
    
    def on_resize(self, e):
        self.width = e.width
        self.height = e.height
        self.canvas.config(width=self.width, height=self.height)

        self.display_list = layout(self.width, self.text)
        self.draw()
    
    def load(self, url: URL) -> None:
        self.text = request(url)
        
        self.display_list = layout(self.width, self.text)
        self.draw()