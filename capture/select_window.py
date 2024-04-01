from pynput import mouse
import threading
import queue
import pyautogui
import time
from gui.screen_capture_gui import ScreenCaptureGUI  # GUI 모듈 임포트

# 캡처할 영역의 시작점과 끝점을 저장할 전역 변수
start_point = None
end_point = None

# GUI 업데이트를 위한 큐
gui_queue = queue.Queue()

def on_click(x, y, button, pressed):
    global start_point, end_point
    if pressed:
        start_point = (x, y)
        gui_queue.put(('start', x, y, x, y))
    else:
        end_point = (x, y)
        gui_queue.put(('end', x, y))
        return False

def on_move(x, y):
    if start_point is not None:
        gui_queue.put(('update', start_point[0], start_point[1], x, y))

def capture_selected_area():
    global start_point, end_point, region
    # 마우스 리스너를 별도의 스레드에서 실행
    listener_thread = threading.Thread(target=lambda: mouse.Listener(on_click=on_click, on_move=on_move).start())
    listener_thread.start()

    # GUI 시작
    app = ScreenCaptureGUI(gui_queue)
    app.start()  # 이 호출은 메인 스레드에서 실행되어야 합니다.

    listener_thread.join()  # 마우스 리스너 스레드가 종료될 때까지 기다립니다.




    # 캡처할 영역의 좌표 계산
    x1, y1 = start_point
    x2, y2 = end_point
    region = (min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))

    # 캡처 직전에 윈도우를 숨김
    gui_queue.put(('withdraw',))
    time.sleep(0.1)  # GUI 업데이트를 위한 충분한 시간 제공

    # 지정된 영역 캡처
    screenshot = pyautogui.screenshot(region=region)

    # 캡처 후에 윈도우를 다시 표시
    gui_queue.put(('deiconify',))
    time.sleep(0.1)  # GUI 업데이트를 위한 충분한 시간 제공

    # 캡처한 이미지 저장
    screenshot.save("captured_image.png")  

    return screenshot, region

def capture_fixed_area(region):
    screenshot = pyautogui.screenshot(region=region)

    screenshot.save("captured_image_fixed.png")

    return screenshot

if __name__ == "__main__":
    capture_selected_area()