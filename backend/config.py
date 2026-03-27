from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    db_host: str = "db"
    db_port: int = 5432
    db_name: str = "nailydews"
    db_user: str = "nailydews"
    db_password: str = "change_me_in_production"

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # Claude API
    anthropic_api_key: str = ""

    # Discord (optional, for Discord channel scraping)
    discord_bot_token: str = ""

    # App
    app_env: str = "production"
    app_secret_key: str = "change_me_random_string"
    digest_time: str = "19:00"
    digest_timezone: str = "Europe/Berlin"

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @property
    def sync_database_url(self) -> str:
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"


settings = Settings()
