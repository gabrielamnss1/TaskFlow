import sys
from usuarios import cadastrar_usuario, autenticar_usuario, logout, get_usuario_logado
# Variável global para controle do loop principal
EXECUTANDO = True


def menu_principal():
    print("\n--- TaskFlow - Gerenciador de Tarefas ---")
    print("1. Login")
    print("2. Cadastrar Novo Usuário")
    print("3. Sair")
    
    escolha = input("Escolha uma opção: ")
    return escolha

def menu_logado():
    usuario = get_usuario_logado()
    if not usuario:
        return # Não deveria acontecer
        
    print(f"\n--- Menu de {usuario['nome']} ---")
    print("1. Minhas Tarefas")
    print("2. Criar Nova Tarefa")
    print("3. Editar Tarefa")
    print("4. Concluir Tarefa")
    print("5. Excluir Tarefa")
    print("6. Relatórios")
    print("7. Logout")
    
    escolha = input("Escolha uma opção: ")
    return escolha

def tela_cadastro():
    print("\n--- Cadastro de Novo Usuário ---")
    nome = input("Nome completo: ")
    email = input("E-mail: ")
    login = input("Login (será usado para acesso): ")
    senha = input("Senha: ")
    
    if cadastrar_usuario(nome, email, login, senha):
        print("Cadastro realizado. Você pode fazer login agora.")
        
def tela_login():
    print("\n--- Login ---")
    login = input("Login: ")
    senha = input("Senha: ")
    
    autenticar_usuario(login, senha)
    
def tela_criar_tarefa():
    print("\n--- Criar Nova Tarefa ---")
    titulo = input("Título da Tarefa: ")
    descricao = input("Descrição: ")
    prazo = input("Prazo (DD/MM/AAAA): ")
    
    criar_tarefa(titulo, descricao, prazo)
    
def tela_editar_tarefa():
    listar_tarefas()
    print("\n--- Editar Tarefa ---")
    try:
        tarefa_id = int(input("ID da tarefa a editar: "))
    except ValueError:
        print("ID inválido.")
        return
        
    print("Deixe em branco para não alterar o campo.")
    novo_titulo = input("Novo Título: ") or None
    nova_descricao = input("Nova Descrição: ") or None
    novo_prazo = input("Novo Prazo (DD/MM/AAAA): ") or None
    
    editar_tarefa(tarefa_id, novo_titulo, nova_descricao, novo_prazo)