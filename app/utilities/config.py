from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_whatsapp_from: str = "whatsapp:+14155238886"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
