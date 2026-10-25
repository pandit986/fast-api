import os
from dotenv import load_dotenv


load_dotenv()  # Load environment variables from .env file


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY")  # Get
    origin: str = os.getenv("origins")  # Get allowed origins from environment variables
    DB_URL: str = os.getenv("DB_URL")  # Get database URL from environment variables


settings = Settings()

# # allow origins for CORS
# origins = os.getenv("origins")  # Get allowed origins from environment variables

# # Configure CORS

# SECRET_KEY = os.getenv("SECRET_KEY")  # Get secret key from environment variables
# DB_URL = os.getenv("DB_URL")  # Get database URL from environment variables