from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    FIREBASE_TYPE: str
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY : str
    FIREBASE_CLIENT_EMAIL : str
    FIREBASE_CLIENT_ID : str
    FIREBASE_AUTH_URI : str
    FIREBASE_TOKEN_URI : str
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL : str
    FIREBASE_CLIENT_X509_CERT_URL : str
    FIREBASE_UNIVERSE_DOMAIN : str
    FIREBASE_BUCKET :str
    
    class Config:
        env_file = ".env"
        

