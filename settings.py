import os
from dotenv import find_dotenv, load_dotenv


_ = load_dotenv(find_dotenv())

# ImageBB settings
IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY")
IMGBB_EXPIRY_TIME = 60 * 10 # 10 minutes
IMGBB_URL = "https://api.imgbb.com/1/upload"

# Streamlit settings
STREAMLIT_PORT = os.environ.get("PORT", 8501)

# Constants
## LLM and Agent settings
LLM_MODEL = "gpt-4o"
