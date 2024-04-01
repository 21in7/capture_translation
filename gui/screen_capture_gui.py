import tkinter as tk
import queue

class ScreenCaptureGUI:
    def __init__(self, gui_queue):
        self.gui_queue = gui_queue
        self.root = None
        self.canvas = None
        self.setup_gui()

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)  # 윈도우 투명도 설정
        self.root.attributes('-fullscreen', True)  # 전체 화면 모드
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.check_queue()

    def check_queue(self):
        try:
            while True:
                action, *args = self.gui_queue.get_nowait()
                if action == 'start':
                    self.canvas.delete("all")
                    self.canvas.create_rectangle(*args, outline='red', tag="rect")
                elif action == 'update':
                    self.canvas.coords("rect", *args)
                elif action == 'end':
                    self.root.destroy()
                    return # 애플리케이션이 종료되면 check_queue 메서드를 종료
                elif action == 'withdraw':
                    if self.root.winfo_exists():
                        self.root.withdraw()
                elif action == 'deiconify':
                    if self.root.winfo_exists():
                        self.root.deiconify()
        except queue.Empty:
            pass
        if self.root.winfo_exists():
            self.root.after(10, self.check_queue)

    def start(self):
        self.root.after(10, self.check_queue)
        self.root.mainloop()