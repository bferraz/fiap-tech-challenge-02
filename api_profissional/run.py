"""
Arquivo de entrada para execução local da API
"""

import uvicorn
from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    print(f"🚀 Iniciando {settings.APP_NAME}...")
    print(f"📖 Documentação disponível em: http://{settings.HOST}:{settings.PORT}/docs")
    print(f"🔗 API disponível em: http://{settings.HOST}:{settings.PORT}")
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
