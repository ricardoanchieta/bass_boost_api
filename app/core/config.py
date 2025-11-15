"""
Configurações da aplicação Bass Boost API
"""
import os
from typing import Optional


class Settings:
    """Configurações da aplicação"""
    
    # API Info
    app_name: str = "Bass Boost API"
    app_description: str = "API para aumentar o grave de músicas MP3"
    app_version: str = "1.0.0"
    
    # Server Config
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = True
    reload: bool = True
    
    # Upload Config
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    allowed_extensions: list = ["mp3", "wav", "m4a", "flac"]
    max_duration_seconds: int = 600  # 10 minutos
    
    # Audio Processing Config
    default_bass_boost: int = 5
    min_bass_boost: int = -50
    max_bass_boost: int = 50
    
    # CORS Settings (pode ser sobrescrito por CORS_ORIGINS do ambiente)
    cors_origins: list = ["*"]
    cors_methods: list = ["GET", "POST"]
    cors_headers: list = ["*"]


# Instância global das configurações
settings = Settings()

# Sobrescrever CORS_ORIGINS via variável de ambiente (lista separada por vírgulas)
_cors_env = os.environ.get("CORS_ORIGINS")
if _cors_env:
    settings.cors_origins = [o.strip() for o in _cors_env.split(",") if o.strip()]
