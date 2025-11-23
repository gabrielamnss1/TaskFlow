import json
import os

# Define o caminho dos arquivos JSON onde os dados serão armazenados
# Usaremos um diretório 'data' para organizar melhor o projeto
ARQUIVO_USUARIOS = 'data/usuarios.json'
ARQUIVO_TAREFAS = 'data/tarefas.json'


def garantir_diretorio(caminho):
    # Extrai o diretório do caminho do arquivo
    diretorio = os.path.dirname(caminho)
    # Se o caminho for apenas um nome de arquivo, dirname retorna string vazia,
    # então verificamos se diretorio existe e se o caminho não é vazio.
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)
        
def ler_dados(caminho_arquivo):
    garantir_diretorio(caminho_arquivo)
    try:
        with open(caminho_arquivo, 'r', encoding='utf-8') as f:
            # Tenta carregar o JSON. Se o arquivo estiver vazio, retorna []
            conteudo = f.read()
            if not conteudo:
                return []
            return json.loads(conteudo)
    except FileNotFoundError:
        # Retorna uma lista vazia se o arquivo não existir (primeira execução)
        return []
    except json.JSONDecodeError:
        # Retorna uma lista vazia se o arquivo estiver corrompido ou vazio
        return []
    
def salvar_dados(caminho_arquivo, dados):
    garantir_diretorio(caminho_arquivo)
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            # ensure_ascii=False para permitir caracteres UTF-8 no JSON
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados em {caminho_arquivo}: {e}")
        return False
