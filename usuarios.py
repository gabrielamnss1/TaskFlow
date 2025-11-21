"""
================================================================================
MÓDULO: usuarios.py
================================================================================
DESCRIÇÃO:
    Módulo responsável pelo GERENCIAMENTO DE USUÁRIOS do sistema TaskFlow.
    Implementa todas as funcionalidades relacionadas a autenticação e
    controle de acesso.

FUNCIONALIDADES PRINCIPAIS:
    - Cadastro de novos usuários
    - Login com autenticação segura (hash SHA256)
    - Logout do sistema
    - Controle de sessão (usuário logado)
    - Busca de usuários por ID

SEGURANÇA:
    - Senhas nunca são armazenadas em texto puro
    - Utiliza hash SHA256 para criptografia de senhas
    - Validação de unicidade de login
    - Remoção do hash da senha na sessão ativa

IMPORTANTE PARA APRESENTAÇÃO:
    Este módulo demonstra boas práticas de segurança em sistemas web:
    - Nunca armazenar senhas em texto claro
    - Usar funções hash criptográficas
    - Separar dados sensíveis da sessão do usuário
================================================================================
"""

import hashlib
from utils.arquivos import ler_dados, salvar_dados, ARQUIVO_USUARIOS
# Variável global para simular o usuário logado (sessão)
# Em um sistema real, isso seria gerenciado por sessões web ou tokens
USUARIO_LOGADO = None

def _hash_senha(senha):
    """
    Gera o hash criptográfico SHA256 da senha.
    
    PARÂMETROS:
        senha (str): Senha em texto puro
    
    RETORNO:
        str: Hash hexadecimal de 64 caracteres
    
    SEGURANÇA:
        SHA256 é uma função hash unidirecional: é impossível recuperar
        a senha original a partir do hash. Por isso é seguro armazenar.
    
    EXEMPLO:
        senha "123" → hash "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
    """
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()


def _carregar_usuarios():
    """
    Carrega a lista de todos os usuários do arquivo JSON.
    
    RETORNO:
        list: Lista de dicionários com dados dos usuários
    """
    return ler_dados(ARQUIVO_USUARIOS)

def _salvar_usuarios(usuarios):
    """
    Salva a lista de usuários no arquivo JSON.
    
    PARÂMETROS:
        usuarios (list): Lista completa de usuários a ser salva
    
    RETORNO:
        bool: True se salvou com sucesso, False caso contrário
    """
    return salvar_dados(ARQUIVO_USUARIOS, usuarios)


def cadastrar_usuario(nome, email, login, senha):
    """
    Cadastra um novo usuário no sistema.
    
    PARÂMETROS:
        nome (str): Nome completo do usuário
        email (str): E-mail do usuário
        login (str): Login único para acesso ao sistema
        senha (str): Senha em texto puro (será criptografada)
    
    RETORNO:
        bool: True se cadastrou com sucesso, False se login já existe
    
    PROCESSO:
        1. Carrega lista de usuários existentes
        2. Verifica se o login já está em uso (deve ser único)
        3. Cria novo usuário com ID auto-incrementado
        4. Gera hash da senha (nunca salva senha em texto puro)
        5. Adiciona à lista e salva no arquivo
    
    VALIDAÇÕES:
        - Login deve ser único no sistema
        - Senha é automaticamente criptografada com SHA256
    """
    usuarios = _carregar_usuarios()
    
    # 1. Verificar unicidade do login
    if any(u['login'] == login for u in usuarios):
        print(f"Erro: O login '{login}' já está em uso.")
        return False
    
    # 2. Criar o novo usuário
    novo_usuario = {
        'id': len(usuarios) + 1, # ID simples baseado no tamanho da lista
        'nome': nome,
        'email': email,
        'login': login,
        'senha_hash': _hash_senha(senha) # Armazena o hash da senha
    }
    
    # 3. Adicionar e salvar
    usuarios.append(novo_usuario)
    if _salvar_usuarios(usuarios):
        print(f"Usuário '{login}' cadastrado com sucesso!")
        return True
    return False


def autenticar_usuario(login, senha):
    """
    Realiza o login do usuário no sistema.
    
    PARÂMETROS:
        login (str): Login do usuário
        senha (str): Senha em texto puro (será comparada via hash)
    
    RETORNO:
        dict: Dados do usuário se autenticado com sucesso
        None: Se login ou senha estiverem incorretos
    
    PROCESSO DE AUTENTICAÇÃO:
        1. Carrega todos os usuários
        2. Gera o hash da senha fornecida
        3. Procura usuário com login e hash correspondentes
        4. Se encontrar, define como usuário logado (sessão)
        5. Remove dados sensíveis antes de retornar
    
    SEGURANÇA:
        - Compara hashes, nunca senhas em texto puro
        - Remove o hash da senha da sessão ativa
        - Mensagem de erro genérica (não indica se login ou senha está errado)
    """
    global USUARIO_LOGADO
    usuarios = _carregar_usuarios()
    senha_hash = _hash_senha(senha)
    
    for usuario in usuarios:
        if usuario['login'] == login and usuario['senha_hash'] == senha_hash:
            # Remove o hash da senha antes de definir como logado
            usuario_logado = {k: v for k, v in usuario.items() if k != 'senha_hash'}
            USUARIO_LOGADO = usuario_logado
            print(f"Bem-vindo(a), {usuario_logado['nome']}!")
            return usuario_logado
            
    print("Erro: Login ou senha inválidos.")
    return None


def get_usuario_logado():
    """
    Retorna os dados do usuário atualmente logado.
    
    RETORNO:
        dict: Dados do usuário logado (sem senha)
        None: Se ninguém estiver logado
    
    USO:
        Usado por outros módulos para verificar permissões e
        identificar quem está executando ações no sistema.
    """
    return USUARIO_LOGADO

def logout():
    """
    Realiza o logout do usuário atual.
    
    RETORNO:
        bool: True se havia alguém logado, False caso contrário
    
    EFEITO:
        Limpa a variável global USUARIO_LOGADO, encerrando a sessão
    """
    global USUARIO_LOGADO
    if USUARIO_LOGADO:
        print(f"Logout de {USUARIO_LOGADO['nome']} realizado com sucesso.")
        USUARIO_LOGADO = None
        return True
    return False

def get_usuario_por_id(user_id):
    """
    Busca um usuário específico pelo seu ID.
    
    PARÂMETROS:
        user_id (int): ID do usuário a ser buscado
    
    RETORNO:
        dict: Dados completos do usuário se encontrado
        None: Se não encontrar usuário com esse ID
    
    USO:
        Útil para relatórios e exibição de informações de responsáveis
        por tarefas, mesmo que não estejam logados.
    """
    usuarios = _carregar_usuarios()
    for usuario in usuarios:
        if usuario['id'] == user_id:
            return usuario
    return None
