from datetime import datetime
from utils.arquivos import ler_dados, salvar_dados, ARQUIVO_TAREFAS
from usuarios import get_usuario_logado

# Constantes para Status da Tarefa (evita erros de digitação)
STATUS_PENDENTE = "Pendente"
STATUS_CONCLUIDA = "Concluída"
STATUS_ATRASADA = "Atrasada"


def _carregar_tarefas():
    """
    Carrega a lista de todas as tarefas do arquivo JSON.
    
    RETORNO:
        list: Lista de dicionários com todas as tarefas do sistema
    """
    return ler_dados(ARQUIVO_TAREFAS)

def _salvar_tarefas(tarefas):
    """
    Salva a lista completa de tarefas no arquivo JSON.
    
    PARÂMETROS:
        tarefas (list): Lista completa de tarefas a ser salva
    
    RETORNO:
        bool: True se salvou com sucesso, False caso contrário
    """
    return salvar_dados(ARQUIVO_TAREFAS, tarefas)