import requests
import json

print("Testando múltiplas execuções da API...")
for i in range(5):
    response = requests.get('http://localhost:8000/funcionarios/exemplo')
    config = response.json()
    
    response = requests.post('http://localhost:8000/otimizar', json=config)
    resultado = response.json()
    
    print(f'Teste {i+1}: {resultado["num_violacoes"]} violações (tempo: {resultado["tempo_execucao"]:.2f}s)')
