# TaskFlow - Gerenciador de Tarefas

## Descrição

TaskFlow é um sistema de gerenciamento de tarefas desenvolvido em Python que permite aos usuários criar, editar, acompanhar e concluir tarefas com prazos definidos. O sistema foi projetado com foco em segurança, boas práticas de programação e facilidade de uso, com interface de linha de comando (CLI) intuitiva.

---

## Funcionalidades Principais

### Gerenciamento de Usuários
- Cadastro de Novos Usuários: Criar contas com nome, e-mail, login e senha
- Autenticação Segura: Login com hash SHA256 para proteção de senha
- Controle de Sessão: Gerenciamento de usuário logado
- Logout: Encerramento seguro de sessão

### Gerenciamento de Tarefas (CRUD Completo)
- Criar Tarefas: Adicionar novas tarefas com título, descrição e prazo
- Listar Tarefas: Visualizar todas as tarefas pessoais com status automático
- Editar Tarefas: Modificar título, descrição ou prazo existentes
- Concluir Tarefas: Marcar tarefas como concluídas
- Excluir Tarefas: Remover tarefas permanentemente do sistema
- Detecção de Tarefas Atrasadas: Identificação automática de prazos vencidos

### Sistema de Relatórios
- Tarefas Concluídas: Histórico e estatísticas de produtividade
- Tarefas Pendentes: Lista de trabalho em andamento
- Tarefas Atrasadas: Alertas de urgência para prazos vencidos
- Exportação em TXT: Salvar relatórios em arquivo para posterior análise

### Estrutura de Dados de Tarefas
Cada tarefa contém:
- id: Identificador único auto-incrementado
- título: Nome da tarefa
- descrição: Descrição detalhada
- responsável_id: ID do usuário responsável
- responsável_nome: Nome do responsável (referência facilitada)
- prazo: Data limite (formato DD/MM/AAAA)
- status: Estado (Pendente, Concluída, Atrasada)
- criação: Data e hora de criação (timestamp)

---

## Estrutura de Arquivos

Task/
- main.py               # Controlador principal, interface do usuário e loop de eventos
- usuarios.py          # Módulo de autenticação e gerenciamento de usuários
- Tarefas.py           # Módulo de gerenciamento de tarefas (CRUD completo)
- README.md            # Este arquivo
- utils/
  - arquivos.py        # Funções de leitura/escrita persistente em JSON (quando implementado)

---

## Atualizações Recentes

### Novas Implementações
- Loop principal com gerenciamento de estado (logado/não logado)
- Sistema de relatórios com três categorias (Concluídas, Pendentes, Atrasadas)
- Detecção automática e dinâmica de tarefas com prazos vencidos
- Funções adicionais: tela_concluir_tarefa(), tela_excluir_tarefa(), tela_relatorios()
- Exportação de relatórios em arquivo TXT com timestamp
- Interface CLI completa com menus personalizados

### Melhorias de Código
- Docstrings detalhadas em todas as funções (padrão PEP 257)
- Constantes para status de tarefas (evita erros de digitação)
- Funções auxiliares centralizadas (_encontrar_tarefa, etc.)
- Tratamento robusto de exceções
- Separação clara de responsabilidades entre módulos

### Padrões Implementados
- MVC Simplificado: View (telas), Controller (menus e loop), Model (dados)
- Event Loop: Padrão reativo para fluxo de aplicação
- CRUD Completo: Create, Read, Update, Delete em tarefas
- Factory Pattern: Criação de IDs auto-incrementados

---

### main.py - Controlador Principal
Responsável pela interface do usuário e orquestração do fluxo da aplicação.

Segue padrão MVC simplificado com separação clara de responsabilidades.

Funções de Menu:
- menu_principal() - Menu para usuários não autenticados (Login, Cadastro, Sair)
- menu_logado() - Menu personalizado para usuários autenticados

Funções de Interface (Telas):
- tela_cadastro() - Coleta dados para novo cadastro de usuário
- tela_login() - Interface de autenticação
- tela_criar_tarefa() - Formulário para criar nova tarefa
- tela_editar_tarefa() - Interface para editar tarefa existente
- tela_concluir_tarefa() - Interface para marcar tarefa como concluída
- tela_excluir_tarefa() - Interface para remover tarefa
- tela_relatorios() - Menu e interface de relatórios

Função de Controle:
- loop_principal() - O "coração" da aplicação, gerencia o fluxo de eventos
  e alterna entre estado logado e não logado

Entrada do Programa:
- __main__: Ponto de entrada que inicia o loop_principal()

---

### usuarios.py - Gerenciamento de Usuários
Módulo de autenticação e gerenciamento de usuários com segurança de ponta.

