import os
from dotenv import load_dotenv

load_dotenv()
API_BASE_URL = os.getenv("QG_API_URL", "http://localhost:8000")

