from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = ""
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str
    secret: str
    secret_parse: int
    log_level: str

    @property
    def database_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"


settings = Settings()
