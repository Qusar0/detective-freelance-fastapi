from pydantic import BaseSettings, Field
from fastapi_jwt_auth import AuthJWT
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Database
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    sqlalchemy_track_modifications: bool = Field(True, env="SQLALCHEMY_TRACK_MODIFICATIONS")

    # JWT
    secret_key: str = Field(..., env="SECRET_KEY")
    authjwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(21600, env="JWT_ACCESS_TOKEN_EXPIRES")
    refresh_token_expire_minutes: int = Field(604800, env="JWT_REFRESH_TOKEN_EXPIRES")
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False

    # Mail
    mail_username: str = Field(..., env="MAIL_USERNAME")
    mail_password: str = Field(..., env="MAIL_PASSWORD")
    mail_from: str = Field(..., env="MAIL_DEFAULT_SENDER")
    mail_port: int = Field(..., env="MAIL_PORT")
    mail_server: str = Field(..., env="MAIL_SERVER")
    mail_use_tls: bool = Field(True, env="MAIL_USE_TLS")
    mail_use_ssl: bool = Field(False, env="MAIL_USE_SSL")

    # Redis
    redis_url: str = Field(..., env="REDIS_URL")

    # General settings
    debug: bool = Field(True, env="DEBUG")
    application_root: str = Field("/", env="APPLICATION_ROOT")
    preferred_url_scheme: str = Field("https", env="PREFERRED_URL_SCHEME")
    session_cookie_secure: bool = Field(True, env="SESSION_COOKIE_SECURE")
    security_password_salt: str = Field(..., env="SECURITY_PASSWORD_SALT")

    # Telegram Bot
    telegram_api_id: int = Field(..., env="TELEGRAM_API_ID")
    telegram_api_hash: str = Field(..., env="TELEGRAM_API_HASH")
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    telegram_db_encryption_key: str = Field(..., env="TELEGRAM_DB_ENCRYPTION_KEY")
    admin_chat_id: int = Field(..., env="ADMIN_CHAT_ID")

    # Notification Bot
    notification_bot_token: str = Field(..., env="NOTIFICATION_BOT_TOKEN")

    # Support Bot
    support_bot_token: str = Field(..., env="SUPPORT_BOT_TOKEN")

    # XML River API
    xml_river_user_id: str = Field(..., env="XML_RIVER_USER_ID")
    xml_river_api_key: str = Field(..., env="XML_RIVER_API_KEY")

    # Utils
    utils_token: str = Field(..., env="UTILS_TOKEN")
    lighthouse_url: str = Field(..., env="LIGHTHOUSE_URL")

    # Frontend URLs
    frontend_url: str = Field(..., env="FRONTEND_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
