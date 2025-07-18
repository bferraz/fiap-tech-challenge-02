# 🏢 API de Otimização de Escalas de Trabalho

Sistema inteligente para geração e otimização de escalas de trabalho usando **Algoritmos Genéticos** desenvolvido em **Python** com **FastAPI**.

## 🎯 Funcionalidades

- 🧬 **Otimização Inteligente**: Gera escalas otimizadas usando algoritmos genéticos
- ✅ **Validação de Escalas**: Verifica se uma escala atende todas as restrições
- ⚙️ **Configuração Flexível**: Parâmetros ajustáveis para diferentes cenários
- 📖 **Documentação Automática**: Interface Swagger gerada automaticamente
- 🚀 **Alta Performance**: Otimizado para processar escalas complexas rapidamente

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **FastAPI**: Framework web moderno e rápido
- **Pydantic**: Validação de dados e serialização
- **Uvicorn**: Servidor ASGI de alta performance

## 📋 Restrições Suportadas

1. **Carga Horária Máxima**: Limite de turnos por funcionário por semana
2. **Folgas Obrigatórias**: Mínimo de dias de folga por funcionário
3. **Cobertura Mínima**: Número mínimo de funcionários por turno
4. **Preferências de Folga**: Dias preferenciais de cada funcionário

## 🚀 Instalação e Execução

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar a API

```bash
python api_escala_trabalho.py
```

A API estará disponível em: `http://localhost:8000`

### 3. Acessar Documentação

Abra no navegador: `http://localhost:8000/docs`

## 📚 Endpoints Principais

### 🎯 POST `/otimizar`
Gera uma escala otimizada usando algoritmo genético.

**Exemplo de Requisição:**
```json
{
  "funcionarios": [
    {"id": 1, "nome": "Ana", "preferencias_folga": ["domingo"]},
    {"id": 2, "nome": "Bruno", "preferencias_folga": ["sábado"]}
  ],
  "carga_max_semanal": 6,
  "folgas_obrigatorias": 1,
  "cobertura_minima": 2,
  "parametros": {
    "pop_size": 30,
    "n_geracoes": 100,
    "taxa_mutacao": 0.2,
    "usar_elitismo": true
  }
}
```

### ✅ POST `/validar`
Valida uma escala existente e retorna violações encontradas.

### ⚙️ GET `/configuracao/exemplo`
Retorna uma configuração completa de exemplo.

## 🧪 Testando a API

Execute o cliente de exemplo:

```bash
python cliente_exemplo.py
```

Este script demonstra:
- Como otimizar uma escala
- Como validar uma escala existente
- Como reparar escalas problemáticas
- Comparação entre diferentes configurações

## 📊 Parâmetros do Algoritmo Genético

| Parâmetro | Descrição | Padrão | Faixa |
|-----------|-----------|--------|-------|
| `pop_size` | Tamanho da população | 20 | 10-100 |
| `n_geracoes` | Número de gerações | 50 | 10-200 |
| `taxa_mutacao` | Taxa de mutação | 0.2 | 0.01-1.0 |
| `usar_elitismo` | Preservar melhor indivíduo | true | true/false |
| `usar_reparo` | Aplicar reparo automático | true | true/false |

## 🎛️ Configurações de Restrições

| Parâmetro | Descrição | Padrão | Faixa |
|-----------|-----------|--------|-------|
| `carga_max_semanal` | Máximo de turnos por semana | 6 | 1-21 |
| `folgas_obrigatorias` | Mínimo de folgas por semana | 1 | 0-7 |
| `cobertura_minima` | Mínimo de funcionários por turno | 2 | 1-10 |

## 💡 Exemplos de Uso

### Otimização Básica
```python
import requests

config = {
    "funcionarios": [
        {"id": 1, "nome": "João", "preferencias_folga": ["domingo"]},
        {"id": 2, "nome": "Maria", "preferencias_folga": ["sábado"]}
    ],
    "carga_max_semanal": 5,
    "folgas_obrigatorias": 2,
    "cobertura_minima": 1
}

response = requests.post("http://localhost:8000/otimizar", json=config)
resultado = response.json()

print(f"Violações: {resultado['num_violacoes']}")
print(f"Tempo: {resultado['tempo_execucao']:.2f}s")
```

### Validação de Escala
```python
dados = {
    "escala": escala_para_validar,
    "funcionarios": lista_funcionarios
}

response = requests.post("http://localhost:8000/validar", json=dados)
validacao = response.json()

print(f"Escala válida: {validacao['escala_valida']}")
if validacao['violacoes']:
    for violacao in validacao['violacoes']:
        print(f"- {violacao}")
```

## 🎨 Interface Web (Opcional)

Para uma interface gráfica, acesse a documentação interativa do Swagger em:
`http://localhost:8000/docs`

Esta interface permite:
- ✨ Testar todos os endpoints visualmente
- 📋 Ver exemplos de requisições e respostas
- 🔍 Explorar modelos de dados
- 🧪 Executar testes direto no navegador

## 📈 Performance

A API foi otimizada para:
- ⚡ Processar escalas com até 20 funcionários em menos de 2 segundos
- 🧬 Convergir para soluções válidas em 80%+ dos casos
- 🔄 Executar múltiplas otimizações simultaneamente
- 💾 Usar memória eficientemente

## 🔧 Personalização

### Adicionando Novas Restrições

1. Edite a função `checar_restricoes()` na classe `EscalaGenetica`
2. Adicione validação no modelo `ConfiguracaoEscala`
3. Atualize a documentação

### Modificando Algoritmo Genético

- **Seleção**: Modifique `selecionar_pais()`
- **Cruzamento**: Ajuste `cruzar_pais()`
- **Mutação**: Customize `mutar_individuo()`
- **Reparo**: Melhore `reparar_individuo()`

## 🐛 Solução de Problemas

### API não inicia
```bash
# Verificar se todas as dependências estão instaladas
pip install -r requirements.txt

# Verificar se a porta 8000 está livre
netstat -ano | findstr :8000
```

### Erro de validação
- Verifique se os IDs dos funcionários são únicos
- Confirme que todos os parâmetros estão dentro das faixas válidas
- Use os endpoints de exemplo para testar

### Performance baixa
- Reduza `pop_size` e `n_geracoes` para testes
- Ative `usar_reparo` para convergência mais rápida
- Use `usar_elitismo` para preservar boas soluções

## 📝 Logs e Monitoramento

A API registra automaticamente:
- 📊 Tempo de execução de cada otimização
- 🔢 Número de violações encontradas
- ⚙️ Parâmetros utilizados
- 🚨 Erros e exceções

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙋‍♂️ Suporte

Para dúvidas ou problemas:
1. Consulte a documentação interativa: `/docs`
2. Execute o cliente de exemplo: `cliente_exemplo.py`
3. Verifique os logs da API
4. Abra uma issue no repositório

---

**Desenvolvido com ❤️ usando Algoritmos Genéticos e FastAPI**
