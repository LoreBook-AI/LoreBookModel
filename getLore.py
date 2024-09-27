import anthropic
import time
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access the variables

api_key = os.getenv('API_KEY')

print(api_key)
