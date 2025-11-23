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