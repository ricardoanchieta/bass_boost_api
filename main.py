"""
Ponto de entrada principal da aplicação Bass Boost API
"""
import uvicorn
from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    print(f"🎵 Iniciando {settings.app_name} v{settings.app_version}")
    print(f"📖 Documentação: http://{settings.host}:{settings.port}/docs")
    print(f"🔧 Health Check: http://{settings.host}:{settings.port}/health")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        reload_dirs=["app"],
        log_level="info"
    )
