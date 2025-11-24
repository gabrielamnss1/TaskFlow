"""
================================================================================
MÓDULO: utils/arquivos.py
================================================================================
DESCRIÇÃO:
    Módulo utilitário responsável pela PERSISTÊNCIA DE DADOS do sistema.
    Gerencia a leitura e escrita de arquivos JSON para armazenar informações
    de usuários e tarefas.

FUNCIONALIDADES PRINCIPAIS:
    - Criar diretórios automaticamente quando necessário
    - Ler dados de arquivos JSON (com tratamento de erros)
    - Salvar dados em arquivos JSON (formatados e com UTF-8)
    - Garantir integridade dos dados mesmo em primeira execução

ARQUIVOS GERENCIADOS:
    - data/usuarios.json: Armazena cadastros de usuários
    - data/tarefas.json: Armazena todas as tarefas criadas

IMPORTANTE PARA APRESENTAÇÃO:
    Este módulo é a "camada de persistência" do sistema, separando a lógica
    de negócio (regras) da lógica de armazenamento (arquivos).
================================================================================
"""

import json
import os

# Define o caminho dos arquivos JSON onde os dados serão armazenados
# Usaremos um diretório 'data' para organizar melhor o projeto
ARQUIVO_USUARIOS = 'data/usuarios.json'
ARQUIVO_TAREFAS = 'data/tarefas.json'


def garantir_diretorio(caminho):
    """
    Cria o diretório necessário para salvar um arquivo, caso ainda não exista.
    
    PARÂMETROS:
        caminho (str): Caminho completo do arquivo (ex: 'data/usuarios.json')
    
    FUNCIONAMENTO:
        1. Extrai o nome do diretório do caminho do arquivo
        2. Verifica se o diretório existe
        3. Se não existir, cria toda a estrutura de pastas necessária
    
    EXEMPLO:
        Se o caminho for 'data/usuarios.json', cria a pasta 'data/'
    """
    # Extrai o diretório do caminho do arquivo
    diretorio = os.path.dirname(caminho)
    # Se o caminho for apenas um nome de arquivo, dirname retorna string vazia,
    # então verificamos se diretorio existe e se o caminho não é vazio.
    if diretorio and not os.path.exists(diretorio):
        os.makedirs(diretorio)


def ler_dados(caminho_arquivo):
    """
    Lê e retorna os dados armazenados em um arquivo JSON.
    
    PARÂMETROS:
        caminho_arquivo (str): Caminho do arquivo a ser lido
    
    RETORNO:
        list: Lista de dicionários com os dados (usuários ou tarefas)
              Retorna [] (lista vazia) se o arquivo não existir ou
              estiver vazio
    
    TRATAMENTO DE ERROS:
        - FileNotFoundError: Arquivo ainda não foi criado (primeira execução)
        - JSONDecodeError: Arquivo está corrompido ou vazio
        - Em ambos os casos, retorna lista vazia para não quebrar o sistema
    
    IMPORTANTE:
        Esta função garante que o sistema sempre tenha dados válidos,
        mesmo na primeira execução ou em caso de problemas.
    """
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
    """
    Salva uma lista de dados em um arquivo JSON formatado.
    
    PARÂMETROS:
        caminho_arquivo (str): Caminho onde o arquivo será salvo
        dados (list): Lista de dicionários a ser salva
    
    RETORNO:
        bool: True se salvou com sucesso, False se houve erro
    
    FORMATAÇÃO:
        - indent=4: Salva com indentação de 4 espaços (arquivo legível)
        - ensure_ascii=False: Permite acentos e caracteres especiais (UTF-8)
        - encoding='utf-8': Garante compatibilidade com português
    
    SEGURANÇA:
        Trata exceções para evitar perda de dados em caso de erro
        de escrita (disco cheio, permissões, etc.)
    """
    garantir_diretorio(caminho_arquivo)
    try:
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            # ensure_ascii=False para permitir caracteres UTF-8 no JSON
            json.dump(dados, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar dados em {caminho_arquivo}: {e}")
        return False
