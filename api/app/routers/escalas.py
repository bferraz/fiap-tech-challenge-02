"""
Router para endpoints relacionados a escalas
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.core.constants import DIAS_SEMANA, TURNOS
from app.models.schemas import (
    ConfiguracaoEscala, 
    EscalaCompleta, 
    ResultadoOtimizacao, 
    ValidacaoEscala
)
from app.services.genetic_algorithm import EscalaGeneticaService

router = APIRouter()


@router.post("/otimizar", response_model=ResultadoOtimizacao)
async def otimizar_escala(config: ConfiguracaoEscala):
    """
    Gera uma escala de trabalho otimizada usando algoritmo genético
    
    - **funcionarios**: Lista de funcionários com suas preferências
    - **carga_max_semanal**: Máximo de turnos por funcionário por semana
    - **folgas_obrigatorias**: Mínimo de folgas por funcionário por semana
    - **cobertura_minima**: Mínimo de funcionários necessários por turno
    - **parametros**: Configurações do algoritmo genético (opcional)
    """
    try:
        # Validações básicas
        if len(config.funcionarios) == 0:
            raise HTTPException(
                status_code=400, 
                detail="Lista de funcionários não pode estar vazia"
            )
        
        if config.carga_max_semanal > len(DIAS_SEMANA) * len(TURNOS):
            raise HTTPException(
                status_code=400, 
                detail="Carga máxima semanal excede turnos disponíveis"
            )
        
        # Executar otimização
        service = EscalaGeneticaService(config)
        escala_otimizada, evolucao, tempo = service.otimizar()
        
        # Avaliar resultado final
        num_violacoes = service.avaliar_individuo(escala_otimizada)
        
        return ResultadoOtimizacao(
            escala_otimizada=escala_otimizada,
            num_violacoes=num_violacoes,
            evolucao_fitness=evolucao,
            tempo_execucao=tempo,
            parametros_utilizados=service.params
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro na otimização: {str(e)}"
        )


@router.post("/validar", response_model=ValidacaoEscala)
async def validar_escala(dados: EscalaCompleta):
    """
    Valida uma escala existente verificando todas as restrições
    
    - **escala**: Escala completa para validação (dict com id do funcionário como chave)
    - **funcionarios**: Lista de funcionários correspondente        
    """
    try:
        # Criar configuração temporária para validação
        config_temp = ConfiguracaoEscala(funcionarios=dados.funcionarios)
        service = EscalaGeneticaService(config_temp)
        
        # Verificar violações
        violacoes = service.checar_restricoes(dados.escala)
        
        # Calcular estatísticas
        estatisticas = service.calcular_estatisticas(dados.escala)
        
        return ValidacaoEscala(
            escala_valida=len(violacoes) == 0,
            num_violacoes=len(violacoes),
            violacoes=violacoes,
            estatisticas=estatisticas
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Erro na validação: {str(e)}"
        )