Funções Principais:
- cadastrar_usuario(nome, email, login, senha) - Registra novo usuário com validação de login único
- autenticar_usuario(login, senha) - Realiza login com comparação de hash
- get_usuario_logado() - Retorna dados do usuário em sessão ativa
- logout() - Encerra a sessão do usuário atual
- get_usuario_por_id(user_id) - Busca usuário específico pelo ID

Funções Internas:
- _hash_senha(senha) - Gera hash SHA256 da senha
- _carregar_usuarios() - Carrega lista de usuários do arquivo JSON
- _salvar_usuarios(usuarios) - Persiste lista de usuários no JSON

Segurança Implementada:
- Senhas armazenadas com hash SHA256 (unidirecional)
- Senhas nunca aparecem em texto puro na sessão
- Validação de unicidade de login no cadastro
- Sessão segura sem dados sensíveis
- Mensagens de erro genéricas (não especificam se login ou senha estão errados)

---

### tarefas.py - Gerenciamento de Tarefas (CRUD)
Módulo que implementa todas as operações de Criação, Leitura, Atualização e Exclusão de tarefas.

Funções Principais:
- criar_tarefa(titulo, descricao, prazo_str) - Cria nova tarefa com validação de formato de data
- listar_tarefas(filtrar_por_responsavel=True) - Lista tarefas com filtro opcional
  * Detecta automaticamente tarefas atrasadas comparando prazo com data atual
  * Mostra status visual dinamicamente sem alterar o arquivo
- editar_tarefa(tarefa_id, novo_titulo, nova_descricao, novo_prazo) - Modifica tarefa existente com controle de acesso
- concluir_tarefa(tarefa_id) - Marca tarefa como concluída
- excluir_tarefa(tarefa_id) - Remove tarefa permanentemente

Funções Internas:
- _carregar_tarefas() - Carrega lista de tarefas do arquivo JSON
- _salvar_tarefas(tarefas) - Persiste lista de tarefas no JSON
- _encontrar_tarefa(tarefas, tarefa_id) - Busca auxiliar centralizada por ID

Constantes de Status:
- STATUS_PENDENTE = "Pendente" - Tarefa criada, aguardando conclusão
- STATUS_CONCLUIDA = "Concluída" - Tarefa finalizada pelo responsável
- STATUS_ATRASADA = "Atrasada" - Tarefa pendente com prazo vencido (detectado dinamicamente)

Regras de Negócio:
- Apenas usuário logado pode criar tarefas
- IDs são auto-incrementados e únicos
- Datas devem estar no formato DD/MM/AAAA
- Cada tarefa registra automaticamente a hora de criação
- Tarefas atrasadas são detectadas em tempo real (sem modificar o JSON)

Controle de Acesso e Segurança (Novo):
- Apenas o responsável pela tarefa pode editá-la, concluí-la ou excluí-la
- Validações de permissão impedem acesso não autorizado
- Campos opcionais em edição permitem modificações parciais
- Confirmação de sucesso com mensagens claras ao usuário

---

### relatorios.py - Geração de Relatórios
Módulo responsável pela coleta, formatação e exportação de relatórios de tarefas.

Funções Principais (implementadas em main.py):
- tarefas_concluidas() - Retorna lista de tarefas com status Concluída
- tarefas_pendentes() - Retorna lista de tarefas com status Pendente
- tarefas_atrasadas() - Retorna lista de tarefas com prazo vencido
- exibir_relatorio(titulo, lista_tarefas) - Formata e exibe relatório no console
- exportar_relatorio(titulo, lista_tarefas) - Salva relatório em arquivo TXT

Funcionalidades:
- Filtragem por status de tarefa
- Estatísticas (contagem total, por responsável)
- Formatação clara e legível para console
- Exportação com timestamp para arquivo TXT
- Cada usuário vê apenas suas próprias tarefas nos relatórios

__NOTA__: As funções de relatório estão sendo implementadas atualmente. O módulo `relatorio.py` contém a estrutura base com documentação completa, e as funções serão desenvolvidas em breve para integração total com o sistema.

---

## Como Usar

### 1. Executar o Programa
`
python main.py
`

### 2. Menu Principal (Não Logado)
`
--- TaskFlow - Gerenciador de Tarefas ---
1. Login
2. Cadastrar Novo Usuário
3. Sair
`

Escolha 1 para fazer login ou 2 para criar uma conta nova.

### 3. Cadastrar Novo Usuário
- Escolha opção 2 no menu principal
- Forneça: nome completo, e-mail, login único e senha
- O sistema validará a unicidade do login
- Após cadastro, você pode fazer login com suas credenciais

### 4. Fazer Login
- Escolha opção 1 no menu principal
- Informe o login e senha cadastrados
- O sistema autenticará suas credenciais
- Após login bem-sucedido, você acessará o menu personalizado

