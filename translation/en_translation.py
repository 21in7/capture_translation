import requests
import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()
DEEPL_API_KEY = os.getenv('DEEPL_API_KEY')

def translate_text(text, source_lang='en', target_lang='ko'):
    """DeepL API를 이용해 텍스트 번역"""
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
    }
    data = {
        "text": text,
        "source_lang": source_lang,
        "target_lang": target_lang,
    }
    response = requests.post(url, headers=headers, data=data)
    try:
        result = response.json()
        if 'translations' in result:
            return result['translations'][0]['text']
        else:
            print("Error:", result.get('message', 'Unknown Error'))
            return None
    except requests.exceptions.JSONDecodeError as e:
        print("JSON Decode Error:", e)
        return None