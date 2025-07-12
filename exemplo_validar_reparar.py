"""
Exemplo de como usar os endpoints /validar e /reparar corretamente
"""

import requests
import json

BASE_URL = "http://localhost:8000"

# 1. Primeiro, obter a lista de funcionários de exemplo
print("1. Obtendo lista de funcionários...")
response = requests.get(f"{BASE_URL}/funcionarios/exemplo")
funcionarios_response = response.json()
funcionarios = funcionarios_response['funcionarios']  # Extrair a lista
print(f"✅ Obtidos {len(funcionarios)} funcionários")

# 2. Sua escala (a que você tentou enviar)
escala = {
    "1": {
        "segunda": {"manha": 0, "tarde": 1, "noite": 0},
        "terça": {"manha": 1, "tarde": 0, "noite": 0},
        "quarta": {"manha": 1, "tarde": 0, "noite": 0},
        "quinta": {"manha": 0, "tarde": 0, "noite": 0},
        "sexta": {"manha": 0, "tarde": 0, "noite": 0},
        "sábado": {"manha": 0, "tarde": 1, "noite": 0},
        "domingo": {"manha": 1, "tarde": 1, "noite": 0}
    },
    "2": {
        "segunda": {"manha": 1, "tarde": 1, "noite": 1},
        "terça": {"manha": 0, "tarde": 0, "noite": 0},
        "quarta": {"manha": 0, "tarde": 1, "noite": 1},
        "quinta": {"manha": 0, "tarde": 0, "noite": 0},
        "sexta": {"manha": 0, "tarde": 1, "noite": 1},
        "sábado": {"manha": 1, "tarde": 0, "noite": 0},
        "domingo": {"manha": 0, "tarde": 1, "noite": 1}
    },
    "3": {
        "segunda": {"manha": 0, "tarde": 0, "noite": 0},
        "terça": {"manha": 0, "tarde": 1, "noite": 0},
        "quarta": {"manha": 0, "tarde": 0, "noite": 1},
        "quinta": {"manha": 0, "tarde": 0, "noite": 0},
        "sexta": {"manha": 0, "tarde": 0, "noite": 0},
        "sábado": {"manha": 1, "tarde": 0, "noite": 1},
        "domingo": {"manha": 1, "tarde": 0, "noite": 0}
    },
    "4": {
        "segunda": {"manha": 1, "tarde": 0, "noite": 0},
        "terça": {"manha": 0, "tarde": 0, "noite": 0},
        "quarta": {"manha": 1, "tarde": 0, "noite": 0},
        "quinta": {"manha": 1, "tarde": 0, "noite": 0},
        "sexta": {"manha": 1, "tarde": 1, "noite": 0},
        "sábado": {"manha": 0, "tarde": 0, "noite": 0},
        "domingo": {"manha": 0, "tarde": 0, "noite": 1}
    },
    "5": {
        "segunda": {"manha": 0, "tarde": 0, "noite": 0},
        "terça": {"manha": 0, "tarde": 0, "noite": 1},
        "quarta": {"manha": 0, "tarde": 0, "noite": 1},
        "quinta": {"manha": 0, "tarde": 1, "noite": 1},
        "sexta": {"manha": 1, "tarde": 1, "noite": 0},
        "sábado": {"manha": 0, "tarde": 0, "noite": 0},
        "domingo": {"manha": 0, "tarde": 0, "noite": 0}
    },
    "6": {
        "segunda": {"manha": 0, "tarde": 0, "noite": 1},
        "terça": {"manha": 1, "tarde": 1, "noite": 1},
        "quarta": {"manha": 1, "tarde": 1, "noite": 0},
        "quinta": {"manha": 1, "tarde": 1, "noite": 1},
        "sexta": {"manha": 0, "tarde": 0, "noite": 1},
        "sábado": {"manha": 0, "tarde": 1, "noite": 1},
        "domingo": {"manha": 0, "tarde": 0, "noite": 0}
    }
}

# 3. Estrutura correta para os endpoints (precisa dos dois campos!)
dados_para_api = {
    "escala": escala,
    "funcionarios": funcionarios
}

print("\n2. Validando a escala...")
response = requests.post(
    f"{BASE_URL}/validar",
    json=dados_para_api,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    validacao = response.json()
    print("✅ Validação realizada com sucesso!")
    print(f"   • Escala válida: {validacao['escala_valida']}")
    print(f"   • Número de violações: {validacao['num_violacoes']}")
    
    if validacao['violacoes']:
        print("   • Violações encontradas:")
        for v in validacao['violacoes']:
            print(f"     - {v}")
    
    print("   • Estatísticas por funcionário:")
    for nome, stats in validacao['estatisticas'].items():
        print(f"     - {nome}: {stats['turnos_totais']} turnos, {stats['folgas']} folgas")
else:
    print(f"❌ Erro na validação: {response.status_code}")
    print(response.text)

print("\n3. Tentando reparar a escala...")
response = requests.post(
    f"{BASE_URL}/reparar",
    json=dados_para_api,
    headers={"Content-Type": "application/json"}
)

if response.status_code == 200:
    reparo = response.json()
    print("✅ Reparo realizado com sucesso!")
    print(f"   • Violações antes: {reparo['violacoes_antes']}")
    print(f"   • Violações depois: {reparo['violacoes_depois']}")
    print(f"   • Melhoria: {reparo['melhoria']} violações corrigidas")
    
    # Salvar escala reparada em arquivo para análise
    with open('escala_reparada.json', 'w') as f:
        json.dump(reparo['escala_reparada'], f, indent=2)
    print("   • Escala reparada salva em 'escala_reparada.json'")
else:
    print(f"❌ Erro no reparo: {response.status_code}")
    print(response.text)

print("\n4. Estrutura JSON correta para usar os endpoints:")
print("""
{
  "escala": {
    "1": { "segunda": {"manha": 0, "tarde": 1, "noite": 0}, ... },
    "2": { "segunda": {"manha": 1, "tarde": 0, "noite": 0}, ... },
    ...
  },
  "funcionarios": [
    {"id": 1, "nome": "Ana", "preferencias_folga": []},
    {"id": 2, "nome": "Bruno", "preferencias_folga": []},
    ...
  ]
}
""")
