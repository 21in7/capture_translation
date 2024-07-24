import tkinter as tk

class TranslatedTextOverlay:
    def __init__(self, root, on_retry):
        self.root = root
        self.on_retry = on_retry
        self.setup_gui()
        self.dragging = False

    def setup_gui(self):
        self.root.overrideredirect(True)  # 타이틀 바와 테두리 제거
        self.root.attributes('-topmost', True)  # 항상 최상위에 위치
        self.root.attributes('-alpha', 0.5)  # 창의 투명도 설정 (0.0 완전 투명, 1.0 완전 불투명)

        # 화면 크기와 위치 설정
        self.window_width = 800
        self.window_height = 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.window_width) // 2
        y = (screen_height - self.window_height) // 2
        self.root.geometry(f'{self.window_width}x{self.window_height}+{x}+{y}')

        # 텍스트 라벨 추가
        self.label = tk.Label(self.root, text="", bg="black", fg="white", font=("Helvetica", 16), wraplength=self.window_width - 20)
        self.label.pack(expand=True, fill=tk.BOTH)

        # 창 이동을 위한 이벤트 바인딩
        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<ButtonRelease-1>', self.stop_drag)
        self.label.bind('<B1-Motion>', self.do_drag)

        # 종료 키 이벤트 바인딩
        self.root.bind('<Escape>', self.close)
        # 재번역 키 이베트 바인딩
        self.root.bind('r', self.retry_capture)

    def start_drag(self, event):
        self.dragging = True
        self.mouse_x = event.x
        self.mouse_y = event.y

    def stop_drag(self, event):
        self.dragging = False

    def do_drag(self, event):
        if self.dragging:
            delta_x = event.x - self.mouse_x
            delta_y = event.y - self.mouse_y
            x = self.root.winfo_x() + delta_x
            y = self.root.winfo_y() + delta_y
            self.root.geometry(f"+{x}+{y}")

    def update_text(self, text):
        self.label.config(text=text)

    def close(self, event=None):
        self.root.destroy()

    def retry_capture(self, event):
        self.on_retry()

def main():
    def on_retry():
        print("재번역을 시도합니다.")

    root = tk.Tk()
    app = TranslatedTextOverlay(root, on_retry)
    app.update_text("번역된 텍스트가 여기에 표시됩니다.")
    root.mainloop()

if __name__ == "__main__":
    main()