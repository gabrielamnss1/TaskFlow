
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


def criar_tarefa(titulo, descricao, prazo_str):
    """
    Cria uma nova tarefa no sistema (CREATE do CRUD).
    
    PARÂMETROS:
        titulo (str): Título resumido da tarefa
        descricao (str): Descrição detalhada do que deve ser feito
        prazo_str (str): Data limite no formato DD/MM/AAAA
    
    RETORNO:
        bool: True se criou com sucesso, False se houve erro
    
    PROCESSO:
        1. Valida se há usuário logado (responsável)
        2. Valida o formato da data do prazo
        3. Gera ID único auto-incrementado
        4. Cria registro com todos os dados
        5. Salva no arquivo JSON
    
    ESTRUTURA DA TAREFA:
        - id: Identificador único
        - titulo: Nome da tarefa
        - descricao: Detalhes
        - responsavel_id: ID do usuário que criou
        - responsavel_nome: Nome do usuário (facilitação)
        - prazo: Data limite (DD/MM/AAAA)
        - status: Sempre inicia como "Pendente"
        - criacao: Data/hora da criação (timestamp)
    """
    usuario = get_usuario_logado()
    if not usuario:
        print("Erro: Nenhum usuário logado para criar a tarefa.")
        return False

    try:
        # Validação básica do formato da data
        prazo = datetime.strptime(prazo_str, '%d/%m/%Y').strftime('%d/%m/%Y')
    except ValueError:
        print("Erro: Formato de prazo inválido. Use DD/MM/AAAA.")
        return False

