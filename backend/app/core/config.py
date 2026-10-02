from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "EIGEN AI Email Operations"

    database_url: str

    gemini_api_key: str
    gemini_model: str = "gemini-3.8-flash"

    class Config:
        env_file = ".env"


settings = Settings()