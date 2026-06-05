from app.core.config import Settings
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

settings = Settings()

class Model:
    def __init__(self):
        self.AZURE_OPENAI_DEPLOYMENT = settings.AZURE_OPENAI_DEPLOYMENT
        self.AZURE_OPENAI_ENDPOINT = settings.AZURE_OPENAI_ENDPOINT
        self.AZURE_OPENAI_EMB_DEPLOYMENT = settings.AZURE_OPENAI_EMB_DEPLOYMENT
        self.AZURE_OPENAI_API_VERSION = settings.AZURE_OPENAI_API_VERSION
        self.AZURE_OPENAI_API_KEY = settings.AZURE_OPENAI_API_KEY
        
    def get_model(self):
        model = AzureChatOpenAI(
        azure_deployment=self.AZURE_OPENAI_DEPLOYMENT,
        api_version=self.AZURE_OPENAI_API_VERSION,
        azure_endpoint=self.AZURE_OPENAI_ENDPOINT,
        api_key=self.AZURE_OPENAI_API_KEY
        )
        return model  
    
    def get_embedding_model(self):
        embeddings = AzureOpenAIEmbeddings(
        azure_endpoint=self.AZURE_OPENAI_ENDPOINT,
        azure_deployment=self.AZURE_OPENAI_EMB_DEPLOYMENT,
        openai_api_version=self.AZURE_OPENAI_API_VERSION,
        api_key=self.AZURE_OPENAI_API_KEY
        )
        return embeddings  
    
    
    
    