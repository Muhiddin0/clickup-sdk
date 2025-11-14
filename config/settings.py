"""
Application settings and configuration management.
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # ClickUp API Configuration
    CLICKUP_API_TOKEN: str = os.getenv("CLICKUP_API_TOKEN", "")
    TEAM_ID: str = os.getenv("TEAM_ID", "")
    
    # Telegram Bot Configuration
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    
    # Webhook Configuration
    WEBHOOK_SECRET: Optional[str] = os.getenv("WEBHOOK_SECRET", None)
    WEBHOOK_ENDPOINT: str = os.getenv(
        "WEBHOOK_ENDPOINT", 
        "https://clickup.venu.uz/clickup-webhook"
    )
    WEBHOOK_PATH: str = os.getenv("WEBHOOK_PATH", "/clickup-webhook")
    
    # Server Configuration
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "3000"))
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_DIR: str = os.getenv("LOG_DIR", "logs")
    LOG_FILE_MAX_BYTES: int = int(os.getenv("LOG_FILE_MAX_BYTES", "10485760"))  # 10MB
    LOG_FILE_BACKUP_COUNT: int = int(os.getenv("LOG_FILE_BACKUP_COUNT", "5"))
    
    # Application Configuration
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    RELOAD: bool = os.getenv("RELOAD", "True").lower() == "true"
    
    def validate(self) -> None:
        """
        Validate that all required settings are present.
        
        Raises:
            ValueError: If required settings are missing
        """
        required_settings = {
            "CLICKUP_API_TOKEN": self.CLICKUP_API_TOKEN,
            "TEAM_ID": self.TEAM_ID,
            "BOT_TOKEN": self.BOT_TOKEN,
        }
        
        missing = [key for key, value in required_settings.items() if not value]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Get or create global settings instance.
    
    Returns:
        Settings instance
    """
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.validate()
    return _settings

