"""
Cliente de Exemplo para a API de Otimização de Escalas de Trabalho

Este script demonstra como usar a API para:
1. Otimizar uma escala de trabalho
2. Validar uma escala existente
3. Reparar uma escala com problemas

Para usar: 
1. Instale as dependências: pip install requests
2. Execute a API: python api_escala_trabalho.py
3. Execute este cliente: python cliente_exemplo.py
"""

import requests
import json
from datetime import datetime

# URL base da API (ajuste se necessário)
BASE_URL = "http://localhost:8000"

def testar_api():
    print("🧪 TESTANDO API DE OTIMIZAÇÃO DE ESCALAS DE TRABALHO")
    print("=" * 60)
    
    # 1. TESTE: Obter exemplo de configuração
    print("\n1️⃣ Obtendo configuração de exemplo...")
    try:
        response = requests.get(f"{BASE_URL}/configuracao/exemplo")
        if response.status_code == 200:
            config_exemplo = response.json()
            print("✅ Configuração de exemplo obtida com sucesso!")
        else:
            print(f"❌ Erro ao obter configuração: {response.status_code}")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Erro: API não está rodando. Execute 'python api_escala_trabalho.py' primeiro.")
        return
    
    # 2. TESTE: Otimizar escala
    print("\n2️⃣ Otimizando escala de trabalho...")
    try:
        response = requests.post(
            f"{BASE_URL}/otimizar",
            json=config_exemplo,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print("✅ Otimização concluída!")
            print(f"   • Violações: {resultado['num_violacoes']}")
            print(f"   • Tempo de execução: {resultado['tempo_execucao']:.2f}s")
            print(f"   • Gerações executadas: {len(resultado['evolucao_fitness'])}")
            print(f"   • Fitness final: {resultado['evolucao_fitness'][-1]}")
            
            # Salvar resultado para próximos testes
            escala_otimizada = resultado['escala_otimizada']
            funcionarios = config_exemplo['funcionarios']
            
        else:
            print(f"❌ Erro na otimização: {response.status_code}")
            print(response.text)
            return
            
    except Exception as e:
        print(f"❌ Erro na requisição: {e}")
        return
    
    # 3. TESTE: Validar escala otimizada
    print("\n3️⃣ Validando escala otimizada...")
    try:
        dados_validacao = {
            "escala": escala_otimizada,
            "funcionarios": funcionarios
        }
        
        response = requests.post(
            f"{BASE_URL}/validar",
            json=dados_validacao,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            validacao = response.json()
            print("✅ Validação concluída!")
            print(f"   • Escala válida: {validacao['escala_valida']}")
            print(f"   • Número de violações: {validacao['num_violacoes']}")
            
            if validacao['violacoes']:
                print("   • Violações encontradas:")
                for v in validacao['violacoes'][:3]:  # Mostrar apenas as primeiras 3
                    print(f"     - {v}")
            
            print("   • Estatísticas por funcionário:")
            for nome, stats in validacao['estatisticas'].items():
                print(f"     - {nome}: {stats['turnos_totais']} turnos, {stats['folgas']} folgas")
                
        else:
            print(f"❌ Erro na validação: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro na validação: {e}")
    
    # 4. TESTE: Criar escala com problemas e reparar
    print("\n4️⃣ Testando reparo de escala com violações...")
    try:
        # Criar uma escala problemática (todos trabalham demais)
        escala_problemática = {}
        for func in funcionarios:
            escala_problemática[func['id']] = {}
            for dia in ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]:
                escala_problemática[func['id']][dia] = {}
                for turno in ["manha", "tarde", "noite"]:
                    # Fazer todos trabalharem em todos os turnos (violação!)
                    escala_problemática[func['id']][dia][turno] = 1
        
        dados_reparo = {
            "escala": escala_problemática,
            "funcionarios": funcionarios
        }
        
        response = requests.post(
            f"{BASE_URL}/reparar",
            json=dados_reparo,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            reparo = response.json()
            print("✅ Reparo concluído!")
            print(f"   • Violações antes: {reparo['violacoes_antes']}")
            print(f"   • Violações depois: {reparo['violacoes_depois']}")
            print(f"   • Melhoria: {reparo['melhoria']} violações corrigidas")
            
        else:
            print(f"❌ Erro no reparo: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro no reparo: {e}")
    
    # 5. TESTE: Múltiplas otimizações com parâmetros diferentes
    print("\n5️⃣ Comparando diferentes configurações...")
    try:
        configuracoes = [
            {"nome": "Rápida", "pop_size": 10, "n_geracoes": 20, "usar_reparo": False},
            {"nome": "Equilibrada", "pop_size": 20, "n_geracoes": 50, "usar_reparo": True},
            {"nome": "Intensiva", "pop_size": 40, "n_geracoes": 100, "usar_reparo": True}
        ]
        
        print("   Configuração    | Violações | Tempo  | Gerações")
        print("   --------------- | --------- | ------ | --------")
        
        for config in configuracoes:
            config_teste = config_exemplo.copy()
            config_teste['parametros'] = {
                "pop_size": config['pop_size'],
                "n_geracoes": config['n_geracoes'],
                "taxa_mutacao": 0.2,
                "usar_elitismo": True,
                "usar_reparo": config['usar_reparo']
            }
            
            response = requests.post(
                f"{BASE_URL}/otimizar",
                json=config_teste,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                resultado = response.json()
                print(f"   {config['nome']:<15} | {resultado['num_violacoes']:>9} | {resultado['tempo_execucao']:>5.1f}s | {len(resultado['evolucao_fitness']):>8}")
            
    except Exception as e:
        print(f"❌ Erro no teste comparativo: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 TESTES CONCLUÍDOS!")
    print("\n💡 Para explorar mais:")
    print(f"   • Documentação interativa: {BASE_URL}/docs")
    print(f"   • Dados de exemplo: {BASE_URL}/funcionarios/exemplo")
    print(f"   • Informações da API: {BASE_URL}/")

def exemplo_uso_personalizado():
    """Exemplo de como usar a API com dados personalizados"""
    print("\n" + "="*60)
    print("📝 EXEMPLO DE USO PERSONALIZADO")
    print("="*60)
    
    # Configuração personalizada
    config_personalizada = {
        "funcionarios": [
            {"id": 1, "nome": "João", "preferencias_folga": ["domingo"]},
            {"id": 2, "nome": "Maria", "preferencias_folga": ["sábado"]},
            {"id": 3, "nome": "Pedro", "preferencias_folga": ["segunda"]},
            {"id": 4, "nome": "Ana", "preferencias_folga": ["sexta"]}
        ],
        "carga_max_semanal": 5,  # Carga mais leve
        "folgas_obrigatorias": 2,  # Mais folgas
        "cobertura_minima": 1,     # Cobertura mais flexível
        "parametros": {
            "pop_size": 25,
            "n_geracoes": 75,
            "taxa_mutacao": 0.15,
            "usar_elitismo": True,
            "usar_reparo": True
        }
    }
    
    print("Configuração personalizada:")
    print(f"• {len(config_personalizada['funcionarios'])} funcionários")
    print(f"• Carga máxima: {config_personalizada['carga_max_semanal']} turnos/semana")
    print(f"• Folgas obrigatórias: {config_personalizada['folgas_obrigatorias']}")
    print(f"• Cobertura mínima: {config_personalizada['cobertura_minima']} funcionários/turno")
    
    try:
        response = requests.post(
            f"{BASE_URL}/otimizar",
            json=config_personalizada,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            resultado = response.json()
            print(f"\n✅ Otimização personalizada concluída!")
            print(f"   • Violações: {resultado['num_violacoes']}")
            print(f"   • Tempo: {resultado['tempo_execucao']:.2f}s")
            
            # Mostrar evolução do fitness
            evolucao = resultado['evolucao_fitness']
            print(f"   • Evolução: {evolucao[0]} → {evolucao[-1]} violações")
            
        else:
            print(f"❌ Erro: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    print(f"🕐 Início dos testes: {datetime.now().strftime('%H:%M:%S')}")
    
    # Executar testes principais
    testar_api()
    
    # Executar exemplo personalizado
    exemplo_uso_personalizado()
    
    print(f"\n🕐 Fim dos testes: {datetime.now().strftime('%H:%M:%S')}")
