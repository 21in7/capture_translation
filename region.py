import time
from capture.select_window import capture_selected_area, capture_fixed_area
from tesseract.text_extraction import extract_text_from_image
from translation.en_translation import translate_text


def main():
    print("캡처할 영역을 마우스로 지정하세요.")
    screenshot, region = capture_selected_area()

    fixed_region = region

    prev_translated_text = ""
    try:
        while True:
            screenshot = capture_fixed_area(fixed_region)
            text = extract_text_from_image(screenshot)
            if text:
                translated_text = translate_text(text)
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