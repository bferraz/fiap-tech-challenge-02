"""
Configurações da aplicação
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações da aplicação usando Pydantic Settings
    """
    APP_NAME: str = "API de Otimização de Escalas de Trabalho"
    APP_DESCRIPTION: str = "Sistema inteligente para geração e otimização de escalas usando algoritmos genéticos"
    VERSION: str = "1.0.0"
    
    # Configurações do servidor
    HOST: str = "localhost"
    PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Configurações do algoritmo genético (padrões)
    DEFAULT_POP_SIZE: int = 20
    DEFAULT_N_GERACOES: int = 80
    DEFAULT_TAXA_MUTACAO: float = 0.2
    DEFAULT_USAR_ELITISMO: bool = False
    
    # Configurações da escala (padrões)
    DEFAULT_CARGA_MAX_SEMANAL: int = 6
    DEFAULT_FOLGAS_OBRIGATORIAS: int = 1
    DEFAULT_COBERTURA_MINIMA: int = 2
    
    # Configurações de logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
