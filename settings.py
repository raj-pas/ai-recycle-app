import os
from dotenv import find_dotenv, load_dotenv


_ = load_dotenv(find_dotenv())

# ImageBB settings
IMGBB_API_KEY = os.environ.get("IMGBB_API_KEY")
IMGBB_EXPIRY_TIME = 60 * 5  # 5 minutes
IMGBB_URL = "https://api.imgbb.com/1/upload"

# Constants
## LLM and Agent settings
LLM_MODEL = "gpt-4o"
