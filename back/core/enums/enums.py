from enum import Enum


class ModelUsedEnum(str, Enum):
    GEMINI = "Gemini"
    LLAMA = "LLAMA"
    GPT = "GPT"

class SentByEnum(str, Enum):
    USER = "User"
    BOT = "Bot"
