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
    database_url: str = Field(..., env="DATABASE_URL")

    # JWT
    secret_key: str = Field(..., env="SECRET_KEY")
    authjwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    access_token_expire_minutes: int = Field(
        30,
        env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES",
    )
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False

    # Mail
    mail_username: str = Field(..., env="MAIL_USERNAME")
    mail_password: str = Field(..., env="MAIL_PASSWORD")
    mail_from: str = Field(..., env="MAIL_FROM")
    mail_port: int = Field(..., env="MAIL_PORT")
    mail_server: str = Field(..., env="MAIL_SERVER")
    mail_from_name: str = Field(..., env="MAIL_FROM_NAME")
    mail_use_tls: bool = Field(True, env="MAIL_USE_TLS")
    mail_use_ssl: bool = Field(False, env="MAIL_USE_SSL")

    # Redis
    redis_url: str = Field(..., env="REDIS_URL")

    # General settings
    debug: bool = Field(False, env="DEBUG")
    application_root: str = Field("/", env="APPLICATION_ROOT")
    preferred_url_scheme: str = Field("https", env="PREFERRED_URL_SCHEME")
    session_cookie_secure: bool = Field(True, env="SESSION_COOKIE_SECURE")
    security_password_salt: str = Field(..., env="SECURITY_PASSWORD_SALT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


@AuthJWT.load_config
def get_config():
    return settings
