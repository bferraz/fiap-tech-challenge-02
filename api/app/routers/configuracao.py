"""
Router para endpoints de configuração
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/exemplo")
async def exemplo_configuracao():
    """
    Retorna um exemplo completo de configuração para otimização
    """
    return {
        "funcionarios": [
            {"id": 1, "nome": "Ana", "preferencias_folga": ["domingo"]},
            {"id": 2, "nome": "Bruno", "preferencias_folga": ["sábado"]},
            {"id": 3, "nome": "Carla", "preferencias_folga": ["segunda"]},
            {"id": 4, "nome": "Diego", "preferencias_folga": ["terça"]},
            {"id": 5, "nome": "Elisa", "preferencias_folga": ["quarta"]},
            {"id": 6, "nome": "Felipe", "preferencias_folga": ["sexta"]}
        ],
        "carga_max_semanal": 6,
        "folgas_obrigatorias": 1,
        "cobertura_minima": 2,
        "parametros": {
            "pop_size": 30,
            "n_geracoes": 100,
            "taxa_mutacao": 0.2,
            "usar_elitismo": True
        }
    }
