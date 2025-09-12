"""
Modelos Pydantic para validação de dados de áudio
"""
from pydantic import BaseModel, Field, validator
from typing import Optional


class BassBoostRequest(BaseModel):
    """Modelo para requisição de bass boost"""
    boost_number: int = Field(
        default=5,
        ge=-50, 
        le=50,
        description="Número para aumentar/diminuir o grave (entre -50 e 50)"
    )
    
    @validator('boost_number')
    def validate_boost_number(cls, v):
        if not -50 <= v <= 50:
            raise ValueError('boost_number deve estar entre -50 e 50')
        return v


class AudioResponse(BaseModel):
    """Modelo para resposta de processamento de áudio"""
    message: str
    original_filename: str
    processed_filename: str
    boost_applied: int
    file_size_bytes: Optional[int] = None


class ErrorResponse(BaseModel):
    """Modelo para respostas de erro"""
    error: str
    detail: Optional[str] = None
    status_code: int


class HealthResponse(BaseModel):
    """Modelo para resposta de health check"""
    status: str = "healthy"
    app_name: str
    version: str


class APIInfo(BaseModel):
    """Modelo para informações da API"""
    message: str
    description: str
    version: str
    endpoints: dict[str, str]
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
