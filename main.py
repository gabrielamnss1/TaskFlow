"""
================================================================================
MÓDULO: main.py - CONTROLADOR PRINCIPAL DO SISTEMA
================================================================================
DESCRIÇÃO:
    Arquivo principal do TaskFlow. Controla o fluxo da aplicação e
    gerencia a interface de linha de comando (CLI) do sistema.

RESPONSABILIDADES:
    - Exibir menus de navegação (pré-login e pós-login)
    - Coordenar chamadas aos módulos especializados
    - Controlar o loop principal da aplicação
    - Gerenciar tratamento de erros global
    - Orquestrar a experiência do usuário

FLUXO DA APLICAÇÃO:
    1. Menu Principal (não logado):
       - Login
       - Cadastro de novo usuário
       - Sair
    
    2. Menu Logado (após autenticação):
       - Visualizar tarefas
       - Criar/Editar/Concluir/Excluir tarefas
       - Gerar relatórios
       - Logout

ARQUITETURA:
    Este módulo segue o padrão MVC simplificado:
    - View: Funções tela_* (interação com usuário)
    - Controller: menu_* e loop_principal (controle de fluxo)
    - Model: Módulos importados (usuarios, tarefas, relatorios)

IMPORTANTE PARA APRESENTAÇÃO:
    Este é o "maestro" do sistema, que coordena todos os outros
    módulos. Demonstra separação de responsabilidades e organização.
================================================================================
"""

import sys
from usuarios import cadastrar_usuario, autenticar_usuario, logout, get_usuario_logado
from tarefas import criar_tarefa, listar_tarefas, editar_tarefa, concluir_tarefa, excluir_tarefa
from relatorios import tarefas_concluidas, tarefas_pendentes, tarefas_atrasadas, exibir_relatorio, exportar_relatorio

# Variável global para controle do loop principal
EXECUTANDO = True


def menu_principal():
    """
    Exibe o menu principal para usuários NÃO autenticados.
    
    OPÇÕES:
        1. Login - Acessar o sistema
        2. Cadastrar Novo Usuário - Criar conta
        3. Sair - Encerrar aplicação
    
    RETORNO:
        str: Opção escolhida pelo usuário
    """
    print("\n--- TaskFlow - Gerenciador de Tarefas ---")
    print("1. Login")
    print("2. Cadastrar Novo Usuário")
    print("3. Sair")
    
    escolha = input("Escolha uma opção: ")
    return escolha

def menu_logado():
    """
    Exibe o menu para usuários AUTENTICADOS.
    
    PERSONALIZAÇÃO:
        - Mostra nome do usuário logado no cabeçalho
        - Opções específicas para gerenciar tarefas pessoais
    
    OPÇÕES:
        1. Minhas Tarefas - Listar tarefas do usuário
        2. Criar Nova Tarefa - Adicionar tarefa
        3. Editar Tarefa - Modificar informações
        4. Concluir Tarefa - Marcar como finalizada
        5. Excluir Tarefa - Remover tarefa
        6. Relatórios - Visualizar análises
        7. Logout - Sair da conta
    
    RETORNO:
        str: Opção escolhida pelo usuário
    """
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
    """
    Interface para cadastro de novo usuário.
    
    COLETA DE DADOS:
        - Nome completo
        - E-mail
        - Login (único no sistema)
        - Senha (será criptografada)
    
    DELEGAÇÃO:
        Chama a função cadastrar_usuario() do módulo usuarios.py
    """
    print("\n--- Cadastro de Novo Usuário ---")
    nome = input("Nome completo: ")
    email = input("E-mail: ")
    login = input("Login (será usado para acesso): ")
    senha = input("Senha: ")
    
    if cadastrar_usuario(nome, email, login, senha):
        print("Cadastro realizado. Você pode fazer login agora.")

def tela_login():
    """
    Interface para login no sistema.
    
    COLETA DE DADOS:
        - Login
        - Senha
    
    DELEGAÇÃO:
        Chama a função autenticar_usuario() do módulo usuarios.py
        Se autenticado com sucesso, o usuário fica logado
    """
    print("\n--- Login ---")
    login = input("Login: ")
    senha = input("Senha: ")
    
    autenticar_usuario(login, senha)


def tela_criar_tarefa():
    """
    Interface para criar uma nova tarefa.
    
    COLETA DE DADOS:
        - Título da tarefa
        - Descrição detalhada
        - Prazo (formato DD/MM/AAAA)
    
    DELEGAÇÃO:
        Chama a função criar_tarefa() do módulo tarefas.py
        O responsável é automaticamente o usuário logado
    """
    print("\n--- Criar Nova Tarefa ---")
    titulo = input("Título da Tarefa: ")
    descricao = input("Descrição: ")
    prazo = input("Prazo (DD/MM/AAAA): ")
    
    criar_tarefa(titulo, descricao, prazo)

def tela_editar_tarefa():
    """
    Interface para editar uma tarefa existente.
    
    PROCESSO:
        1. Lista tarefas do usuário
        2. Solicita ID da tarefa a editar
        3. Coleta novos valores (campos em branco não são alterados)
        4. Delega para editar_tarefa() do módulo tarefas.py
    
    VALIDAÇÃO:
        - ID deve ser numérico
        - Campos vazios mantêm valor original
    """
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

