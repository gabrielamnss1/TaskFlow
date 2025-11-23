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
from Tarefas import _carregar_tarefas, STATUS_CONCLUIDA, STATUS_PENDENTE, STATUS_ATRASADA
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


def _formatar_relatorio(titulo, lista_tarefas):
    """
    Formata uma lista de tarefas para exibição ou exportação.
    
    PARÂMETROS:
        titulo (str): Título do relatório
        lista_tarefas (list): Lista de tarefas a formatar
    
    RETORNO:
        str: Relatório formatado em texto, pronto para exibir ou salvar
    
    FORMATAÇÃO:
        - Cabeçalho com título do relatório
        - Cada tarefa com todos os detalhes
        - Separadores visuais entre tarefas
        - Mensagem específica se não houver tarefas
    
    INFORMAÇÕES INCLUÍDAS:
        - ID da tarefa
        - Título e descrição
        - Prazo
        - Status
        - Nome do responsável (buscado por ID)
    """
    if not lista_tarefas:
        return f"--- {titulo} ---\nNenhuma tarefa encontrada."

    relatorio = [f"--- {titulo} ---"]
    for t in lista_tarefas:
        responsavel = get_usuario_por_id(t['responsavel_id'])
        nome_responsavel = responsavel['nome'] if responsavel else "Desconhecido"
        
        relatorio.append(f"ID: {t['id']}")
        relatorio.append(f"Título: {t['titulo']}")
        relatorio.append(f"Descrição: {t['descricao']}")
        relatorio.append(f"Prazo: {t['prazo']}")
        relatorio.append(f"Status: {t['status']}")
        relatorio.append(f"Responsável: {nome_responsavel}")
        relatorio.append("-" * 20)
        
    return "\n".join(relatorio)


def exibir_relatorio(tipo, lista_tarefas):
    """
    Exibe um relatório formatado no console.
    
    PARÂMETROS:
        tipo (str): Nome/tipo do relatório (ex: "Tarefas Concluídas")
        lista_tarefas (list): Lista de tarefas a exibir
    
    EFEITO:
        Imprime o relatório formatado na tela
    
    USO:
        Visualização rápida de relatórios sem necessidade de arquivo
    """
    relatorio_formatado = _formatar_relatorio(tipo, lista_tarefas)
    print("\n" + relatorio_formatado)

def exportar_relatorio(tipo, lista_tarefas):
    """
    Salva um relatório em arquivo de texto (.txt).
    
    PARÂMETROS:
        tipo (str): Nome/tipo do relatório (usado no nome do arquivo)
        lista_tarefas (list): Lista de tarefas a exportar
    
    RETORNO:
        str: Nome do arquivo criado se sucesso
        None: Se houver erro na exportação
    
    NOME DO ARQUIVO:
        Formato: relatorio_[tipo]_[data]_[hora].txt
        Exemplo: relatorio_tarefas_concluídas_20251113_143022.txt
    
    CARACTERÍSTICAS:
        - Encoding UTF-8 (suporta acentos)
        - Timestamp no nome (evita sobrescrever arquivos)
        - Conteúdo idêntico ao exibido no console
    
    USO:
        - Documentação de progresso
        - Compartilhamento de informações
        - Arquivamento de histórico
    """
    relatorio_formatado = _formatar_relatorio(tipo, lista_tarefas)
    nome_arquivo = f"relatorio_{tipo.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write(relatorio_formatado)
        print(f"\nRelatório '{tipo}' exportado com sucesso para o arquivo: {nome_arquivo}")
        return nome_arquivo
    except Exception as e:
        print(f"Erro ao exportar relatório: {e}")
        return None
# Fim do módulo relatorios.py