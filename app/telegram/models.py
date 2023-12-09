from pydantic import BaseModel

class TelegramConfig(BaseModel):
    token: str