import time
import threading
import tkinter as tk
from capture.select_window import capture_selected_area, capture_fixed_area
from tesseract.text_extraction import extract_text_from_image
from translation.en_translation import translate_text
from gui.overlay import TranslatedTextOverlay

def background_task(overlay, fixed_region, stop_event):
    prev_translated_text = ""
    while not stop_event.is_set():
        screenshot = capture_fixed_area(fixed_region)
        text = extract_text_from_image(screenshot)
        if text:
            translated_text = translate_text(text)
            if translated_text != prev_translated_text:
                print("번역된 텍스트:", translated_text)
                # 메인 스레드에서 오버레이 창에 번역된 텍스트 업데이트
                overlay.update_text(translated_text)
                prev_translated_text = translated_text
            else:
                print("텍스트 변화 없음.")
        else:
            print("텍스트를 추출할 수 없습니다. 다시 캡처를 시도합니다.")
            time.sleep(1.5)
            continue
        time.sleep(1)  # 5초 간격으로 반복

def main():
    print("캡처할 영역을 마우스로 지정하세요.")
    screenshot, region = capture_selected_area()

    fixed_region = region
    stop_event = threading.Event()

    def on_retry():
        print("재번역을 시도합니다.")
        screenshot = capture_fixed_area(fixed_region)
        text = extract_text_from_image(screenshot)
        if text:
            translated_text = translate_text(text)
            print("재번역된 텍스트:", translated_text)
            overlay.update_text(translated_text)
        else:
            print("텍스트를 추출할 수 없습니다. 다시 캡처를 시도합니다.")

    root = tk.Tk()
    overlay = TranslatedTextOverlay(root, on_retry)
    
    # 백그라운드 작업을 위한 스레드 생성 및 시작
    background_thread = threading.Thread(target=background_task, args=(overlay, fixed_region, stop_event), daemon=True)
    background_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()