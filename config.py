import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SHOPIFY_API_KEY = os.getenv("SHOPIFY_API_KEY")
SHOPIFY_ACCESS_TOKEN = os.getenv("SHOPIFY_PASSWORD")
SHOPIFY_STORE_URL = os.getenv("SHOPIFY_STORE_URL")

MODEL_NAME = "llama3-8b-8192"
