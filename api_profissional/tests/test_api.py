"""
Testes básicos para a API
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    """Testa o health check"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root_endpoint():
    """Testa o endpoint raiz"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data
    assert "version" in data


def test_configuracao_exemplo():
    """Testa o endpoint de configuração de exemplo"""
    response = client.get("/api/v1/exemplo")
    assert response.status_code == 200
    data = response.json()
    assert "funcionarios" in data
    assert "carga_max_semanal" in data
    assert "parametros" in data


def test_otimizar_escala():
    """Testa o endpoint de otimização"""
    config = {
        "funcionarios": [
            {"id": 1, "nome": "Ana", "preferencias_folga": ["domingo"]},
            {"id": 2, "nome": "Bruno", "preferencias_folga": ["sábado"]}
        ],
        "carga_max_semanal": 6,
        "folgas_obrigatorias": 1,
        "cobertura_minima": 1,
        "parametros": {
            "pop_size": 10,
            "n_geracoes": 20,
            "taxa_mutacao": 0.2,
            "usar_elitismo": True
        }
    }
    
    response = client.post("/api/v1/otimizar", json=config)
    assert response.status_code == 200
    data = response.json()
    assert "escala_otimizada" in data
    assert "num_violacoes" in data
    assert "evolucao_fitness" in data
    assert "tempo_execucao" in data


def test_validar_escala():
    """Testa o endpoint de validação"""
    dados = {
        "escala": {
            "1": {
                "segunda": {"manha": 1, "tarde": 0, "noite": 0},
                "terça": {"manha": 0, "tarde": 1, "noite": 0},
                "quarta": {"manha": 0, "tarde": 0, "noite": 1},
                "quinta": {"manha": 0, "tarde": 0, "noite": 0},
                "sexta": {"manha": 0, "tarde": 0, "noite": 0},
                "sábado": {"manha": 0, "tarde": 0, "noite": 0},
                "domingo": {"manha": 0, "tarde": 0, "noite": 0}
            }
        },
        "funcionarios": [
            {"id": 1, "nome": "Ana", "preferencias_folga": ["domingo"]}
        ]
    }
    
    response = client.post("/api/v1/validar", json=dados)
    assert response.status_code == 200
    data = response.json()
    assert "escala_valida" in data
    assert "num_violacoes" in data
    assert "violacoes" in data
    assert "estatisticas" in data
