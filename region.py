import time
from PIL import Image
import pyautogui

from capture import select_window
from tesseract import text_extraction
from translation import en_translation

def main():
    print("캡처할 영역을 마우스로 지정하세요.")
    region = select_window.capture_selected_area()  # 사용자가 영역을 지정하도록 함

    prev_translated_text = ""
    try:
        while True:
            screenshot = pyautogui.screenshot(region=region)
            text = text_extraction.extract_text_from_image(screenshot)
            if text:
                translated_text = en_translation.translate_text(text)
                if translated_text != prev_translated_text:
                    print("번역된 텍스트:", translated_text)
                    prev_translated_text = translated_text
                else:
                    print("텍스트 변화 없음.")
            else:
                print("텍스트를 추출할 수 없습니다.")
            time.sleep(5)  # 5초 간격으로 반복
    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")

if __name__ == "__main__":
    main()