from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	bot_token: str
	webhook_host: str
	webhook_path: str

	class Config:
		env_file = ".env"

settings = Settings()
WEBHOOK_URL = settings.webhook_host + settings.webhook_path