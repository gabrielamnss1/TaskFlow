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


def exibir_relatorio(titulo, lista_tarefas):
    """
    Exibe um relatório formatado no console.
    
    PARÂMETROS:
        titulo (str): Título do relatório
        lista_tarefas (list): Lista de tarefas a exibir
    
    FORMATAÇÃO:
        - Cabeçalho com título
        - Cada tarefa em uma linha formatada
        - Rodapé com contagem total
    """
    print(f"\n--- {titulo} ---")
    
    if not lista_tarefas:
        print("Nenhuma tarefa encontrada.")
        return
    
    for tarefa in lista_tarefas:
        print(f"ID: {tarefa['id']} | Título: {tarefa['titulo']} | "
              f"Prazo: {tarefa['prazo']} | Status: {tarefa['status']} | "
              f"Responsável: {tarefa['responsavel_nome']}")
    
    print(f"\nTotal: {len(lista_tarefas)} tarefa(s)")


def exportar_relatorio(titulo, lista_tarefas):
    """
    Exporta um relatório para arquivo TXT.
    
    PARÂMETROS:
        titulo (str): Título do relatório
        lista_tarefas (list): Lista de tarefas a exportar
    
    FORMATO:
        - Nome: relatorio_<timestamp>.txt
        - Encoding: UTF-8
        - Localização: raiz do projeto
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"relatorio_{timestamp}.txt"
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(f"{titulo}\n")
            f.write("=" * 80 + "\n")
            f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            if not lista_tarefas:
                f.write("Nenhuma tarefa encontrada.\n")
            else:
                for tarefa in lista_tarefas:
                    f.write(f"ID: {tarefa['id']}\n")
                    f.write(f"Título: {tarefa['titulo']}\n")
                    f.write(f"Descrição: {tarefa['descricao']}\n")
                    f.write(f"Prazo: {tarefa['prazo']}\n")
                    f.write(f"Status: {tarefa['status']}\n")
                    f.write(f"Responsável: {tarefa['responsavel_nome']}\n")
                    f.write(f"Criado em: {tarefa['criacao']}\n")
                    f.write("-" * 80 + "\n\n")
                
                f.write(f"Total de tarefas: {len(lista_tarefas)}\n")
        
        print(f"✓ Relatório exportado para: {nome_arquivo}")
        return True
    except Exception as e:
        print(f"✗ Erro ao exportar relatório: {e}")
        return False
