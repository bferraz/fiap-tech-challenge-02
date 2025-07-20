"""
Serviço do algoritmo genético para otimização de escalas
"""

import random
import time
from typing import Dict, List, Tuple

from app.core.constants import DIAS_SEMANA, TURNOS
from app.models.schemas import ConfiguracaoEscala, ParametrosAlgoritmo


class EscalaGeneticaService:
    """
    Serviço para otimização de escalas usando algoritmos genéticos.
    """
    
    def __init__(self, config: ConfiguracaoEscala):
        self.funcionarios = config.funcionarios
        self.carga_max_semanal = config.carga_max_semanal
        self.folgas_obrigatorias = config.folgas_obrigatorias
        self.cobertura_minima = config.cobertura_minima
        
        # Parâmetros do algoritmo
        if config.parametros:
            self.params = config.parametros
        else:
            self.params = ParametrosAlgoritmo()

    def checar_restricoes(self, escala: Dict) -> List[str]:
        """Verifica todas as restrições da escala"""
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
        """Avaliação do indivíduo (número de violações)"""
        violacoes = self.checar_restricoes(individuo)
        return len(violacoes)

    def gerar_individuo(self) -> Dict:
        """Geração de individuo aleatório (escala de trabalho)"""
        escala = {f.id: {dia: {turno: 0 for turno in TURNOS} for dia in DIAS_SEMANA} for f in self.funcionarios}
        
        for f in self.funcionarios:
            dias_trabalhados = random.sample(DIAS_SEMANA, self.carga_max_semanal)
            for dia in dias_trabalhados:
                turno = random.choice(TURNOS)
                escala[f.id][dia][turno] = 1
        
        return escala

    def selecionar_pais(self, populacao: List[Dict]) -> List[Dict]:
        """Seleção de pais (torneio)"""
        pais = []
        for _ in range(2):
            torneio = random.sample(populacao, 3)
            melhor = min(torneio, key=lambda ind: self.avaliar_individuo(ind))
            pais.append(melhor)
        return pais

    def cruzar_pais(self, pai1: Dict, pai2: Dict) -> Dict:
        """Cruzamento de pais"""
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
        """Mutação do indivíduo"""
        for f in self.funcionarios:
            if random.random() < self.params.taxa_mutacao:
                dia = random.choice(DIAS_SEMANA)
                turno = random.choice(TURNOS)
                if individuo[f.id][dia][turno] == 1:
                    individuo[f.id][dia][turno] = 0  # Remove o turno
                else:
                    individuo[f.id][dia][turno] = 1  # Adiciona o turno
        return individuo

    def otimizar(self) -> Tuple[Dict, List[int], float]:
        """Executa o algoritmo genético completo"""
        inicio = time.time()
        
        # Inicialização da população
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

    def calcular_estatisticas(self, escala: Dict) -> Dict:
        """Calcula estatísticas da escala"""
        estatisticas = {}
        
        for f in self.funcionarios:
            total_turnos = sum(escala[f.id][dia][turno] 
                             for dia in DIAS_SEMANA for turno in TURNOS)
            folgas = sum(all(escala[f.id][dia][t] == 0 for t in TURNOS) 
                        for dia in DIAS_SEMANA)
            
            estatisticas[f.nome] = {
                "turnos_totais": total_turnos,
                "folgas": folgas,
                "carga_percentual": (total_turnos / (len(DIAS_SEMANA) * len(TURNOS))) * 100
            }
        
        return estatisticas
