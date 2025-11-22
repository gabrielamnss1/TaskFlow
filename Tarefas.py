"""
================================================================================
MÓDULO: tarefas.py
================================================================================
DESCRIÇÃO:
    Módulo responsável pelo GERENCIAMENTO DE TAREFAS (CRUD completo).
    Implementa todas as operações de Criação, Leitura, Atualização e
    Exclusão de tarefas do sistema.

FUNCIONALIDADES PRINCIPAIS:
    - Criar novas tarefas com prazo e responsável
    - Listar tarefas (todas ou filtradas por usuário)
    - Editar informações de tarefas existentes
    - Marcar tarefas como concluídas
    - Excluir tarefas
    - Verificação automática de tarefas atrasadas

STATUS DE TAREFAS:
    - Pendente: Tarefa criada, aguardando conclusão
    - Concluída: Tarefa finalizada pelo responsável
    - Atrasada: Tarefa pendente com prazo vencido (calculado dinamicamente)

REGRAS DE NEGÓCIO:
    - Apenas o responsável pode editar/concluir/excluir suas tarefas
    - Datas devem estar no formato DD/MM/AAAA
    - Cada tarefa possui ID único auto-incrementado
    - Registro automático de data/hora de criação

IMPORTANTE PARA APRESENTAÇÃO:
    Este módulo demonstra o padrão CRUD (Create, Read, Update, Delete),
    fundamental em qualquer sistema de gerenciamento de dados.
================================================================================
"""

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

    tarefas = _carregar_tarefas()
    
    nova_tarefa = {
        'id': len(tarefas) + 1,
        'titulo': titulo,
        'descricao': descricao,
        'responsavel_id': usuario['id'],
        'responsavel_nome': usuario['nome'],
        'prazo': prazo,
        'status': STATUS_PENDENTE,
        'criacao': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    }
    
    tarefas.append(nova_tarefa)
    if _salvar_tarefas(tarefas):
        print(f"Tarefa '{titulo}' criada com sucesso! ID: {nova_tarefa['id']}")
        return True
    return False


def listar_tarefas(filtrar_por_responsavel=True):
    """
    Lista tarefas do sistema (READ do CRUD).
    
    PARÂMETROS:
        filtrar_por_responsavel (bool): Se True, mostra apenas tarefas do usuário logado
                                       Se False, mostra todas as tarefas
    
    RETORNO:
        list: Lista de tarefas filtradas
    
    FUNCIONALIDADES:
        - Filtragem por responsável (cada usuário vê suas tarefas)
        - Detecção automática de tarefas atrasadas
        - Exibição formatada com ID, título, prazo, status e responsável
    
    LÓGICA DE STATUS ATRASADA:
        - Verifica se o prazo já passou (comparado com data atual)
        - Altera o status visualmente (não modifica o arquivo)
        - Apenas tarefas "Pendente" podem aparecer como "Atrasada"
    """
    tarefas = _carregar_tarefas()
    usuario = get_usuario_logado()
    
    if filtrar_por_responsavel and usuario:
        tarefas_filtradas = [t for t in tarefas if t['responsavel_id'] == usuario['id']]
    else:
        tarefas_filtradas = tarefas
        
    if not tarefas_filtradas:
        print("Nenhuma tarefa encontrada.")
        return []
        
    print("\n--- Lista de Tarefas ---")
    for t in tarefas_filtradas:
        # Verifica se a tarefa está atrasada
        status = t['status']
        if status == STATUS_PENDENTE:
            try:
                prazo_dt = datetime.strptime(t['prazo'], '%d/%m/%Y')
                if prazo_dt < datetime.now().replace(hour=0, minute=0, second=0, microsecond=0):
                    status = STATUS_ATRASADA
            except ValueError:
                pass # Ignora se o formato da data estiver errado
        
        print(f"ID: {t['id']} | Título: {t['titulo']} | Prazo: {t['prazo']} | Status: {status} | Responsável: {t['responsavel_nome']}")
