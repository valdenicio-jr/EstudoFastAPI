import os 
from dotenv import load_dotenv

load_dotenv()

class Settings:
    ACCESS_TOKEN_EXPIRE: int = int(os.getenv("ACCESS_TOKEN_EXPIR", 99))
    SECRET_KEY: str = os.getenv("SECRET_KEY")   
    ALGORITHM: str = os.getenv("ALGORITHM")
    URL_DB: str = os.getenv("URL_DB")