### 5. Menu Logado (Após Autenticação)
`
--- Menu de [Seu Nome] ---
1. Minhas Tarefas
2. Criar Nova Tarefa
3. Editar Tarefa
4. Concluir Tarefa
5. Excluir Tarefa
6. Relatórios
7. Logout
`

#### Opção 1: Minhas Tarefas
- Exibe todas as suas tarefas com formatação clara
- Mostra: ID, Título, Prazo, Status (com detecção automática de atrasadas)
- Status atrasado é calculado em tempo real

#### Opção 2: Criar Nova Tarefa
- Título: Resumo curto da tarefa
- Descrição: Detalhes sobre o que fazer
- Prazo: Data limite no formato DD/MM/AAAA

Dica: O sistema validará o formato da data automaticamente.

#### Opção 3: Editar Tarefa
1. Exibe lista de suas tarefas
2. Informe o ID da tarefa a editar
3. Deixe campos em branco para não alterar
4. Preencha apenas os campos que deseja modificar
5. Mudanças são salvas imediatamente

#### Opção 4: Concluir Tarefa
1. Exibe lista de suas tarefas
2. Informe o ID da tarefa a concluir
3. Status muda para "Concluída" automaticamente

#### Opção 5: Excluir Tarefa
1. Exibe lista de suas tarefas
2. Informe o ID da tarefa a excluir
3. Exclusão é permanente (sem confirmação adicional)

#### Opção 6: Relatórios
Submenu com opções de geração de relatórios:
1. Tarefas Concluídas - Visualiza histórico de tarefas finalizadas
2. Tarefas Pendentes - Lista de tarefas em andamento
3. Tarefas Atrasadas - Alertas de prazos vencidos
4. Voltar - Retorna ao menu anterior

Após gerar um relatório, você pode optar por exportar para arquivo TXT.

#### Opção 7: Logout
- Encerra sua sessão
- Retorna ao menu principal

---

## Loop Principal e Fluxo da Aplicação

O sistema utiliza um padrão de "event loop" (similar ao usado em frameworks web):

1. ESTADO NÃO LOGADO:
   - Exibe menu_principal()
   - Permite: Login, Cadastro ou Sair

2. ESTADO LOGADO:
   - Exibe menu_logado() personalizado com nome do usuário
   - Permite: Gerenciar tarefas, gerar relatórios

O loop continua até o usuário escolher "Sair". Qualquer erro no processamento é capturado e tratado sem encerrar o programa.

---

## Detecção de Tarefas Atrasadas

O sistema detecta automaticamente tarefas atrasadas:

1. Ao listar tarefas, compara o prazo com a data atual
2. Se a tarefa está em status "Pendente" e o prazo já passou, aparece como "Atrasada"
3. A detecção é dinâmica (em tempo real) sem modificar os dados armazenados
4. Tarefas concluídas nunca aparecem como atrasadas
5. No relatório de atrasadas, mostra apenas pendentes com prazo vencido

---

## Boas Práticas de Segurança

1. Hash de Senhas: Utiliza SHA256 para criptografia unidirecional
2. Sessão Segura: Nunca armazena senhas em memória
3. Validação de Entrada: Verifica unicidade de login e formato de data
4. Mensagens Genéricas: "Login ou senha inválidos" (não especifica qual está errado)
5. Isolamento de Dados: Usuários só veem suas próprias tarefas
6. Proteção contra Acesso Direto: Funções internas (_nome) separadas das públicas

---

## Formato de Dados

### Usuários (JSON)
{
  "id": 1,
  "nome": "Gabriela M Silva",
  "email": "gabriela.m.silva@ba.estudante.senai.br",
  "login": "gabriela_silva",
  "senha_hash": "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"
}

### Tarefas (JSON)
{
  "id": 1,
  "titulo": "Exemplo de Tarefa",
  "descrição": "Descrição detalhada",
  "responsável_id": 1,
  "responsável_nome": "Gabriela M Silva",
  "prazo": "31/12/2025",
  "status": "Pendente",
  "criação": "2025-11-22 14:30:00"
}

---

## Exemplo de Fluxo Completo

1. Execute: python main.py
2. Escolha: 2 - Cadastrar Novo Usuário
3. Digite dados (nome, e-mail, login, senha)
4. Retorne ao menu e escolha: 1 - Login
5. Faça login com suas credenciais
6. Escolha: 2 - Criar Nova Tarefa
7. Preencha título, descrição e prazo
8. Veja suas tarefas com: 1 - Minhas Tarefas
9. Edite com: 3 - Editar Tarefa
10. Marque como concluída com: 4 - Concluir Tarefa
11. Gere relatório com: 6 - Relatórios
12. Escolha 1 para Tarefas Concluídas
13. Exporte para arquivo TXT se desejar
14. Faça logout com: 7 - Logout

