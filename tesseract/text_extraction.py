#import pytesseract
#from PIL import Image

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

#def extract_text_from_image(image):
#    """이미지에서 텍스트 추출"""
#    return pytesseract.image_to_string(image)

import easyocr
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import numpy as np
import time

# easyocr Reader 초기화 (GPU 사용)
reader = easyocr.Reader(['en'], gpu=True)

def preprocess_image(image):
    """이미지 전처리"""
    # 그레이스케일 변환
    gray_image = ImageOps.grayscale(image)
    
    # 이미지 대비 조정
    enhancer = ImageEnhance.Contrast(gray_image)
    enhanced_image = enhancer.enhance(2.0)
    
    # 샤프닝 필터 적용
    sharpened_image = enhanced_image.filter(ImageFilter.SHARPEN)
    
    return sharpened_image

def extract_text_from_image(image):
    """이미지에서 텍스트 추출"""
    start_time = time.time()
    
    # 이미지 전처리
    preprocessed_image = preprocess_image(image)
    
    # 이미지를 numpy 배열로 변환하고 uint8 형식으로 변환
    image_np = np.array(preprocessed_image).astype(np.uint8)
    
    # 디버깅을 위한 로그 추가
    #print("전처리된 이미지 배열:", image_np)
    
    # easyocr을 사용하여 텍스트 추출
    result = reader.readtext(image_np, detail=0, contrast_ths=0.1, adjust_contrast=0.5, text_threshold=0.6)
    
    # 디버깅을 위한 로그 추가
    #print("추출된 텍스트:", result)
    
    # 추출된 텍스트를 하나의 문자열로 결합
    extracted_text = ' '.join(result)
    
    end_time = time.time()
    print(f"텍스트 추출에 걸린 시간: {end_time - start_time:.2f}초")
    print("최종 추출된 텍스트:", extracted_text)
    return extracted_text
    