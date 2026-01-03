import os 
from dataclasses import dataclass

@dataclass
class Config:
    LLM_MODEL: str = "deepseek-r1:7b"
    EMBEDDING_MODEL: str = "bge-m3"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.8
    TOP_P: float = 0.9
    PERSIST_DIRECTORY: str = "./chroma_db"
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    DEFAULT_ARTICLE_LENGTH: int = 800
    MIN_ARTICLE_LENGTH: int = 300

config = Config()