def tela_concluir_tarefa():
    """
    Interface para marcar uma tarefa como concluída.
    
    PROCESSO:
        1. Lista tarefas do usuário
        2. Solicita ID da tarefa
        3. Delega para concluir_tarefa() do módulo tarefas.py
    
    VALIDAÇÃO:
        - ID deve ser numérico
    """
    listar_tarefas()
    print("\n--- Concluir Tarefa ---")
    try:
        tarefa_id = int(input("ID da tarefa a concluir: "))
    except ValueError:
        print("ID inválido.")
        return
        
    concluir_tarefa(tarefa_id)

def tela_excluir_tarefa():
    """
    Interface para excluir uma tarefa.
    
    PROCESSO:
        1. Lista tarefas do usuário
        2. Solicita ID da tarefa
        3. Delega para excluir_tarefa() do módulo tarefas.py
    
    VALIDAÇÃO:
        - ID deve ser numérico
    
    ATENÇÃO:
        Exclusão é permanente (não há confirmação adicional)
    """
    listar_tarefas()
    print("\n--- Excluir Tarefa ---")
    try:
        tarefa_id = int(input("ID da tarefa a excluir: "))
    except ValueError:
        print("ID inválido.")
        return
        
    excluir_tarefa(tarefa_id)


def tela_relatorios():
    """
    Interface para geração e exportação de relatórios.
    
    TIPOS DE RELATÓRIOS DISPONÍVEIS:
        1. Tarefas Concluídas - Histórico de produtividade
        2. Tarefas Pendentes - Trabalho a fazer
        3. Tarefas Atrasadas - Urgências e alertas
    
    FUNCIONALIDADES:
        - Exibição no console
        - Opção de exportar para arquivo TXT
    
    DELEGAÇÃO:
        Usa funções do módulo relatorios.py:
        - tarefas_concluidas(), tarefas_pendentes(), tarefas_atrasadas()
        - exibir_relatorio(), exportar_relatorio()
    """
    print("\n--- Relatórios ---")
    print("1. Tarefas Concluídas")
    print("2. Tarefas Pendentes")
    print("3. Tarefas Atrasadas")
    print("4. Voltar")
    
    escolha = input("Escolha uma opção: ")
    
    if escolha == '1':
        lista = tarefas_concluidas()
        exibir_relatorio("Tarefas Concluídas", lista)
    elif escolha == '2':
        lista = tarefas_pendentes()
        exibir_relatorio("Tarefas Pendentes", lista)
    elif escolha == '3':
        lista = tarefas_atrasadas()
        exibir_relatorio("Tarefas Atrasadas", lista)
    elif escolha == '4':
        return
    else:
        print("Opção inválida.")
        return
        
    if lista:
        exportar = input("Deseja exportar este relatório para um arquivo TXT? (s/n): ").lower()
        if exportar == 's':
            exportar_relatorio(f"Relatório de {escolha}", lista)


def loop_principal():
    """
    LOOP PRINCIPAL DA APLICAÇÃO - CORAÇÃO DO SISTEMA
    
    FUNCIONAMENTO:
        Executa continuamente até o usuário escolher sair.
        Alterna entre dois estados:
        
        1. ESTADO NÃO LOGADO:
           - Exibe menu_principal()
           - Permite: Login, Cadastro ou Sair
        
        2. ESTADO LOGADO:
           - Exibe menu_logado()
           - Permite: Gerenciar tarefas e relatórios
    
    CONTROLE DE FLUXO:
        - Usa variável global EXECUTANDO para controlar o loop
        - Verifica estado de autenticação com get_usuario_logado()
        - Direciona para opção escolhida via estrutura if/elif
    
    TRATAMENTO DE ERROS:
        - Try/except global protege contra crashes
        - Erros são exibidos mas não encerram o programa
        - Usuário pode continuar usando após erro
    
    IMPORTANTE PARA APRESENTAÇÃO:
        Este padrão de "event loop" é comum em aplicações interativas.
        Similar ao que frameworks web fazem em maior escala.
    """
    global EXECUTANDO
    
    while EXECUTANDO:
        try:
            if get_usuario_logado():
                escolha = menu_logado()
                
                if escolha == '1':
                    listar_tarefas()
                elif escolha == '2':
                    tela_criar_tarefa()
                elif escolha == '3':
                    tela_editar_tarefa()
                elif escolha == '4':
                    tela_concluir_tarefa()
                elif escolha == '5':
                    tela_excluir_tarefa()
                elif escolha == '6':
                    tela_relatorios()
                elif escolha == '7':
                    logout()
                else:
                    print("Opção inválida. Tente novamente.")
            else:
                escolha = menu_principal()
                
                if escolha == '1':
                    tela_login()
                elif escolha == '2':
                    tela_cadastro()
                elif escolha == '3':
                    print("Saindo do TaskFlow. Até mais!")
                    EXECUTANDO = False
                else:
                    print("Opção inválida. Tente novamente.")
        except Exception as e:
            print(f"\n--- ERRO GLOBAL ---")
            print(f"Ocorreu um erro inesperado: {e}")
            print("O sistema continuará rodando. Por favor, tente novamente.")

            
if __name__ == "__main__":
    """
    PONTO DE ENTRADA DO PROGRAMA
    
    EXPLICAÇÃO:
        Esta condição verifica se o arquivo está sendo executado diretamente
        (não importado como módulo).
        
        - Se executado: python main.py → loop_principal() é chamado
        - Se importado: import main → loop_principal() NÃO é chamado
    
    BOA PRÁTICA:
        Permite que o código seja reutilizável e testável, pois pode
        ser importado sem executar automaticamente.
    """
    loop_principal()
