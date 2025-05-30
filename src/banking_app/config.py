# src/banking_app/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env

class Config:
    DB_HOST = os.getenv('HOSTNAME')
    DB_PORT = int(os.getenv('PORT', 3306))
    DB_USER = os.getenv('USERNAME')
    DB_PASSWORD = os.getenv('PASSWORD')
    DB_NAME = os.getenv('DATABASE')



config = Config()