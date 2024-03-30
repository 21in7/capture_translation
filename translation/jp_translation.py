import requests
from langdetect import detect
from config import config

def translate_text(text, source_lang='ja', target_lang='ko'):
    """DeepL API를 이용해 텍스트 번역"""
    url = "https://api-free.deepl.com/v2/translate"
    headers = {
        "Authorization": f"DeepL-Auth-Key {config.DEEPL_API_KEY}"
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