---

## Requisitos

- Python 3.7 ou superior
- Sistema de arquivos disponível (para persistência em JSON)
- Nenhuma dependência externa necessária

---

## Notas Importantes

- Persistência: Todos os dados são salvos em arquivos JSON
- Validação de Datas: Sempre use o formato DD/MM/AAAA
- Login Único: Cada login deve ser único no sistema
- Usuário Responsável: Tarefas são automaticamente atribuídas ao usuário logado
- Detecção Dinâmica: Tarefas atrasadas são calculadas em tempo real
- Segurança: Senhas são irreversivelmente criptografadas com SHA256

---

## Arquitetura e Padrões

### Padrão de Projeto
- MVC Simplificado: Separação entre Interface (main.py), Lógica (tarefas.py, usuarios.py) e Dados (utils/arquivos.py)
- Event Loop: Padrão usado em aplicações interativas para controlar fluxo de usuário

### Princípios SOLID Aplicados
- Single Responsibility: Cada módulo tem uma responsabilidade clara
- Open/Closed: Fácil adicionar novos módulos sem modificar os existentes
- Dependency Inversion: Módulos dependem de interfaces abstratas (arquivos.py)

### Boas Práticas
- Funções bem documentadas com docstrings detalhadas
- Constantes em MAIÚSCULAS para evitar erros
- Funções internas (prefixo _) separadas das públicas
- Tratamento de exceções em pontos críticos
- Mensagens de erro claras e úteis ao usuário

---

## Autor

Desenvolvido como um projeto educacional para demonstrar boas práticas em Python, incluindo:
- Modularização e separação de responsabilidades
- Segurança em autenticação e criptografia
- Persistência de dados em JSON
- Interface interativa com usuário
- Padrões de design e arquitetura

Atualizado com novas funcionalidades:
- Sistema completo de relatórios
- Detecção automática de tarefas atrasadas
- Loop principal com gerenciamento de estado
- Exportação de relatórios em TXT

---

## Licença

Este projeto é de código aberto e disponível para fins educacionais.

---

## Equipe

### Informações do Projeto
- Disciplina: Lógica de Programação
- Professor: Washington Luis Souza Anunciação
- Data de Início: 22 de novembro de 2025

### Integrantes

| # | Nome Completo | Email |
|---|---|---|
| 1 | Gabriela M. N. Silva | gabriela.m.silva@ba.estudante.senai.br |
| 2 | Cristiano Silva Santos | Cristiano.s.santos@ba.estudante.senai.br |
| 3 | Joel Macena Costa | joel.c@ba.estudante.senai.br |
| 4 | Josilton José Almeida Santos | josilton.santos@aluno.senai.br |

### Responsabilidades
- **Gabriela M. N. Silva** (gabriela.m.silva@ba.estudante.senai.br): Desenvolvedora principal, autora da conta GitHub, integração com repositório remoto
- **Cristiano Silva Santos** (Cristiano.s.santos@ba.estudante.senai.br): Desenvolvedor, contribuidor do projeto
- **Joel Macena Costa** (joel.c@ba.estudante.senai.br): Desenvolvedor, contribuidor do projeto
- **Josilton José Almeida Santos** (josilton.santos@aluno.senai.br): Desenvolvedor, contribuidor do projeto

### Contribuições
Todos os integrantes contribuem para:
- Implementação de funcionalidades
- Testes e validação
- Documentação
- Revisão de código

---

## Histórico de Atualizações

### 22 de Novembro de 2025
- Estrutura inicial do projeto criada
- Módulos básicos implementados (usuarios.py, Tarefas.py, main.py)
- Sistema de autenticação com SHA256
- CRUD completo de tarefas
- Loop principal com gerenciamento de estado
- Sistema de relatórios (Concluídas, Pendentes, Atrasadas)
- Detecção automática de tarefas atrasadas
- Documentação completa do projeto

### Atualizações Recentes (Última Versão)
- **Funções CRUD Expandidas**: Implementação completa de `editar_tarefa()`, `concluir_tarefa()` e `excluir_tarefa()` em `Tarefas.py`
- **Controle de Acesso**: Validação de segurança assegurando que apenas o responsável pela tarefa pode editá-la, concluí-la ou excluí-la
- **Arquivo de Relatórios**: Criação de `relatorio.py` com estrutura pronta para implementação de funções de geração de relatórios
- **Tabela de Integrantes Atualizada**: Adição de coluna de email para melhor contato com todos os membros da equipe
- **Documentação Aprimorada**: Melhoria nas responsabilidades e informações de contato de cada membro do projeto

---

