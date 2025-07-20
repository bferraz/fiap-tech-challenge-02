"""
Modelos Pydantic para validação de dados
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

from app.core.constants import (
    MIN_POP_SIZE, MAX_POP_SIZE, MIN_N_GERACOES, MAX_N_GERACOES,
    MIN_TAXA_MUTACAO, MAX_TAXA_MUTACAO, MIN_CARGA_MAX_SEMANAL,
    MAX_CARGA_MAX_SEMANAL, MIN_FOLGAS_OBRIGATORIAS, MAX_FOLGAS_OBRIGATORIAS,
    MIN_COBERTURA_MINIMA, MAX_COBERTURA_MINIMA
)


class Funcionario(BaseModel):
    """Modelo para representar um funcionário"""
    id: int
    nome: str
    preferencias_folga: List[str] = Field(
        default=[], 
        description="Dias da semana preferidos para folga"
    )


class ParametrosAlgoritmo(BaseModel):
    """Modelo para parâmetros do algoritmo genético"""
    pop_size: int = Field(
        default=20, 
        ge=MIN_POP_SIZE, 
        le=MAX_POP_SIZE, 
        description="Tamanho da população"
    )
    n_geracoes: int = Field(
        default=80, 
        ge=MIN_N_GERACOES, 
        le=MAX_N_GERACOES, 
        description="Número de gerações"
    )
    taxa_mutacao: float = Field(
        default=0.2, 
        ge=MIN_TAXA_MUTACAO, 
        le=MAX_TAXA_MUTACAO, 
        description="Taxa de mutação"
    )
    usar_elitismo: bool = Field(
        default=False, 
        description="Usar elitismo na evolução"
    )


class ConfiguracaoEscala(BaseModel):
    """Modelo para configuração da escala"""
    funcionarios: List[Funcionario]
    carga_max_semanal: int = Field(
        default=6, 
        ge=MIN_CARGA_MAX_SEMANAL, 
        le=MAX_CARGA_MAX_SEMANAL, 
        description="Máximo de turnos por semana"
    )
    folgas_obrigatorias: int = Field(
        default=1, 
        ge=MIN_FOLGAS_OBRIGATORIAS, 
        le=MAX_FOLGAS_OBRIGATORIAS, 
        description="Mínimo de folgas por semana"
    )
    cobertura_minima: int = Field(
        default=2, 
        ge=MIN_COBERTURA_MINIMA, 
        le=MAX_COBERTURA_MINIMA, 
        description="Mínimo de funcionários por turno"
    )
    parametros: Optional[ParametrosAlgoritmo] = None


class EscalaCompleta(BaseModel):
    """Modelo para escala completa"""
    escala: Dict[int, Dict[str, Dict[str, int]]]
    funcionarios: List[Funcionario]
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "escala": {
                    "1": {
                        "segunda": {"manha": 0, "tarde": 0, "noite": 0},
                        "terça": {"manha": 0, "tarde": 0, "noite": 0},
                        "quarta": {"manha": 0, "tarde": 0, "noite": 0},
                        "quinta": {"manha": 1, "tarde": 0, "noite": 0},
                        "sexta": {"manha": 0, "tarde": 0, "noite": 0},
                        "sábado": {"manha": 1, "tarde": 0, "noite": 0},
                        "domingo": {"manha": 1, "tarde": 0, "noite": 1}
                    },
                    "2": {
                        "segunda": {"manha": 1, "tarde": 0, "noite": 0},
                        "terça": {"manha": 1, "tarde": 1, "noite": 0},
                        "quarta": {"manha": 0, "tarde": 0, "noite": 0},
                        "quinta": {"manha": 0, "tarde": 0, "noite": 1},
                        "sexta": {"manha": 1, "tarde": 1, "noite": 1},
                        "sábado": {"manha": 0, "tarde": 0, "noite": 1},
                        "domingo": {"manha": 1, "tarde": 1, "noite": 0}
                    },
                    "3": {
                        "segunda": {"manha": 0, "tarde": 0, "noite": 0},
                        "terça": {"manha": 0, "tarde": 0, "noite": 0},
                        "quarta": {"manha": 0, "tarde": 0, "noite": 1},
                        "quinta": {"manha": 0, "tarde": 0, "noite": 1},
                        "sexta": {"manha": 0, "tarde": 1, "noite": 1},
                        "sábado": {"manha": 0, "tarde": 1, "noite": 0},
                        "domingo": {"manha": 0, "tarde": 0, "noite": 0}
                    },
                    "4": {
                        "segunda": {"manha": 1, "tarde": 0, "noite": 0},
                        "terça": {"manha": 0, "tarde": 1, "noite": 0},
                        "quarta": {"manha": 1, "tarde": 0, "noite": 0},
                        "quinta": {"manha": 0, "tarde": 1, "noite": 0},
                        "sexta": {"manha": 0, "tarde": 0, "noite": 0},
                        "sábado": {"manha": 0, "tarde": 0, "noite": 1},
                        "domingo": {"manha": 0, "tarde": 1, "noite": 0}
                    },
                    "5": {
                        "segunda": {"manha": 1, "tarde": 1, "noite": 1},
                        "terça": {"manha": 0, "tarde": 0, "noite": 1},
                        "quarta": {"manha": 1, "tarde": 1, "noite": 0},
                        "quinta": {"manha": 0, "tarde": 0, "noite": 0},
                        "sexta": {"manha": 1, "tarde": 0, "noite": 0},
                        "sábado": {"manha": 0, "tarde": 1, "noite": 1},
                        "domingo": {"manha": 0, "tarde": 0, "noite": 1}
                    },
                    "6": {
                        "segunda": {"manha": 0, "tarde": 1, "noite": 1},
                        "terça": {"manha": 1, "tarde": 0, "noite": 1},
                        "quarta": {"manha": 0, "tarde": 1, "noite": 1},
                        "quinta": {"manha": 1, "tarde": 1, "noite": 0},
                        "sexta": {"manha": 0, "tarde": 0, "noite": 0},
                        "sábado": {"manha": 1, "tarde": 1, "noite": 1},
                        "domingo": {"manha": 1, "tarde": 0, "noite": 0}
                    }
                },
                "funcionarios": [
                    {"id": 1, "nome": "Ana", "preferencias_folga": ["domingo"]},
                    {"id": 2, "nome": "Bruno", "preferencias_folga": ["sábado"]},
                    {"id": 3, "nome": "Carla", "preferencias_folga": ["segunda"]},
                    {"id": 4, "nome": "Diego", "preferencias_folga": ["terça"]},
                    {"id": 5, "nome": "Elisa", "preferencias_folga": ["quarta"]},
                    {"id": 6, "nome": "Felipe", "preferencias_folga": ["sexta"]}
                ]
            }
        }
    }


class ResultadoOtimizacao(BaseModel):
    """Modelo para resultado da otimização"""
    escala_otimizada: Dict[int, Dict[str, Dict[str, int]]]
    num_violacoes: int
    evolucao_fitness: List[int]
    tempo_execucao: float
    parametros_utilizados: ParametrosAlgoritmo


class ValidacaoEscala(BaseModel):
    """Modelo para resultado da validação"""
    escala_valida: bool
    num_violacoes: int
    violacoes: List[str]
    estatisticas: Dict[str, Any]


class ErrorResponse(BaseModel):
    """Modelo para resposta de erro"""
    error: str
    detail: str
    timestamp: str
