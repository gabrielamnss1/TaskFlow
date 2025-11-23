"""
================================================================================
MÓDULO: relatorios.py
================================================================================
DESCRIÇÃO:
    Módulo responsável pela GERAÇÃO E EXPORTAÇÃO DE RELATÓRIOS.
    Fornece análises e visualizações das tarefas do sistema através
    de filtros específicos.

FUNCIONALIDADES PRINCIPAIS:
    - Filtrar tarefas por status (Concluídas, Pendentes, Atrasadas)
    - Exibir relatórios formatados no console
    - Exportar relatórios para arquivos TXT
    - Cálculo automático de tarefas atrasadas

TIPOS DE RELATÓRIOS:
    1. Tarefas Concluídas: Todas as tarefas finalizadas
    2. Tarefas Pendentes: Tarefas ainda não concluídas
    3. Tarefas Atrasadas: Tarefas pendentes com prazo vencido

FORMATO DE EXPORTAÇÃO:
    - Arquivos TXT com encoding UTF-8
    - Nome com timestamp (evita sobrescrever)
    - Inclui todos os detalhes da tarefa
    - Informações do responsável

IMPORTANTE PARA APRESENTAÇÃO:
    Este módulo demonstra análise de dados e geração de relatórios,
    funcionalidades essenciais para tomada de decisões gerenciais.
================================================================================
"""

from datetime import datetime
from tarefas import _carregar_tarefas, STATUS_CONCLUIDA, STATUS_PENDENTE, STATUS_ATRASADA
from usuarios import get_usuario_por_id


def _filtrar_tarefas(status_desejado=None, verificar_atraso=False):
    """
    Função auxiliar para filtrar tarefas por critérios específicos.
    
    PARÂMETROS:
        status_desejado (str, opcional): Status para filtrar ("Concluída" ou "Pendente")
        verificar_atraso (bool): Se True, retorna apenas tarefas atrasadas
    
    RETORNO:
        list: Lista de tarefas que atendem aos critérios
    
    LÓGICA DE ATRASO:
        - Compara prazo da tarefa com data atual
        - Considera apenas tarefas com status "Pendente"
        - Ignora tarefas com formato de data inválido
        - Usa hora 00:00:00 para comparação (apenas a data)
    
    USO:
        Centraliza a lógica de filtragem para evitar duplicação
        nas funções de relatório.
    """
    tarefas = _carregar_tarefas()
    
    if verificar_atraso:
        hoje = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        tarefas_filtradas = []
        for t in tarefas:
            if t['status'] == STATUS_PENDENTE:
                try:
                    prazo_dt = datetime.strptime(t['prazo'], '%d/%m/%Y')
                    if prazo_dt < hoje:
                        tarefas_filtradas.append(t)
                except ValueError:
                    # Ignora tarefas com formato de data inválido
                    pass
        return tarefas_filtradas
        
    if status_desejado:
        return [t for t in tarefas if t['status'] == status_desejado]
        
    return tarefas


def tarefas_concluidas():
    """
    Retorna todas as tarefas com status 'Concluída'.
    
    RETORNO:
        list: Lista de tarefas concluídas
    
    USO:
        - Relatório de produtividade
        - Histórico de tarefas finalizadas
        - Análise de desempenho
    """
    return _filtrar_tarefas(STATUS_CONCLUIDA)

def tarefas_pendentes():
    """
    Retorna todas as tarefas com status 'Pendente'.
    
    RETORNO:
        list: Lista de tarefas pendentes (não atrasadas)
    
    USO:
        - Visualizar trabalho a fazer
        - Planejamento de atividades
        - Gestão de prioridades
    """
    return _filtrar_tarefas(STATUS_PENDENTE)

def tarefas_atrasadas():
    """
    Retorna tarefas pendentes cujo prazo já venceu.
    
    RETORNO:
        list: Lista de tarefas atrasadas
    
    CRITÉRIO:
        - Status = "Pendente"
        - Prazo < Data atual
    
    USO:
        - Identificar urgências
        - Alertas de atraso
        - Priorização de tarefas críticas
    """
    return _filtrar_tarefas(verificar_atraso=True)
