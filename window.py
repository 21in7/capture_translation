import time
from capture import window_capture
from tesseract import text_extraction
from translation import en_translation

def main():
    window_title = input("번역할 창의 제목을 입력하세요: ")
    prev_translated_text = ""
    try:
        while True:
            image = window_capture.capture_window(window_title)
            if image:
                text = text_extraction.extract_text_from_image(image)
                if text:
                    translated_text = en_translation.translate_text(text)
                    if translated_text != prev_translated_text:
                        print("번역된 텍스트:", translated_text)
                        prev_translated_text = translated_text
                    else:
                        print("텍스트 변화 없음.")
                else:
                    print("텍스트를 추출할 수 없습니다.")
            else:
                print("창을 찾을 수 없습니다,")
            time.sleep(5)
    except KeyboardInterrupt:
        print("프로그램을 종료합니다.")

if __name__ == "__main__":
    main()