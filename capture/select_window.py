from pynput import mouse
import pyautogui

# 캡쳐할 영역의 시작점과 끝점을 저장할 전역 변수
start_point = None
end_point = None

def on_click(x, y, button, pressed):
    global start_point, end_point
    if pressed:
        start_point = (x, y)  # 마우스 버튼을 누른 위치
    else:
        end_point = (x, y)  # 마우스 버튼을 뗀 위치
        return False  # 리스너를 중지

def capture_selected_area():
    global start_point, end_point
    # 사용자로부터 캡쳐할 영역을 지정받음
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

    # 캡쳐할 영역의 좌표 계산
    x1, y1 = start_point
    x2, y2 = end_point
    region = (min(x1, x2), min(y1, y2), abs(x2-x1), abs(y2-y1))
    return region