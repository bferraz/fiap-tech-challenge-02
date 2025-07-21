# 🏢 API de Otimização de Escalas de Trabalho

Sistema inteligente para geração e otimização de escalas de trabalho usando **Algoritmos Genéticos** desenvolvido em **Python** com **FastAPI**.

## 🏗️ Estrutura do Projeto

```
api_profissional/
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py          # Configurações da aplicação
│   │   └── constants.py       # Constantes
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Modelos Pydantic
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── escalas.py         # Endpoints de escalas
│   │   └── configuracao.py    # Endpoints de configuração
│   ├── services/
│   │   ├── __init__.py
│   │   └── genetic_algorithm.py  # Serviço do algoritmo genético
│   ├── __init__.py
│   └── main.py                # Aplicação FastAPI
├── tests/
│   └── test_api.py           # Testes automatizados
├── Dockerfile                # Container para produção
├── requirements.txt          # Dependências de produção
├── run.py                    # Executável para desenvolvimento
└── .env.example             # Exemplo de variáveis de ambiente
```

## 🚀 Instalação e Execução

### Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de ambiente
cp .env.example .env

# Executar aplicação
python run.py
```

### Docker

```bash
# Construir e executar com Docker
docker build -t escalas-api .
docker run -p 8000:8000 escalas-api
```

## 📚 Endpoints

### Base URL: `/api/v1`

- **POST** `/otimizar` - Otimiza uma escala de trabalho
- **POST** `/validar` - Valida uma escala existente
- **GET** `/exemplo` - Retorna configuração de exemplo

### Documentação:

- **GET** `/docs` - Documentação Swagger
- **GET** `/redoc` - Documentação ReDoc

## 🧪 Testes

```bash
# Executar testes
pytest tests/
```

## ⚙️ Configurações

Configurações podem ser definidas via variáveis de ambiente ou arquivo `.env`:

```bash
APP_NAME=API de Otimização de Escalas de Trabalho
DEBUG=True
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=INFO
```
