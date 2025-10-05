ERROR_MESSAGES = {
    "VALIDATION_ERROR": {
        "en": "Validation error occurred.",
        "ar": "حدث خطأ في التحقق من صحة البيانات."
    },
    "PROBLEM": {
        "en": "An unexpected problem occurred.",
        "ar": "حدث خطأ غير متوقع."
    },
    "CONVERSATIONS_RETURNED_SUCCESSFULLY": {
        "en": "Conversations retrieved successfully.",
        "ar": "تم استرجاع المحادثة بنجاح."
    },
    "AUTHENTICATION_ERROR": {
        "en": "Authentication failed. Please log in again.",
        "ar": "فشل التحقق من الهوية. الرجاء تسجيل الدخول مرة أخرى."
    },
    "NOT_FOUND": {
        "en": "The requested resource was not found.",
        "ar": "المورد المطلوب غير موجود."
    },
}
    

def t(message_key: str, language_code: str = "en") -> str:
    """
    Simple translator function for backend messages.
    Falls back to English if translation not found.
    """
    language_code = language_code.split("-")[0] 
    return ERROR_MESSAGES.get(message_key, {}).get(language_code, message_key)
