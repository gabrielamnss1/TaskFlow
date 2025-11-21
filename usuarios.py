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
