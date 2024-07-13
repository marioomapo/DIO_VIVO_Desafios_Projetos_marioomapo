from pydantic_settings import BaseSettings
from pydantic import Field

# criando a classe de configurações, ou seja, os tipos de configuração da API
class Settings(BaseSettings):
    DB_URL: str = Field(default='postgresql+asyncpg://workout:workout@localhost/workout')

settings = Settings()