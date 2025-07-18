"""
Arquivo principal da aplicação FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import escalas, configuracao


def create_application() -> FastAPI:
    """
    Cria e configura a aplicação FastAPI
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    
    # Configurar CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Incluir routers
    app.include_router(escalas.router, prefix="/api/v1", tags=["escalas"])
    app.include_router(configuracao.router, prefix="/api/v1", tags=["configuracao"])
    
    return app


app = create_application()


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.VERSION
    }


@app.get("/health")
async def health_check():
    """Health check endpoint para load balancers"""
    return {"status": "healthy"}
