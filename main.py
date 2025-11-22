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