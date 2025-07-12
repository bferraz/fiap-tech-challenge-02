"""
API para Otimização de Escalas de Trabalho
Baseada no algoritmo genético desenvolvido no notebook escala_trabalho_hands_on.ipynb

Framework: FastAPI
Funcionalidades:
- Gerar escala otimizada usando algoritmo genético
- Validar escalas existentes
- Reparar escalas com violações
- Configurar parâmetros do algoritmo
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import random
import numpy as np
from datetime import datetime

# Inicializar FastAPI
app = FastAPI(
    title="API de Otimização de Escalas de Trabalho",
    description="Sistema inteligente para geração e otimização de escalas usando algoritmos genéticos",
    version="1.0.0"
)

# ================================
# MODELOS DE DADOS (Pydantic)
# ================================

class Funcionario(BaseModel):
    id: int
    nome: str
    preferencias_folga: List[str] = Field(default=[], description="Dias da semana preferidos para folga")

class ParametrosAlgoritmo(BaseModel):
    pop_size: int = Field(default=20, ge=10, le=100, description="Tamanho da população")
    n_geracoes: int = Field(default=80, ge=10, le=200, description="Número de gerações")
    taxa_mutacao: float = Field(default=0.2, ge=0.01, le=1.0, description="Taxa de mutação")
    usar_elitismo: bool = Field(default=False, description="Usar elitismo na evolução")
    usar_reparo: bool = Field(default=False, description="Aplicar reparo automático")

class ConfiguracaoEscala(BaseModel):
    funcionarios: List[Funcionario]
    carga_max_semanal: int = Field(default=6, ge=1, le=21, description="Máximo de turnos por semana")
    folgas_obrigatorias: int = Field(default=1, ge=0, le=7, description="Mínimo de folgas por semana")
    cobertura_minima: int = Field(default=2, ge=1, le=10, description="Mínimo de funcionários por turno")
    parametros: Optional[ParametrosAlgoritmo] = None

class TurnoTrabalho(BaseModel):
    funcionario_id: int
    dia: str
    turno: str

class EscalaCompleta(BaseModel):
    escala: Dict[int, Dict[str, Dict[str, int]]]
    funcionarios: List[Funcionario]

class ResultadoOtimizacao(BaseModel):
    escala_otimizada: Dict[int, Dict[str, Dict[str, int]]]
    num_violacoes: int
    evolucao_fitness: List[int]
    tempo_execucao: float
    parametros_utilizados: ParametrosAlgoritmo

class ValidacaoEscala(BaseModel):
    escala_valida: bool
    num_violacoes: int
    violacoes: List[str]
    estatisticas: Dict[str, Any]

# ================================
# CONSTANTES E CONFIGURAÇÕES
# ================================

DIAS_SEMANA = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
TURNOS = ["manha", "tarde", "noite"]

# ================================
# ALGORITMO GENÉTICO (Core Logic)
# ================================

class EscalaGenetica:
    """
    Implementação EXATA das 4 primeiras células do notebook.
    SEM reparo automático na otimização principal.
    """
    def __init__(self, config: ConfiguracaoEscala):
        self.funcionarios = config.funcionarios
        self.carga_max_semanal = config.carga_max_semanal
        self.folgas_obrigatorias = config.folgas_obrigatorias
        self.cobertura_minima = config.cobertura_minima
        
        # Parâmetros do algoritmo (valores padrão do notebook)
        if config.parametros:
            self.params = config.parametros
        else:
            self.params = ParametrosAlgoritmo()

    def checar_restricoes(self, escala: Dict) -> List[str]:
        """Verifica todas as restrições da escala - EXATA DO NOTEBOOK"""
        violacoes = []
        
        # 1. Carga horária máxima e folgas obrigatórias
        for f in self.funcionarios:
            total_turnos = sum(escala[f.id][dia][turno] for dia in DIAS_SEMANA for turno in TURNOS)
            folgas = sum(all(escala[f.id][dia][t] == 0 for t in TURNOS) for dia in DIAS_SEMANA)
            
            if total_turnos > self.carga_max_semanal:
                violacoes.append(f"{f.nome} excedeu carga máxima semanal.")
            
            if folgas < self.folgas_obrigatorias:
                violacoes.append(f"{f.nome} não tem folgas suficientes.")
        
        # 2. Cobertura mínima por turno
        for dia in DIAS_SEMANA:
            for turno in TURNOS:
                trabalhando = sum(escala[f.id][dia][turno] for f in self.funcionarios)
                if trabalhando < self.cobertura_minima:
                    violacoes.append(f"Cobertura insuficiente em {dia} {turno}.")
        
        return violacoes

    def avaliar_individuo(self, individuo: Dict) -> int:
        """Avaliação do indivíduo (número de violações) - EXATA DO NOTEBOOK"""
        violacoes = self.checar_restricoes(individuo)
        return len(violacoes)

    def gerar_individuo(self) -> Dict:
        """Geração de individuo aleatório (escala de trabalho) - EXATA DO NOTEBOOK"""
        escala = {f.id: {dia: {turno: 0 for turno in TURNOS} for dia in DIAS_SEMANA} for f in self.funcionarios}
        
        for f in self.funcionarios:
            dias_trabalhados = random.sample(DIAS_SEMANA, self.carga_max_semanal)
            for dia in dias_trabalhados:
                turno = random.choice(TURNOS)
                escala[f.id][dia][turno] = 1
        
        return escala

    def selecionar_pais(self, populacao: List[Dict]) -> List[Dict]:
        """Seleção de pais (torneio) - EXATA DO NOTEBOOK"""
        pais = []
        for _ in range(2):
            torneio = random.sample(populacao, 3)
            melhor = min(torneio, key=lambda ind: self.avaliar_individuo(ind))
            pais.append(melhor)
        return pais

    def cruzar_pais(self, pai1: Dict, pai2: Dict) -> Dict:
        """Cruzamento de pais - EXATA DO NOTEBOOK (Versão refatorada)"""
        filho = {}
        
        for funcionario_id in pai1.keys():
            filho[funcionario_id] = {}
            
            for dia in pai1[funcionario_id].keys():
                filho[funcionario_id][dia] = {}
                
                for turno in pai1[funcionario_id][dia].keys():
                    # Escolha aleatória entre os pais
                    pai_escolhido = pai1 if random.random() < 0.5 else pai2
                    filho[funcionario_id][dia][turno] = pai_escolhido[funcionario_id][dia][turno]
        
        return filho

    def mutar_individuo(self, individuo: Dict) -> Dict:
        """Mutação do indivíduo - EXATA DO NOTEBOOK"""
        for f in self.funcionarios:
            if random.random() < self.params.taxa_mutacao:
                dia = random.choice(DIAS_SEMANA)
                turno = random.choice(TURNOS)
                if individuo[f.id][dia][turno] == 1:
                    individuo[f.id][dia][turno] = 0  # Remove o turno
                else:
                    individuo[f.id][dia][turno] = 1  # Adiciona o turno
        return individuo

    def reparar_individuo(self, individuo: Dict) -> Dict:
        """Função de reparo separada (não usada na otimização principal)"""
        reparado = {f.id: {dia: {turno: individuo[f.id][dia][turno] 
                                for turno in TURNOS} for dia in DIAS_SEMANA} for f in self.funcionarios}
        
        for f in self.funcionarios:
            turnos_ocupados = [(dia, turno) for dia in DIAS_SEMANA for turno in TURNOS 
                              if reparado[f.id][dia][turno] == 1]
            
            # Remover excesso
            if len(turnos_ocupados) > self.carga_max_semanal:
                excesso = len(turnos_ocupados) - self.carga_max_semanal
                turnos_para_remover = random.sample(turnos_ocupados, excesso)
                for dia, turno in turnos_para_remover:
                    reparado[f.id][dia][turno] = 0
            
            # Adicionar se necessário
            elif len(turnos_ocupados) < self.carga_max_semanal:
                turnos_livres = [(dia, turno) for dia in DIAS_SEMANA for turno in TURNOS 
                                if reparado[f.id][dia][turno] == 0]
                if turnos_livres:
                    faltam = min(self.carga_max_semanal - len(turnos_ocupados), len(turnos_livres))
                    turnos_para_adicionar = random.sample(turnos_livres, faltam)
                    for dia, turno in turnos_para_adicionar:
                        reparado[f.id][dia][turno] = 1
        
        return reparado

    def otimizar(self) -> tuple:
        """Executa o algoritmo genético completo - LÓGICA EXATA DO NOTEBOOK"""
        import time
        inicio = time.time()
        
        # Inicialização da população - SEM reparo automático
        populacao = [self.gerar_individuo() for _ in range(self.params.pop_size)]
        
        # Evolução da população
        melhores_geracoes = []
        evolucao_fitness = []
        
        for geracao in range(self.params.n_geracoes):
            nova_populacao = []
            
            # Avaliar e ordenar a população
            populacao_ordenada = sorted(populacao, key=lambda ind: self.avaliar_individuo(ind), reverse=False)
            
            # Manter o melhor indivíduo se elitismo for usado
            if self.params.usar_elitismo:
                nova_populacao.append(populacao_ordenada[0])
            
            # Seleção e cruzamento
            while len(nova_populacao) < self.params.pop_size:
                pai1, pai2 = self.selecionar_pais(populacao_ordenada)
                filho = self.cruzar_pais(pai1, pai2)
                filho = self.mutar_individuo(filho)
                nova_populacao.append(filho)
            
            populacao = nova_populacao
            melhores_geracoes.append(populacao_ordenada[0])
            
            # Adicionar fitness da geração atual
            melhor_fitness = self.avaliar_individuo(populacao_ordenada[0])
            evolucao_fitness.append(melhor_fitness)
        
        # Avaliação da melhor escala encontrada
        melhor_individuo = min(melhores_geracoes, key=lambda ind: self.avaliar_individuo(ind))
        tempo_execucao = time.time() - inicio
        
        return melhor_individuo, evolucao_fitness, tempo_execucao

# ================================
# ENDPOINTS DA API
# ================================

@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "nome": "API de Otimização de Escalas de Trabalho",
        "versao": "1.0.0",
        "descricao": "Sistema inteligente para geração e otimização de escalas usando algoritmos genéticos",
        "endpoints": {
            "/otimizar": "Gerar escala otimizada",
            "/validar": "Validar escala existente",
            "/reparar": "Reparar escala com violações",
            "/docs": "Documentação interativa (Swagger)"
        }
    }

@app.post("/otimizar", response_model=ResultadoOtimizacao)
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
            raise HTTPException(status_code=400, detail="Lista de funcionários não pode estar vazia")
        
        if config.carga_max_semanal > len(DIAS_SEMANA) * len(TURNOS):
            raise HTTPException(status_code=400, detail="Carga máxima semanal excede turnos disponíveis")
        
        # Executar otimização
        algoritmo = EscalaGenetica(config)
        escala_otimizada, evolucao, tempo = algoritmo.otimizar()
        
        # Avaliar resultado final
        num_violacoes = algoritmo.avaliar_individuo(escala_otimizada)
        
        return ResultadoOtimizacao(
            escala_otimizada=escala_otimizada,
            num_violacoes=num_violacoes,
            evolucao_fitness=evolucao,
            tempo_execucao=tempo,
            parametros_utilizados=algoritmo.params
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na otimização: {str(e)}")

@app.post("/validar", response_model=ValidacaoEscala)
async def validar_escala(dados: EscalaCompleta):
    """
    Valida uma escala existente verificando todas as restrições
    
    - **escala**: Escala completa para validação
    - **funcionarios**: Lista de funcionários correspondente
    """
    try:
        # Criar configuração temporária para validação
        config_temp = ConfiguracaoEscala(funcionarios=dados.funcionarios)
        algoritmo = EscalaGenetica(config_temp)
        
        # Verificar violações
        violacoes = algoritmo.checar_restricoes(dados.escala)
        
        # Calcular estatísticas
        estatisticas = {}
        for f in dados.funcionarios:
            total_turnos = sum(dados.escala[f.id][dia][turno] 
                             for dia in DIAS_SEMANA for turno in TURNOS)
            folgas = sum(all(dados.escala[f.id][dia][t] == 0 for t in TURNOS) 
                        for dia in DIAS_SEMANA)
            estatisticas[f.nome] = {
                "turnos_totais": total_turnos,
                "folgas": folgas,
                "carga_percentual": (total_turnos / len(DIAS_SEMANA) / len(TURNOS)) * 100
            }
        
        return ValidacaoEscala(
            escala_valida=len(violacoes) == 0,
            num_violacoes=len(violacoes),
            violacoes=violacoes,
            estatisticas=estatisticas
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na validação: {str(e)}")

@app.post("/reparar")
async def reparar_escala(dados: EscalaCompleta):
    """
    Repara uma escala com violações aplicando correções automáticas
    
    - **escala**: Escala com possíveis violações
    - **funcionarios**: Lista de funcionários correspondente
    """
    try:
        # Criar configuração temporária
        config_temp = ConfiguracaoEscala(funcionarios=dados.funcionarios)
        algoritmo = EscalaGenetica(config_temp)
        
        # Aplicar reparo
        escala_reparada = algoritmo.reparar_individuo(dados.escala)
        
        # Validar resultado
        violacoes_antes = len(algoritmo.checar_restricoes(dados.escala))
        violacoes_depois = len(algoritmo.checar_restricoes(escala_reparada))
        
        return {
            "escala_original": dados.escala,
            "escala_reparada": escala_reparada,
            "violacoes_antes": violacoes_antes,
            "violacoes_depois": violacoes_depois,
            "melhoria": violacoes_antes - violacoes_depois
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no reparo: {str(e)}")

@app.get("/funcionarios/exemplo")
async def exemplo_funcionarios():
    """Retorna um exemplo de lista de funcionários para testes"""
    return {
        "funcionarios": [
            {"id": 1, "nome": "Ana", "preferencias_folga": ["domingo"]},
            {"id": 2, "nome": "Bruno", "preferencias_folga": ["sábado"]},
            {"id": 3, "nome": "Carla", "preferencias_folga": ["segunda"]},
            {"id": 4, "nome": "Diego", "preferencias_folga": ["terça"]},
            {"id": 5, "nome": "Elisa", "preferencias_folga": ["quarta"]},
            {"id": 6, "nome": "Felipe", "preferencias_folga": ["sexta"]}
        ]
    }

@app.get("/configuracao/exemplo")
async def exemplo_configuracao():
    """Retorna um exemplo completo de configuração para otimização"""
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
            "usar_elitismo": True,
            "usar_reparo": True
        }
    }

# ================================
# INICIALIZAÇÃO
# ================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Iniciando API de Otimização de Escalas de Trabalho...")
    print("📖 Documentação disponível em: http://localhost:8000/docs")
    print("🔗 API disponível em: http://localhost:8000")
    uvicorn.run("api_escala_trabalho:app", host="0.0.0.0", port=8000, reload=True)
