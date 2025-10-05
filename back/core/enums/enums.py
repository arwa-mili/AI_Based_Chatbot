from enum import Enum


class ModelUsedEnum(str, Enum):
    GEMINI = "Gemini"
    GPT = "GPT"
    DEEPSEEK = "DEEPSEEK"

class SentByEnum(str, Enum):
    USER = "User"
    BOT = "Bot"
