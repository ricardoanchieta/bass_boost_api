"""
Aplicação principal FastAPI - Bass Boost API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
import time

from .core.config import settings
from .api.endpoints import bass_boost, health


def create_application() -> FastAPI:
    """Cria e configura a aplicação FastAPI"""
    
    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    # Middleware CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )
    
    # Middleware para medir tempo de resposta
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response
    
    # Incluir routers
    app.include_router(bass_boost.router)
    app.include_router(health.router)
    
    # Handler global de exceções
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Erro interno do servidor",
                "detail": str(exc) if settings.debug else "Algo deu errado"
            }
        )
    
    return app


# Instância da aplicação
app = create_application()
