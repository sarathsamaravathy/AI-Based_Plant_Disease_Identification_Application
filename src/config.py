"""Configuration Management"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """Application settings from environment variables."""
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_debug: bool = False
    api_workers: int = 4
    
    # Database
    database_url: str = "postgresql://farmer:password@localhost:5432/plant_disease_db"
    database_echo: bool = False
    
    # LLM Configuration
    llm_model: str = "llama2"
    llm_api_url: str = "http://localhost:11434/api"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 1024
    llm_use_local: bool = True
    
    # Vector Database (Chroma - local)
    vector_db_type: str = "chroma"
    chroma_persist_dir: str = "./data/vector_store"
    
    # Multilingual
    default_language: str = "en"
    supported_languages: str = "en,hi,ta,te,ka,ml,kn,mr,gu,bn"
    translation_service: str = "indicnlp"
    tts_engine: str = "indic_tts"
    
    # Vision Model
    vision_model: str = "efficientnet_v2"
    vision_model_path: str = "./models/vision/"
    confidence_threshold: float = 0.6
    
    # MLOps
    mlflow_tracking_uri: str = "http://localhost:5000"
    mlflow_artifact_store: str = "./mlruns"
    enable_drift_monitoring: bool = True
    
    # Image Processing
    max_image_size: int = 10485760
    allowed_image_formats: str = "jpg,jpeg,png,webp"
    image_upload_dir: str = "./uploads"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/app.log"
    
    # Security
    secret_key: str = "your-secret-key-here"
    allowed_origins: str = "http://localhost:3000,http://localhost:8080,http://localhost:5173"
    
    # Feature Flags
    enable_feedback_loop: bool = True
    enable_offline_mode: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @property
    def supported_langs_list(self) -> List[str]:
        return self.supported_languages.split(",")
    
    @property
    def allowed_origins_list(self) -> List[str]:
        return self.allowed_origins.split(",")

settings = Settings()
