import requests
import json

def testar_api_limpa():
    print("🧪 Testando API após limpeza...")
    
    # Teste 1: Endpoint /configuracao/exemplo
    print("\n1. Testando /configuracao/exemplo...")
    try:
        response = requests.get('http://localhost:8000/configuracao/exemplo')
        if response.status_code == 200:
            config = response.json()
            print("✅ Endpoint funcionando!")
            print(f"   Parâmetros: {config['parametros']}")
            
            # Teste 2: Endpoint /otimizar
            print("\n2. Testando /otimizar...")
            response = requests.post('http://localhost:8000/otimizar', json=config)
            if response.status_code == 200:
                resultado = response.json()
                print("✅ Otimização funcionando!")
                print(f"   Violações: {resultado['num_violacoes']}")
                print(f"   Tempo: {resultado['tempo_execucao']:.2f}s")
                print(f"   Gerações: {len(resultado['evolucao_fitness'])}")
                
                # Teste 3: Endpoint /validar
                print("\n3. Testando /validar...")
                dados_validacao = {
                    "escala": resultado["escala_otimizada"],
                    "funcionarios": config["funcionarios"]
                }
                response = requests.post('http://localhost:8000/validar', json=dados_validacao)
                if response.status_code == 200:
                    validacao = response.json()
                    print("✅ Validação funcionando!")
                    print(f"   Escala válida: {validacao['escala_valida']}")
                    print(f"   Violações: {validacao['num_violacoes']}")
                else:
                    print(f"❌ Erro na validação: {response.status_code}")
            else:
                print(f"❌ Erro na otimização: {response.status_code}")
                print(response.text)
        else:
            print(f"❌ Erro no exemplo: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("❌ API não está rodando!")
    except Exception as e:
        print(f"❌ Erro: {e}")

    print("\n📊 Resumo da API limpa:")
    print("   • Endpoints ativos: /otimizar, /validar, /configuracao/exemplo")
    print("   • Endpoints removidos: /, /reparar, /funcionarios/exemplo")
    print("   • Parâmetro removido: usar_reparo")
    print("   • Função removida: reparar_individuo")
    print("   • Imports removidos: numpy")

if __name__ == "__main__":
    testar_api_limpa()
