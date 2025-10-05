

#translator for the app generated content my models
import os
import requests

DEEPL_API_KEY = "152a76e2-77c6-4d39-8080-7de0ef0376a8:fx"
DEEPL_URL = "https://api-free.deepl.com/v2/translate" 
#this api is limited to 500,000 characters per month for free plan
def translate_text(text: str, source_lang: str,target_lang: str) -> str:
    """
    Translate text using DeepL REST API.
    
    Args:
        text: the text to translate
        target_lang: target language code (e.g., 'EN', 'AR')
        source_lang: source language code (optional)
    """
    data = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang.upper()
    }
    if source_lang:
        data["source_lang"] = source_lang.upper()
    
    try:
        response = requests.post(DEEPL_URL, data=data, timeout=15)
        response.raise_for_status()
        result = response.json()
        return result["translations"][0]["text"]
    except Exception as e:
        return text






# import httpx

# FTAPI_BASE_URL = "https://ftapi.pythonanywhere.com"
# # free api , translation not accurate ! using also open source library deep-translator
# # from deep_translator : GoogleTranslator (src: https://deep-translator-api.azurewebsites.net/google/")
# # gave same poor result

# def translate_text(text: str, source: str, target: str = None) -> dict:
#     """
#     Translate text using Free Translate API.
#     If source is None, API will auto-detect language.
#     Returns: dict with keys: source-language, destination-language, destination-text
#     """
#     params = {"dl": target, "text": text}
#     if source:
#         params["sl"] = source

#     try:
#         response = httpx.get(f"{FTAPI_BASE_URL}/translate", params=params, timeout=15)
#         response.raise_for_status()
#         print(response.json()["destination-text"])
#         return response.json()["destination-text"]
#     except Exception as e:
#         return {
#             "source-language": source or "auto",
#             "destination-language": target,
#             "destination-text": text
#         }
        
# Alternative using DeepL API (commented out due to usage limits)
# Other alternative : Local modls from hugging face (not implemented here)
# Resorted finally to free usage of deepL for less complexity of loading and deployment (will work fine for POC in the next month)
        
