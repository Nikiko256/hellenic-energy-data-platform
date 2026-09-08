from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    open_meteo_base_url: str = "https://archive-api.open-meteo.com/v1/archive"
    
    connect_timeout_seconds: float = 5.0
    read_timeout_seconds: float = 30.0
    
    retry_attempts: int = 3
    retry_wait_Seconds: float = 2.0
    
    model_config = SettingsConfigDict(
        env_prefix="HELLENIC_ENERGY_",
        env_file=".env",
        extra="ignore",
    )
    
settings = Settings()