import hashlib

# Variável global para simular o usuário logado (sessão)
# Em um sistema real, isso seria gerenciado por sessões web ou tokens
USUARIO_LOGADO = None

def _hash_senha(senha):
    return hashlib.sha256(senha.encode('utf-8')).hexdigest()


def _carregar_usuarios():
    return ler_dados(ARQUIVO_USUARIOS)

def _salvar_usuarios(usuarios):
    return salvar_dados(ARQUIVO_USUARIOS, usuarios)


def cadastrar_usuario(nome, email, login, senha):
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
    return USUARIO_LOGADO

def logout():
    global USUARIO_LOGADO
    if USUARIO_LOGADO:
        print(f"Logout de {USUARIO_LOGADO['nome']} realizado com sucesso.")
        USUARIO_LOGADO = None
        return True
    return False