from pathlib import Path
import tempfile
import os
from dotenv import load_dotenv, find_dotenv

# IMPORTANT: dont import logger here (circular import)

env_path = find_dotenv()
load_dotenv(env_path)


class Config:
    BASE_URL_X_BACKEND = os.environ.get(
        "BASE_URL_X_BACKEND", 
        "http://ae1fadc0e73a64793bb68d7c9e29913d-1376196746.us-east-1.elb.amazonaws.com/backend"
    )