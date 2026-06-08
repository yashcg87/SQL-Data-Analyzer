import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PG_URI = os.getenv('PG_URI')
    AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
    AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')
    AZURE_OPENAI_API_VERSION = os.getenv('AZURE_OPENAI_API_VERSION')
    AZURE_OPENAI_EMB_DEPLOYMENT = os.getenv('AZURE_OPENAI_EMB_DEPLOYMENT')
    MONGO_URI = os.getenv("MONGO_URI")
    
    
    DB_NAME = "My_DB"
    COLLECTION_NAME = "metadata_embeddings"
    INDEX = "my_semantic_idx"
    