"""
Endpoints para health check e informações da API
"""
from fastapi import APIRouter

from ...models.audio_models import HealthResponse, APIInfo
from ...core.config import settings


router = APIRouter(
    tags=["System"]
)


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verifica se a API está funcionando corretamente"
)
async def health_check():
    """Endpoint para verificar se a API está funcionando"""
    return HealthResponse(
        status="healthy",
        app_name=settings.app_name,
        version=settings.app_version
    )


@router.get(
    "/",
    response_model=APIInfo,
    summary="Informações da API",
    description="Retorna informações básicas sobre a API"
)
async def root():
    """Endpoint raiz com informações da API"""
    return APIInfo(
        message=f"Bem-vindo ao {settings.app_name}",
        description=settings.app_description,
        version=settings.app_version,
        endpoints={
            "/audio/bass_boost": "POST - Aumentar grave do arquivo MP3",
            "/health": "GET - Verificar saúde da API",
            "/docs": "GET - Documentação interativa (Swagger UI)",
            "/redoc": "GET - Documentação alternativa (ReDoc)"
        },
        docs_url="/docs",
        redoc_url="/redoc"
    )
